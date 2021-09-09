from graph import pathfinding, graph

import matplotlib.pyplot as plt

from lxml import etree as ET
from maps import api

import os
import random

visualise = True
offline = True

sherborne = (50.950340,-2.520400) # lat, lon

print("Getting data...")

if offline:
    if os.path.exists('map.osm.xml'):    
        root = ET.parse('map.osm.xml')
    else:
        print("No downloaded data.")
else:
    root = ET.fromstring(api.roadQuery(sherborne,2))

aGraph = graph.Graph(root)

print("Choosing two random points...")
ways = list(aGraph.getWays().values())

nodes = []

for i in range(2):
    randWay = random.choice(ways)
    nodes.append(random.choice(randWay.getNodes()))

if visualise:
    print("Getting data ready for plot...")
    for way in aGraph.getWays().values():
        x = []
        y = []
        for node in way.getNodes():
            lat,lon = node.getPos()
            x.append(lon)
            y.append(lat)
        plt.plot(x,y,c='r')

print("Started pathfinding...")

route = aGraph.buildRouteFromJunctions(pathfinding.astar(aGraph,nodes[0],nodes[1]))

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
