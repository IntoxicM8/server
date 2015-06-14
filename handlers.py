# Main file used for the endpoints
import tornado.web

from google.google_places import *

class BaseHandler(tornado.web.RequestHandler):
    pass

class UserHandler(BaseHandler):
    def get(self):
        self.write("fuckboi")

    def post(self):
        self.write("New User")


class DataHandler(BaseHandler):
    def post(self):
        self.write(GooglePlaces.get_nearest_general(43.6471642, -79.38705139999999))

class ConfirmHandler(BaseHandler):
    def post(self):
        self.write("Naren is gay")