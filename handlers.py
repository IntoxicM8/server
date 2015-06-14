import tornado.web
import const
import json
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
        uuid = int(self.get_argument('uuid'))
        user_data = self.user_data.find({'uuid': uuid})[0]
        user_data.pop('_id', None)
        self.write(json.dumps(user_data))

    def post(self):
        new_user = tornado.escape.json_decode(self.request.body)
        self.user_data.insert_one(new_user)
        self.write('shit worked')


class DataHandler(BaseHandler):
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
        self.request_data.insert_one(data)

        self.write(GooglePlaces.get_nearest_general(43.6471642, -79.38705139999999))


class ConfirmHandler(BaseHandler):
    def post(self):
        self.write("Naren is gay")
