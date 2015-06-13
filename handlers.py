# Main file used for the endpoints
import tornado.web

class BaseHandler(tornado.web.RequestHandler):
	pass

class UserHandler(BaseHandler):
	def get(self):
		self.write("fuckboi")

	def post(self):
		self.write("New User")


class DataHandler(BaseHandler):
	def post(self):
		self.write("Penis")

class ConfirmHandler(BaseHandler):
	def post(self):
		self.write("Naren is gay")


