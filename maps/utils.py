from math import cos, sin, asin, radians, pi, degrees, atan2, sqrt, acos
from sys import base_exec_prefix
from . import constants

# create a method that will make d/r square bboxes on a straight line

def bBoxSquare(centre,side):
    """Create a square bounding box in the format latitude (southmost), longitude (westmost), latitude (northmost), longitude (eastmost)

    Args:
        centre (tuple): Centre of the square
        side (float): Side length of the square

    Returns:
        list [lat,lon,lat,lon]
    """
    r = side/2
    north = displace(centre, r, 0)
    east = displace(centre, r, 90)
    south = displace(centre, r, 180)
    west = displace(centre, r, 270)
    return south[0],west[1],north[0],east[1]

def haversine(a, b):
    """Determines the great-circle distance between two GPS points
    https://en.wikipedia.org/wiki/Haversine_formula

    Args:
        a (tuple): (lat,lon) 
        b (tuple): (lat,lon)

    Returns:
        float: distance
    """

    # decimal degrees to radians
    lat1, long1, lat2, long2 = map(radians, [a[0], a[1], b[0], b[1]])
    
    # get difference between latitudes and longitudes of a and b, 
    dlon = long2 - long1
    dlat = lat2 - lat1
    
    # use haversine formula
    a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    d = c * constants.earthRadius

    return d

# def displace(latlon, distance, bearing):
#     '''
#     https://gis.stackexchange.com/a/30037
#     Approximately displaces a lat,lon coordinate by a distance (meters), by a bearing (east from north)
#     '''

#     lat,lon = latlon

#     latitudeDegreeConstant = (10**7) / 90

#     # lat,lon = latlon
#     north = distance * sin(radians(bearing)) / latitudeDegreeConstant
#     east = distance * cos(radians(bearing)) / sin(radians(lat)) / latitudeDegreeConstant
#     return lat+east, lon+north

def displace(latlon, distance, bearing):
    """Displace a lat,lon point by a distance due to a given angle
    See test @ tests/angularDisplacement.py

    Args:
        latlon (tuple): Point to displace
        distance (float): Distance to displace by (m)
        bearing (float): Bearing to displace by (degrees)

    Returns:
        tuple: The displaced point
    """
    lat1,lon1 = map(radians,latlon)
    bearing = radians(bearing)
    lat2 = asin(sin(lat1)*cos(distance/constants.earthRadius) +
        cos(lat1)*sin(distance/constants.earthRadius)*cos(bearing))

    lon2 = lon1 + atan2(sin(bearing)*sin(distance/constants.earthRadius)*cos(lat1),
                cos(distance/constants.earthRadius)-sin(lat1)*sin(lat2))

    lat2 = degrees(lat2)
    lon2 = degrees(lon2)

    return lat2,lon2

# def bearing(a,b):
#     '''
#     http://www.edwilliams.org/avform147.htm#Crs
#     From Ed William's aviation formula: course between points
#     formula 2
#     '''
#     lat1,lon1 = map(radians,a)
#     lat2,lon2 = map(radians,b)
#     d = haversine(a,b)
#     if sin(lon2-lon1)<0:
#         tc1=acos((sin(lat2)-sin(lat1)*cos(d))/(sin(d)*cos(lat1)))    
#     else:       
#         tc1=2*pi-acos((sin(lat2)-sin(lat1)*cos(d))/(sin(d)*cos(lat1)))
#     return tc1

# def bearing(a,b):
#     '''
#     http://www.edwilliams.org/avform147.htm#Crs
#     From Ed William's aviation formula: course between points
#     formula 3
#     '''
#     lat1,lon1 = map(radians,a)
#     lat2,lon2 = map(radians,b)
#     tc1 = (atan2(sin(lon1-lon2)*cos(lat2),
#            cos(lat1)*sin(lat2)-sin(lat1)*cos(lat2)*cos(lon1-lon2)) % 2*pi)
#     return tc1

def bearing(a,b):
    """Measures the bearing between two points
    See test @ tests/angularDisplacement.py

    https://stackoverflow.com/a/18738281
    
    Args:
        a (tuple): First point (lat,lon)
        b (tuple): Second point (lat,lon)

    Returns:
        float: Bearing (degrees)
    """
    
    lat1, lon1 = map(radians,a)
    lat2, lon2 = map(radians,b)

    dLon = (lon2 - lon1)

    y = sin(dLon) * cos(lat2)
    x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dLon)

    bearing = atan2(y, x)

    bearing = degrees(bearing)
    bearing = (bearing + 360) % 360

    return bearing
