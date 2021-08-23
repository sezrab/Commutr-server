from math import cos, radians

from . import constants

def boundingBox(center,radius):
    x,y = center
    dY = radius / constants.earthRadius
    dX = dY * cos(radians(y))

    # left bottom right top
    return [x - dX, y - dY, x + dX, y + dY]

