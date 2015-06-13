# Main file used for the endpoints
import tornado.web

class BaseHandler(tornado.web.RequestHandler):
	pass

class UserHandler(BaseHandler):
	def get(self, uuid):
		self.write(self.users.find_one({'uuid': uuid}))

	def post(self):
		#Creates a new user
		new_user = tornado.escape.json_decode(self.request.body)
		
		#Adds it to the database
		self.users.insert_one(new_user)

class DataHandler(BaseHandler):
	def post(self):
		#Create data dict
		data = tornado.escape.json_decode(self.request.body)

		#Write to DB - Needed for ML
		self.request_data.insert_one(data)

		#Find user from data
		user = self.users.find_one({'uuid': data['uuid']})

		'''
			The magic happens here
			Either math or ML, whatever
		'''

class ConfirmHandler(BaseHandler):
	def post(self):
		correct = self.get_argument('correct')
