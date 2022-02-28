from graph import pathfinding, graph, costs
import matplotlib.pyplot as plt

import gpxpy
import gpxpy.gpx

from lxml import etree as ET

from maps import api

from debugUtils import timer

from tests import angularDisplacement

visualise = True # option to visualise route & graph with matplotlib
gpx = True # option to export to gpx file
# offline = False

# points to find path between
ptA = (50.946227,-2.516823)
ptB = (51.024550,-2.532081)

# choose travel mode for pathfinding costs
print("\n--- Cost Maps ---")
count = 1
for key, costMap in costs.costMaps.items():
    print(str(count)+".", key)
    count += 1
print()
n = int(input("Cost map number: "))
chosenCost = list(costs.costMaps.values())[n-1]

print()

# run angular displacement test
angularDisplacement.test()

print()

# set up timers
tmr = timer()
totalTime = timer()


print("Getting data...")
q = api.lineQuery(ptA, ptB) # generate query
rawXML = api.request(q,True) # send query and process response
print("Received data\n")

print("Parsing...\n")
dtd = ET.DTD(open("osm.dtd")) # check validity of data
try: # parse xml using lxml library
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

print("Finished fetching data. Took", tmr, "seconds")

print()

print("Initialising Graph...")
# convert the xml object to a graph structure
aGraph = graph.Graph(root)

print("Initialised graph in", tmr, "seconds\n")

print("Finding terminal nodes...")

# from the graph, get the closest junction nodes to the given start and end coordinates
a = aGraph.getClosestNode(ptA)
b = aGraph.getClosestNode(ptB)

print("Found terminal nodes in", tmr, "seconds")

print()

print("Started pathfinding...")
print()

# perform A*
route = pathfinding.aStar(aGraph, aGraph.nodes[a], aGraph.nodes[b], chosenCost)
print("Calculated route in", tmr, "seconds")

# add non-junction nodes back in to the route
route = aGraph.redetail(route)

# remove excess nodes (nodes that are not between the start and end node) from redetailing
route = aGraph.trim(route, ptA, ptB)

print("Detailed route in", tmr, "seconds")
print("Total calculation time was", totalTime, "seconds")
print()

# define on-click event for matplotlib window
def onclick(event):
    # prints the coordinates of where we clicked on the graph
    ix, iy = event.xdata, event.ydata
    print("({},{})".format(iy, ix))

if visualise:
    # set up window
    fig = plt.figure()
    ax = fig.add_subplot(111)

    print("Plotting...")

    # for every way on the graph
    for way in aGraph.ways.values():    
        # create two seperate lists of the x coordinates and the y coordinates of all nodes on this way.
        x = []
        y = []
        for nodeID in way.nodeIDs:
            if nodeID in aGraph.junctionNodes:
                pos = aGraph.nodes[nodeID].position
                # plt.scatter(*pos[::-1], s=2)
                x.append(pos[1])
                y.append(pos[0])
        # plot the graph
        ax.plot(x, y)

    # create a list of the x coordinates and y coordiantes on the route 
    x = []
    y = []
    for node in route:
        lat, lon = node.position
        x.append(lon)
        y.append(lat)

    # plot the x list and the y list (plot the route)
    ax.plot(x, y, c='b')

    # register the on-click event
    cid = fig.canvas.mpl_connect('button_press_event', onclick)

    # show the window
    plt.show()

if gpx:
    # create gpx object
    gpxFile = gpxpy.gpx.GPX()

    # set up gpx object
    gpx_track = gpxpy.gpx.GPXTrack()
    gpxFile.tracks.append(gpx_track)
    gpx_segment = gpxpy.gpx.GPXTrackSegment()
    gpx_track.segments.append(gpx_segment)

    # append all coordinates to the gpx file
    for node in route:
        lat,lon = node.position
        gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(lat, lon))

    # export to standard gpx format xml
    xmlFile = gpxFile.to_xml()

    # save file
    try:
        print("Save route (CTRL+C to cancel)")
        with open('gpx\\'+input("route name: ")+".gpx", 'w') as f:
            f.write(xmlFile)
    except KeyboardInterrupt:
        print("Quitting...")
        exit()