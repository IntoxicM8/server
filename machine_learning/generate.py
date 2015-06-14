import json

from random import *
from equation import *

def generate(iters):
	data = []
	for i in range(iters):
		thing = rnJesus()
		y = -1
		if thing[0] < 30:
			y = 0
		elif thing[0] < 70:
			y = 1
		else:
			y = 2

		thing[0] = y
		data.append(thing)

	return data

def rnJesus():
	dow = randint(0, 6)
	gender = randint(0, 1)
	tol = random() * 2.0
	bpm = random() + 0.5
	tod = random() * 24
	prox_bar = random() * 1000
	prox_night = random() * 2000
	prox_casino = random() * 4000
	prox_danger = random() * 4000
	count = randint(0, 10)
	age = randint(14, 70)
	multipliers = []
	multipliers.append(day_of_week(dow))
	multipliers.append(gender_func(gender))
	multipliers.append(tolerance(tol))
	multipliers.append(bpm_percent(bpm))
	multipliers.append(time_of_day(tod))
	multipliers.append(proximity_func_bar(prox_bar))
	multipliers.append(proximity_func_nightclub(prox_night))
	multipliers.append(proximity_func_casino(prox_casino))
	multipliers.append(proximity_func_danger(prox_danger, count))
	multipliers.append(age_func(age))

	product = 1
	for mult in multipliers:
		product *= mult
	
	return [product, [dow, gender, tol, bpm, tod, prox_bar, prox_night, prox_casino, prox_danger, count, age]]

def save():
	f = open('data.json', 'w')
	f.write(json.dumps(generate(10000)))

save()