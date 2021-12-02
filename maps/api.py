from requests.models import Response
from maps import utils
import requests
from math import ceil
from . import constants

# TODO: clean up and make names clearer

def radiusQuery(center,radius):
    # center is a tuple of format (lat,lon)
    # radius is a float in meters

    lat,lon = center
    return request(constants.roadQuery.format(radius*1000,lat,lon,))

def lineQueryString(bboxes):
    # bboxes is a 2D list, where second dimensional lists are in the format [southMostLat,westMostLon,northMostLat,eastMostLon]
    
    queries = [constants.wayQueryLine.format(*bbox) for bbox in bboxes]
    return constants.blankRoadQuery.format("\n".join(queries))

def lineQuery(a,b):
    distance = utils.haversine(a,b)
    bearing = utils.bearing(a,b)

    squareSide = max(distance/10,2000)
    nSquares = ceil(distance/squareSide)

    squareBboxes = []

    previousCentre = a
    for i in range(nSquares):
        newCentre = utils.displace(previousCentre,squareSide,bearing)
        previousCentre = newCentre
        squareBboxes.append(utils.bBoxSquare(newCentre,squareSide))

    return lineQueryString(squareBboxes)

# constants.apiURL: "http://overpass-api.de/api/interpreter"
def request(query, verbose=False, attempts=0):
    try:
        response = requests.get(constants.apiURL, params={'data': query})
        return response.text.encode()
    except requests.exceptions.Timeout:
        if verbose:
            print("Timeout error")
        if attempts < 3:
            if verbose:
                print("Retrying request (attempt {}/{})".format(attempts+1,constants.allowedRetries))
            return request(query,verbose,attempts+1)
        else:
            response.raise_for_status()
    except requests.exceptions.TooManyRedirects as e:
        raise SystemExit("Too many redirects for URL: " + constants.apiURL)
    except requests.exceptions.ConnectionError:
        raise SystemExit("Connection error: do you have internet access?")
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)