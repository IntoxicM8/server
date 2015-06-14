import tornado.web
import const
import json
import datetime
import dateutil.parser
import math
from pymongo import MongoClient

from google_api.google_places import *
from google_api.google_utils import get_distance

class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.db = self.application.client['database']
        self.db.authenticate(const.USERNAME, const.PASSWORD)
        self.user_data = self.db['user_data']
        self.request_data = self.db['request_data']
        self.locations = self.db['locations']
        self.g = GooglePlaces()


class UserHandler(BaseHandler):
    def get(self):
        uuid = int(self.get_argument('uuid'))
        user_data = self.user_data.find({'uuid': uuid})[0]
        user_data.pop('_id', None)
        self.write(json.dumps(user_data))

    def post(self):
        new_user = tornado.escape.json_decode(self.request.body)
        self.user_data.insert_one(new_user)
        self.write('shit worked')


class DataHandler(BaseHandler):
    def day_of_week(self, x):
        efunc = math.exp(-1*pow(x - 5.3, 2)/1.5)
        return 1+efunc

    def gender_func(self, x):
        return x*0.2 + 1

    def tolerance(self, x):
        return 0.8 + x*0.2

    def bpm_percent(self, x):
        return 3/x - 2

    def time_of_day(self, x):
        if -6 < x and x < 6:
            return math.exp(-1.0*x*x/20)*1.5
        return 0.1

    def proximity_func_bar(self, x):
        return math.exp(-1.0*x*x/8192)*4

    def proximity_func_nightclub(self, x):
        return math.exp(-1.0*x*x/8192)*4

    def proximity_func_casino(self, x):
        return math.exp(-1.0*x*x/8192)*2

    def age_func(self, x):
        if x < 12:
            return x/17
        elif 12 <= x and x <25:
            return pow(x-12,1.7)/8.5 + 12/17
        else:
            return -10*x/55 + 160/11

    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        uuid = data['uuid']
        _lng = data['lng']
        _lat = data['lat']
        timestamp = dateutil.parser.parse(data['timestamp'])
        bpm = data['bpm']

        user_data = self.user_data.find({'uuid': uuid})[0]
        gender = user_data['gender']
        age = user_data['age']
        tolerance = user_data['tolerance']
        resting_bpm = user_data['bpm']


        # get location factor
        nearby = self.g.get_high_priority(_lat, _lng)
        found = True
        place_id = None

        if nearby:
            closest_place = nearby[0]

        else:
            nearby = self.g.get_nearest_general(_lat, _lng)
            for place in nearby:
                nearby_in_db = self.locations.count({'place_id': place['place_id']})
                if count:
                    closest_place = place
                    break
            found = False

        if found:
            place_id = closest_place['place_id']
            distance = get_distance(_lat, _lng, closest_place['lat'], closest_place['lng'])
        else:
            distance = 69696969696969.420 #blaze

        if 'bar' or 'nightclub' in closest_place['types']:
            dist_factor = self.proximity_func_bar(distance)
        elif 'casino' in closest_place['types']:
            dist_factor = self.proximity_func_casino(distance)
        else:
            dist_factor = 1

        # get day of week factor
        dow_factor = self.day_of_week(timestamp.weekday())

        #get gen fact
        if gender.lower() == 'male':
            gen_factor = self.gender_func(0)
        else:
            gen_factor = self.gender_func(1)

        #get tolerance fact
        if tolerance.lower() == 'h':
            tol_factor = self.tolerance(0)
        elif tolerance.lower() == 'm':
            tol_factor = self.tolerance(1)
        else:
            tol_factor = self.tolerance(2)

        #get bpm shit
        percent_bpm = float(bpm) / resting_bpm
        bpm_factor = self.bpm_percent(percent_bpm)

        #time of day shit
        hour = timestamp.hour
        if hour > 2:
            hour = hour - 24

        tod_factor = self.time_of_day(hour)

        #age factor
        age_factor = self.age_func(age)

        result = float(age_factor * tod_factor * bpm_factor * tol_factor * gen_factor * dow_factor * dist_factor)
        print result
        response = {'place_id': place_id}

        if result >= 0.7:
            response['drunk'] = True
        else:
            response['drunk'] = False
        print(response)
        self.write(json.dumps(response))

        if found:
            exist = self.locations.count({'place_id': closest_place['place_id']})
            print(exist)
            if exist:
                exist = self.locations.find({'place_id': closest_place['place_id']})
                count = exist[0]['count'] + 1
                res = self.locations.update_one({'place_id': closest_place['place_id']}, {'$inc': {'count': count}})
            else:
                self.locations.insert_one({'place_id': closest_place['place_id'], 'count': 1})

class ConfirmHandler(BaseHandler):
    def post(self):
        self.write("Naren is gay")
