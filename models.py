import const
from pymongo import MongoClient

client = MongoClient(const.MONGO_URL)

user_data = db['user_data']
request_data = db['request_data']