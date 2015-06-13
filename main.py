import tornado.ioloop
import tornado.web

from handlers import *
from pymongo import MongoClient

application = tornado.web.Application([
	(r"/user/", UserHandler),
	(r"/data/", DataHandler),
	(r"/confirm/", ConfirmHandler),
])

client = MongoClient('mongodb://naren:wojtechnology@ds063140.mongolab.com:63140')
db = client['db']

users = db['users']
user_data = db['user_data']
locations = db['locations']

if __name__ == "__main__":
	application.listen(8888)
	tornado.ioloop.IOLoop.current().start()
