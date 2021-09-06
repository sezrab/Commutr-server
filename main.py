import graph
from pathfinding import pathfinding
import random
import matplotlib.pyplot as plt
from lxml import etree as ET
from map import api

sherborne = (50.950340,-2.520400) # lat, lon
print("Getting data...")
root = ET.fromstring(api.roadQuery(sherborne,2))
# root = ET.parse('map.osm.xml')
aGraph = graph.Graph(root)

print("Choosing two random points...")
ways = list(aGraph.getWays().values())

nodes = []

for i in range(2):
    randWay = random.choice(ways)
    nodes.append(random.choice(randWay.getNodes()))

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

route = pathfinding.astar(aGraph,nodes[0],nodes[1])

print("Plotting...")

x = []
y = []

for node in route:
    lat,lon = node.getPos()
    x.append(lon)
    y.append(lat)

plt.plot(x,y,c='b')

plt.show()
