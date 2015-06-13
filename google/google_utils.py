from math import sin, cos, sqrt, atan2, radians, pi

def get_distance(user_lat, user_lng, lat, lng):
	radius = 6373000.0

	if user_lat != 0.0 or user_lng != 0.0 or lat != 0.0 or lng != 0.0:

		lng = radians(lng)
		lat = radians(lat)
		user_lng = radians(user_lng)
		user_lat = radians(user_lat)

		dlng = lng - user_lng
		dlat = lat - user_lat

		a = (sin(dlat / 2)) ** 2 + cos(lat) * cos(user_lat) * (sin(dlng / 2)) ** 2
		c = 2 * atan2(sqrt(a), sqrt(1 - a))

		return radius * c

	else:
		return "696969696.9"