import math

def day_of_week(x):
	efunc = math.exp(-1*pow(x - 5.3, 2)/1.5)
	return 1+efunc

def gender_func(x):
	return x*0.2 + 1

def tolerance(x):
	return 0.8 + x*0.2

def bpm_percent(x):
	return 3/x - 2

def time_of_day(x):
    if x > 12:
        x = x - 24
    if -6 < x and x < 6:
        return math.exp(-1.0*x*x/20)*1.5 + 1
    return 1

def proximity_func_bar(x):
	return math.exp(-1.0*x*x/8192)*4 + 1

def proximity_func_nightclub(x):
	return math.exp(-1.0*x*x/8192)*4 + 1

def proximity_func_casino(x):
	return math.exp(-1.0*x*x/8192)*2 + 1

def proximity_func_danger(x, count):
    if count < 1:
        return 1
    multiplier = ((-1)/x+2)/2
    return math.exp(-1.0*x*x/8192)*4 * multiplier + 1

def age_func(x):
    if x < 12:
        return x/17
    elif x < 25:
        return pow(x-12,1.7)/8.5 + 12/17
    elif x < 65:
        return -10*x/55 + 160/11
    else:
        return 1

