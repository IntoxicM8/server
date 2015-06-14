import tornado.web
import const
from pymongo import MongoClient

from google_api.google_places import *

class BaseHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.db = self.application.client['database']
        self.db.authenticate(const.USERNAME, const.PASSWORD)
        self.user_data = self.db['user_data']
        self.request_data = self.db['request_data']
        self.locations = self.db['locations']

class UserHandler(BaseHandler):
    def get(self):
        uuid = self.get_arguments('uuid')
        user_data = json.dumps(self.user_data.find_one({'uuid': uuid}))
        print(user_data)
        self.write(user_data)

    def post(self):
        #Creates a new user
        new_user = tornado.escape.json_decode(self.request.body)
        
        #Adds it to the database
        self.user_data.insert_one(new_user)

class DataHandler(BaseHandler):
    def post(self):
        #Create data dict
        data = tornado.escape.json_decode(self.request.body)

        #Write to DB - Needed for ML
        self.request_data.insert_one(data)

        #Find user from data
        user = self.user_data.find_one({'uuid': data['uuid']})

        '''
            The magic happens here
            Either math or ML, whatever
        '''

        self.write(GooglePlaces.get_nearest_general(43.6471642, -79.38705139999999))

class ConfirmHandler(BaseHandler):
    def post(self):
        self.write("Naren is gay")
