from math import cos, sin, asin, radians, pi, degrees, atan2, sqrt, acos
from sys import base_exec_prefix
from . import constants

# create a method that will make d/r square bboxes on a straight line

def bBoxSquare(centre,side):
    r = side/2
    north = displace(centre, r, 0)
    east = displace(centre, r, 90)
    south = displace(centre, r, 180)
    west = displace(centre, r, 270)
    return south[0],west[1],north[0],east[1]

def bBox(start,end,width):
    # something is not working
    lat1,lon1 = start
    lat2,lon2 = end

    maxLat = max(lat1,lat2)
    minLat = min(lat1,lat2)

    maxLon = max(lon1,lon2)
    minLon = min(lon1,lon2)

    meanLat = (maxLat+minLat)/2
    meanLon = (maxLon+minLon)/2

    print("Max min lat:",maxLat,minLat)
    print("Max min lon:",minLon,maxLon)

    horizontalDistance = haversine((maxLat,meanLon),(minLat,meanLon))
    verticalDistance = haversine((meanLat,minLon),(meanLat,maxLon))

    print(horizontalDistance,verticalDistance)

    if horizontalDistance > verticalDistance:
        north = displace((meanLat,maxLon),2000,0)[1]
        south = displace((meanLat,minLon),2000,180)[1]
        east = maxLat
        west = minLat
    else:
        east = displace((maxLat,meanLon),2000,90)[0]
        west = displace((minLon,meanLon),2000,270)[0]
        north = maxLon
        south = minLon

    # there is not much documentation for this,
    # but it should follow the format
    # left,bottom,right,top
    
    return west,south,east,north

def haversine(a, b):
    '''
    determines the great-circle distance between two GPS points
    https://en.wikipedia.org/wiki/Haversine_formula
    '''
    lat1, long1, lat2, long2 = map(radians, [a[0], a[1], b[0], b[1]])
    
    dlon = long2 - long1
    dlat = lat2 - lat1
    
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
    '''
    from https://stackoverflow.com/a/18738281
    '''

    lat1, lon1 = map(radians,a)
    lat2, lon2 = map(radians,b)

    dLon = (lon2 - lon1);

    y = sin(dLon) * cos(lat2);
    x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(dLon);

    bearing = atan2(y, x);

    bearing = degrees(bearing);
    bearing = (bearing + 360) % 360;

    return bearing;
