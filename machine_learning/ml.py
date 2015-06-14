import json
from pymongo import *

from sklearn import svm

class Learn():

	TRAINED_DATA = 'data.json'

	def __init__(self, uuid, request_data):
		self.uuid = uuid
		self.request_data = request_data

	def train_data(self):
		pass

	def predict(self, data_point):
		pass

	def get_user_data(self):
		if self.request_data.count({'uuid' : self.uuid}) == 0:
			return []
		obj = self.request_data.find({'uuid' : self.uuid})[0]
		params = [
			obj['weekday'],
			obj['gender'],
			obj['tol'],
			obj['bpm'],
			obj['hour'],
			obj['prox_bar'],
			obj['prox_night'],
			obj['prox_casino'],
			obj['prox_danger'],
			obj['age']
		]
		return [obj['rating'], params]

	def get_default_data(self):
		f = open(Learn.TRAINED_DATA, 'r')
		obj = json.loads(f.read())
		return obj

db = MongoClient('ds063140.mongolab.com', 63140)['database']
db.authenticate("naren", "wojtechnology")
learn = Learn(1338, db['request_data'])
#print learn.get_default_data()
print learn.get_default_data()
print learn.get_user_data()