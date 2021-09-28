from graph import pathfinding, graph
import matplotlib.pyplot as plt

from lxml import etree as ET

from maps import api

import os
import random

from debugUtils import timer

visualise = False
offline = False

sherborne = (50.950340,-2.520400) # lat, lon
yeovil = (50.943647,-2.647176)

tmr = timer()

print("Getting data...")

if offline:
    if os.path.exists('map.osm.xml'):    
        root = ET.parse('map.osm.xml')
    else:
        print("No downloaded data.")
else:
    # rawXML = api.multipleBboxRoadQuery(sherborne,yeovil)
    print("Querying API")
    rawXML = api.lineQuery(sherborne,yeovil)
    try:
        root = ET.fromstring(rawXML)
    except ValueError as e:
        print(rawXML[:500])
        print("...")
        print(rawXML[-500:])
        raise(e)

print("Finished getting data. Took",tmr,"seconds")

aGraph = graph.Graph(root)

print("Choosing two random points...")
ways = list(aGraph.getWays().values())

nodes = []

for i in range(2):
    randWay = random.choice(ways)
    nodes.append(random.choice(randWay.getNodes()))

if visualise:
    tmr.reset()
    print("Getting data ready for plot...")
    for way in aGraph.getWays().values():
        x = []
        y = []
        for node in way.getNodes():
            lat,lon = node.getPos()
            x.append(lon)
            y.append(lat)
        plt.plot(x,y,c='r')
    print("Took",tmr,"seconds")

tmr.reset()

print("Started pathfinding...")

route = aGraph.buildRouteFromJunctions(pathfinding.astar(aGraph,nodes[0],nodes[1]))

print("Got route in",tmr,"seconds")

if visualise:
    print("Plotting...")

    x = []
    y = []

    for node in route:
        lat,lon = node.getPos()
        x.append(lon)
        y.append(lat)

    plt.plot(x,y,c='b')

    plt.show()
