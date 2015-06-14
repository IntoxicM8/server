import math

GENDER_CONST = {'M': 0, 'F': 1}
TOLERANCE = {'H': 0, 'M': 1, 'L': 2}
PROXIMITIES = {'CLOSE': 4, 'CLOSETOOTHER': 2, 'FAR': 1}

def day_of_week(x):
	efunc = exp(-1*pow(x - 5.3, 2)/1.5)
	return 1+efunc

def gender_func(x):
	return x*0.2 + 1

def tolerance(x):
	return 0.8 + x*0.2

def bpm_percent(x):
	return 3/x - 2

def time_of_day(x):
    if -6 < x and x < 6:
        return math.exp(-1.0*x*x/20)*1.5
    return 0.1

def proximity_func_bar(x):
	return math.exp(-1.0*x*x/8192)*4

def proximity_func_nightclub(x):
	return math.exp(-1.0*x*x/8192)*4

def proximity_func_casino(x):
	return math.exp(-1.0*x*x/8192)*2

def age_func(x):
    if x < 12:
        return x/17
    elif 12 <= x and x <25
        return pow(x-12,1.7)/8.5 + 12/17
    else
        return -10*x/55 + 160/11
