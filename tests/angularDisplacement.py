from ast import ExtSlice
from traceback import print_tb
from maps import utils

def test():
    sherborne = (50.948721, -2.509110)

    displacementBearing = 90
    
    displacedCoordinates = utils.displace(sherborne, 100000, displacementBearing)

    measuredBearing = utils.bearing(sherborne, displacedCoordinates)

    accuracy = 100 * measuredBearing/displacementBearing
    
    if accuracy >= 90:
        print("Angular dispalcement test passed")
    else:
        raise("Angular displacement test failed")
    
    print("Accuracy was {:.3f}%".format(accuracy))