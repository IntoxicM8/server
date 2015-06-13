import tornado.ioloop
import tornado.web
import const

from handlers import *
from pymongo import MongoClient

application = tornado.web.Application([
	(r"/users/([a-z0-9\-]+)/?", UserHandler),
	(r"/data/?", DataHandler),
	(r"/confirms/?", ConfirmHandler),
])

client = MongoClient(const.MONGO_URL)
db = client['db']

if __name__ == "__main__":
	application.users = db['users']
	application.user_data = db['user_data']
	application.request_data = db['request_data']
	application.locations = db['locations']
	application.listen(8888)
	tornado.ioloop.IOLoop.current().start()
