import tornado.web
import const
import json
import datetime
import dateutil.parser
import math
from pymongo import MongoClient

from google_api.google_places import *
from google_api.google_utils import get_distance

FAR = 69696969696969.420

class BaseHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, PATCH, DELETE, OPTIONS, HEAD")
        self.set_header("Content-Type", "application/json")

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
        self.write(json.dumps({'shit': 'works'}))


class DataHandler(BaseHandler):
    def day_of_week(self, x):
        efunc = math.exp(-1*pow(x - 5.3, 2)/1.5)
        return 1+efunc

    def gender_func(self, x):
        return x*0.2 + 1

    def tolerance(self, x):
        return 0.8 + x*0.2

    def bpm_percent(self, x):
        if x > 1.5:
            return 1.0
        return 6/x - 2

    def time_of_day(self, x):
        if x > 12:
            x = x - 24
        if -6 < x and x < 6:
            return math.exp(-1.0*x*x/20)*1.5 + 1
        return 1

    def proximity_func_bar(self, x):
        return math.exp(-1.0*x*x/8192)*4 + 1

    def proximity_func_nightclub(self, x):
        return math.exp(-1.0*x*x/8192)*4 + 1

    def proximity_func_casino(self, x):
        return math.exp(-1.0*x*x/8192)*2 + 1

    def proximity_func_danger(self, x, count):
        if count < 1:
            return 1
        multiplier = ((-1)/x+2)/2
        return math.exp(-1.0*x*x/8192)*4 * multiplier + 1

    def age_func(self, x):
        if x < 12:
            return x/17
        elif x <25:
            return pow(x-12,1.7)/8.5 + 12/17
        elif x < 65:
            return -10*x/55 + 160/11
        else:
            return 1


    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        uuid = data['uuid']
        _lng = float(data['lng'])
        _lat = float(data['lat'])
        timestamp = dateutil.parser.parse(data['timestamp'])
        bpm = data['bpm']

        user_data = self.user_data.find({'uuid': uuid})[0]
        gender = user_data['gender']
        age = 25
        tolerance = user_data['tolerance']
        resting_bpm = user_data['bpm']

        data_point = {
            'uuid' : uuid,
            'timestamp' : data['timestamp'],
            'tolerance' : tolerance,
            'age' : age,
            'gender' : gender,
        }

        # get location factor
        nearby = self.g.get_high_priority(_lat, _lng)
        found = True
        place_id = None
        distance =  FAR #blaze
        count = 0

        data_point['prox_bar'] = FAR
        data_point['prox_danger'] = FAR
        data_point['prox_night'] = FAR
        data_point['prox_casino'] = FAR

        if nearby:
            closest_place = nearby[0]

        else:
            nearby = self.g.get_nearest_general(_lat, _lng)
            for place in nearby:
                count = self.locations.count({'place_id': place['place_id']})
                if count:
                    closest_place = place
                    break
            found = False

        data_point['count'] = count

        if found:
            place_id = closest_place['place_id']
            distance = get_distance(_lat, _lng, closest_place['lat'], closest_place['lng'])

        if 'bar' in closest_place['types']:
            dist_factor = self.proximity_func_bar(distance)
            data_point['prox_bar'] = distance
        elif 'nightclub' in closest_place['types']:
            dist_factor = self.proximity_func_nightclub(distance)
            data_point['prox_night'] = distance
        elif 'casino' in closest_place['types']:
            dist_factor = self.proximity_func_casino(distance)
            data_point['prox_casino'] = distance
        else:
            dist_factor = self.proximity_func_casino(distance)
            data_point['prox_danger'] = distance

        # get day of week factor
        weekday = timestamp.weekday()
        if weekday == 6:
            weekday = 0
        else:
            weekday += 1
        dow_factor = self.day_of_week(timestamp.weekday())

        data_point['weekday'] = weekday

        #get gen fact
        if gender.lower() == 'male':
            gen_factor = self.gender_func(0)
            data_point['gender'] = 0
        else:
            gen_factor = self.gender_func(1)
            data_point['gender'] = 1

        #get tolerance fact
        tolerance = 2 - tolerance
        tol_factor = self.tolerance(tolerance)
        data_point['tol'] = tolerance
        
        #get bpm shit
        percent_bpm = float(bpm) / resting_bpm
        data_point['bpm'] = percent_bpm
        bpm_factor = self.bpm_percent(percent_bpm)

        #time of day shit
        hour = timestamp.hour
        if hour > 12:
            hour = hour - 24

        data_point['hour'] = hour

        tod_factor = self.time_of_day(hour)

        #age factor
        age_factor = self.age_func(age)
        print age_factor
        print tod_factor
        print bpm_factor
        print tol_factor
        print gen_factor
        print dow_factor
        print dist_factor
        result = float(age_factor * tod_factor * bpm_factor * tol_factor * gen_factor * dow_factor * dist_factor)
        print result
        response = {'place_id': place_id}

        if result >= 30:
            response['drunk'] = True
        else:
            response['drunk'] = False
        self.write(json.dumps(response))

        data_point['count'] = 0

        if found:
            exist = self.locations.count({'place_id': closest_place['place_id']})
            if exist:
                res = self.locations.update_one({'place_id': closest_place['place_id']}, {'$inc': {'count': 1}})
            else:
                self.locations.insert_one({'place_id': closest_place['place_id'], 'count': 1})

        if response['drunk'] == True:
            data_point['rating'] = 2
            self.request_data.insert_one(data_point)

class ConfirmHandler(BaseHandler):
    def post(self):
        conf = tornado.escape.json_decode(self.request.body)
        uuid = conf['uuid']
        timestamp = conf['timestamp']
        rating = conf['rating']
        print self.request_data.find({'uuid' : uuid, 'timestamp' : timestamp})[0]
        request = self.request_data.update_one({'uuid' : uuid, 'timestamp' : timestamp}, {'$set': {'rating' : rating}})
        if rating == 0:
            location = self.locations.find({'place_id': conf['place_id']})[0]
            if location['count'] > 1:
                self.locations.update_one({'place_id': conf['place_id']}, {'$inc': {'count': -1}})
            else:
                self.locations.remove(location)
