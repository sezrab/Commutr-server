import math
from maps import utils
import clipboard

def run():
    sherborne = (50.948721, -2.509110)
    originalBearing = 90
    displaced = utils.displace(sherborne, 100000, originalBearing)

    newBearing = utils.bearing(sherborne, displaced)
    print(newBearing,originalBearing)
    accuracy = 100 * newBearing/originalBearing
    return accuracy >= 90