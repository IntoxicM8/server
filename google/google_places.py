import requests
import json

class GooglePlaces():

    BASE_URL = 'https://maps.googleapis.com/maps/api/place/'
    GOOGLE_API_KEY = 'AIzaSyCORAI3VeDDSkOJL-tb2H-9Uz4Z-nmW8NM'

    @staticmethod
    def get_nearest_general(lat, lng):
        url = "{0}nearbysearch/json".format(GooglePlaces.BASE_URL)
        types = [
            'amusement_park',
            'bakery',
            'bar',
            'bowling_alley',
            'bus_station',
            'cafe',
            'campground',
            'casino',
            'cemetery',
            'establishment',
            'food',
            'gas_station',
            'grocery_or_supermarket',
            'gym',
            'health',
            'liquor_store',
            'meal_delivery',
            'meal_takeaway',
            'movie_theater',
            'museum',
            'night_club',
            'park',
            'parking',
            'police',
            'restaurant',
            'rv_park',
            'school',
            'shopping_mall',
            'stadium',
            'subway_station',
            'university'
        ]
        params = {
            'key' : GooglePlaces.GOOGLE_API_KEY,
            'location' : '{0},{1}'.format(lat, lng),
            'rankby' : 'distance',
            'types' : '|'.join(types)
            }
        results = json.loads(requests.get(url, params = params).content.decode())['results']

        places = []
        for result in results:
            place = {
                'place_id' : result['place_id'],
                'name' : result['name'],
                'types' : result['types'],
                'lat' : result['geometry']['location']['lat'],
                'lng' : result['geometry']['location']['lng']
                }
            if (result.has_key("opening_hours")):
                place['open_now'] = result['opening_hours']['open_now']

            places.append(place)

        return places

    @staticmethod
    def get_high_priority(lat, lng):
        url = "{0}nearbysearch/json".format(GooglePlaces.BASE_URL)
        types = [
            'bar',
            'casino',
            'night_club',
        ]
        params = {
            'key' : GooglePlaces.GOOGLE_API_KEY,
            'location' : '{0},{1}'.format(lat, lng),
            'rankby' : 'distance',
            'types' : '|'.join(types)
            }
        results = json.loads(requests.get(url, params = params).content.decode())['results']

        places = []
        for result in results:
            place = {
                'place_id' : result['place_id'],
                'name' : result['name'],
                'types' : result['types'],
                'lat' : result['geometry']['location']['lat'],
                'lng' : result['geometry']['location']['lng']
                }
            if (result.has_key("opening_hours")):
                place['open_now'] = result['opening_hours']['open_now']

            places.append(place)

        return places