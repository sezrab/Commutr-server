from maps import utils
import requests
from math import ceil
from . import constants

def radiusQuery(center,radius):
    lat,lon = center
    return request(constants.roadQuery.format(radius*1000,lat,lon,))

def lineQueryString(bboxes):
    queries = []
    for bbox in bboxes:
        queries.append(constants.wayQueryLine.format(*bbox))

    return constants.blankRoadQuery.format("\n".join(queries))

def lineQuery(a,b):
    distance = utils.haversine(a,b)
    bearing = utils.bearing(a,b)

    squareSide = 2000
    nSquares = ceil(distance/squareSide)

    squareBboxes = []

    previousCentre = a
    for i in range(nSquares):
        newCentre = utils.displace(previousCentre,squareSide,bearing)
        previousCentre = newCentre
        squareBboxes.append(utils.bBoxSquare(newCentre,squareSide))

    return request(lineQueryString(squareBboxes))

def request(query):
    return requests.get(constants.apiURL, params={'data': query}).text.encode()
