from maps.utils import bBox, displace
from tests import displacementBearing, bbox
import clipboard

bbQuery = bbox.run()
clipboard.copy(bbQuery)

results = {
    'displacement & bearings': displacementBearing.run(),
}

for test in results.keys():
    print(test, "-", results[test])