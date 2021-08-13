import requests
from constants import *

class queries(object):
    @staticmethod
    def getSurroundingWays(condition,radius,lat,long):
        return """
[out:json][timeout:25];
(
way[{}](around:{},{},{});
);
out ids tags geom;""".format(condition,radius,lat,long)

def doQuery(query):
    response = requests.get(overpass_url, params={'data': query})
    try:
        return response.json()["elements"]
    except:
        raise(Exception(response.text))