from graph import pathfinding, graph
import matplotlib.pyplot as plt

from lxml import etree as ET

from maps import api

import os
import random

from debugUtils import timer

visualise = True
offline =   False

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
    rawXML = api.radiusQuery(yeovil,2)
    try:
        root = ET.fromstring(rawXML)
    except ValueError as e:
        print(rawXML[:500])
        print("...")
        print(rawXML[-500:])
        raise(e)

print("Finished getting data. Took",tmr,"seconds")

print("\n"*2)

aGraph = graph.Graph(root)

while True:

    print("Choosing two random points...")

    a,b = random.choices(aGraph.junctionNodes,k=2)

    # a = '939851691'

    # print(len(aGraph.getNeighbouringNodes(aGraph.nodes[a])))

    # input("paused")

    print("\n"*2)

    tmr.reset()

    print("Started pathfinding...")

    # route = aGraph.buildRouteFromJunctions(pathfinding.astar(aGraph,nodes[0],nodes[1]))

    route = pathfinding.aStar(aGraph,aGraph.nodes[a],aGraph.nodes[b])

    print("Got route in",tmr,"seconds")

    print("\n"*2)

    for way in aGraph.ways.values():
        x = []
        y = []
        for nodeID in way.nodeIDs:
            if nodeID in aGraph.junctionNodes:
                pos = aGraph.nodes[nodeID].position
                # plt.scatter(*pos[::-1], s=2)
                x.append(pos[1])
                y.append(pos[0])
        plt.plot(x,y)

    # plt.scatter(*aGraph.nodes[a].position[::-1],s=100)

    # for nb in aGraph.getNeighbouringNodes(aGraph.nodes[a]):
        # plt.scatter(*nb.position[::-1],s=50)

    # plt.savefig('nodesEdges.png')
    # plt.show()

    # quit()

    if visualise:
        print("Plotting...")

        x = []
        y = []

        for node in route:
            lat,lon = node.position
            x.append(lon)
            y.append(lat)

        plt.plot(x,y,c='b')

        plt.show()
