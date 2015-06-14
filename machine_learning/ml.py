import json
from pymongo import *
import numpy as np
from sklearn import svm

class Learn():

	TRAINED_DATA = 'data.json'

	def __init__(self, uuid, request_data, trained_data):
		self.uuid = uuid
		self.request_data = request_data
		self.trained_data = trained_data

	def train_data(self):
		data = self.get_user_data()
		x = []
		y = []
		for dat in data:
			y.append(dat[0])
			x.append(dat[1])

		clf = svm.SVC()
		clf.fit(x, y) 

		for i in range(len(data)):
			print str(y[i]) + ': ' + str(clf.predict(x[i]))

	def predict(self, data_point):
		return clf.predict(data_point)

	def get_user_data(self):
		objs = self.request_data.find({'uuid' : self.uuid})
		data = self.get_default_data()
		for obj in objs:
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
				obj['count'],
				obj['age']
			]
			data.append([obj['rating'], params])

		return data

	def get_default_data(self):
		f = open(Learn.TRAINED_DATA, 'r')
		obj = json.loads(f.read())
		return obj

'''db = MongoClient('ds063140.mongolab.com', 63140)['database']
db.authenticate("naren", "wojtechnology")
learn = Learn(1338, db['request_data'])
learn.train_data()'''