import requests
import json

from google_utils import *

class GoogleRoads():

    BASE_URL = 'https://roads.googleapis.com/v1/'
    GOOGLE_API_KEY = 'AIzaSyCORAI3VeDDSkOJL-tb2H-9Uz4Z-nmW8NM'

    @staticmethod
    def get_nearest_road(lat, lng):
        url = '{0}snapToRoads'.format(GoogleRoads.BASE_URL)
        params = {
            'key' : GoogleRoads.GOOGLE_API_KEY,
            'path' : ','.join([str(lat), str(lng)])
        }
        point = json.loads(requests.get(url, params = params).content.decode())['snappedPoints'][0]
        distance = get_distance(lat, lng, point['location']['latitude'], point['location']['longitude'])
        return {
            'distance' : distance,
            'lat' : point['location']['latitude'],
            'lng' : point['location']['longitude']
        }