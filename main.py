from graph import pathfinding, graph
import matplotlib.pyplot as plt

from lxml import etree as ET

from maps import api

import os
import random

from debugUtils import timer

visualise = True
offline = True

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

a,b = random.choices(aGraph.junctionNodes,k=2)

# print(len(aGraph.getNeighbouringNodes(aGraph.nodes[a])))

# input("paused")

if visualise:
    tmr.reset()
    print("Getting data ready for plot...")
    for way in aGraph.ways.values():
        x = []
        y = []
        for nodeID in way.nodeIDs:
            lat,lon = aGraph.nodes[nodeID].position
            x.append(lon)
            y.append(lat)
        plt.plot(x,y,c='r')
    print("Took",tmr,"seconds")

tmr.reset()

print("Started pathfinding...")

# route = aGraph.buildRouteFromJunctions(pathfinding.astar(aGraph,nodes[0],nodes[1]))

route = pathfinding.astar(aGraph,aGraph.nodes[a],aGraph.nodes[b])

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
