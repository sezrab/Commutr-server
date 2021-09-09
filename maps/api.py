import requests
from . import constants

def roadQuery(center,radius):
    lat,long = center
    return request(constants.roadQuery.format(radius*1000,lat,long)).encode()

def request(query):
    return requests.get(constants.apiURL, params={'data': query}).text
