# Main file used for the endpoints
import tornado.web
import const
from pymongo import MongoClient

client = MongoClient(const.MONGO_URL)
db = client['db']

user_data = db['user_data']
request_data = db['request_data']
locations = db['locations']

class BaseHandler(tornado.web.RequestHandler):
    pass

class UserHandler(BaseHandler):
    def get(self, uuid):
        self.write(user_data.find_one({'uuid': uuid}))

    def post(self):
        #Creates a new user
        new_user = tornado.escape.json_decode(self.request.body)
        
        #Adds it to the database
        user_data.insert_one(new_user)

class DataHandler(BaseHandler):
    def post(self):
        #Create data dict
        data = tornado.escape.json_decode(self.request.body)

        #Write to DB - Needed for ML
        request_data.insert_one(data)

        #Find user from data
        user = user_data.find_one({'uuid': data['uuid']})

        '''
            The magic happens here
            Either math or ML, whatever
        '''

class ConfirmHandler(BaseHandler):
    def post(self):
        data = tornado.escape.json_decode(self.request.body)
