from graph import pathfinding, graph, costs
import matplotlib.pyplot as plt

import gpxpy
import gpxpy.gpx

from lxml import etree as ET

from maps import api

from debugUtils import timer

visualise = True
gpx = False
offline = False

ptA = (50.943136,-2.511581)
ptB = (50.987201,-2.539558)

print("\n--- Cost Maps ---")

count = 1
for key, costMap in costs.costMaps.items():
    print(str(count)+".", key)
    count += 1

print()

n = int(input("Cost map number: "))
chosenCost = list(costs.costMaps.values())[n-1]

print()

tmr = timer()
totalTime = timer()

print("Getting data...")

# print("Querying API")
q = api.lineQuery(ptA, ptB)
print(q)
rawXML = api.request(q,True)

print("Got data")
print("Parsing...")
dtd = ET.DTD(open("osm.dtd"))

try:
    root = ET.fromstring(rawXML)
    valid = dtd.validate(root)
    if valid:
        print("OSM data is VALID")
    else:
        print("! OSM data is INVALID")
        print(dtd.error_log.filter_from_errors())
        raise(ValueError)
except ValueError as e:
    print(rawXML[:500])
    print("...")
    print(rawXML[-500:])
    raise(e)

# if offline:
#     if os.path.exists('map.osm.xml'):
#         root = ET.parse('map.osm.xml')
#     else:
#         print("No downloaded data.")
# else:
#     # rawXML = api.multipleBboxRoadQuery(sherborne,yeovil)
#     print("Querying API")
#     rawXML = api.lineQuery(ptA,ptB)
#     try:
#         root = ET.fromstring(rawXML)
#     except ValueError as e:
#         print(rawXML[:500])
#         print("...")
#         print(rawXML[-500:])
#         raise(e)

print("Finished getting data. Took", tmr, "seconds")

print()

print("Initialising Graph...")
aGraph = graph.Graph(root)

print("Initialised graph in", tmr, "seconds")

print("Finding terminal nodes...")

# a,b = random.choices(aGraph.junctionNodes,k=2)
a = aGraph.getClosestNode(ptA)
b = aGraph.getClosestNode(ptB)

print("Got terminal junction nodes in", tmr, "seconds")

print()

print("Started pathfinding...")
print()
route = pathfinding.aStar(aGraph, aGraph.nodes[a], aGraph.nodes[b], chosenCost)

print("Calculated route in", tmr, "seconds")

route = aGraph.redetail(route)
route = aGraph.trim(route, ptA, ptB)
print("Detailed route in", tmr, "seconds")


print("Total calculation time was", totalTime, "seconds")

print()


def onclick(event):
    ix, iy = event.xdata, event.ydata
    print("({},{})".format(iy, ix))


if visualise:
    fig = plt.figure()
    ax = fig.add_subplot(111)

    print("Plotting...")

    for way in aGraph.ways.values():
        x = []
        y = []
        for nodeID in way.nodeIDs:
            if nodeID in aGraph.junctionNodes:
                pos = aGraph.nodes[nodeID].position
                # plt.scatter(*pos[::-1], s=2)
                x.append(pos[1])
                y.append(pos[0])

        ax.plot(x, y)

    x = []
    y = []

    for node in route:
        lat, lon = node.position
        x.append(lon)
        y.append(lat)

    ax.plot(x, y, c='b')

    # plt.show()

    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()

if gpx:
    gpxFile = gpxpy.gpx.GPX()

    # Create first track in our GPX:
    gpx_track = gpxpy.gpx.GPXTrack()
    gpxFile.tracks.append(gpx_track)

    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)
    for node in route:
        lat,lon = node.position
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(lat, lon))
    xmlFile = gpxFile.to_xml()
    print("Save file as")
    with open('gpx\\'+input("file name: gpx\\"), 'w') as f:
        f.write(xmlFile)