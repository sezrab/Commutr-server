from graph import pathfinding, graph, costs
import matplotlib.pyplot as plt

from lxml import etree as ET

from maps import api

import os
import random

from debugUtils import timer

visualise = True
offline =   False

# ptA = list(map(float, input("Point A: ").split(',')))
# ptB = list(map(float, input("Point B: ").split(',')))

ptA = (50.999929,-2.144443)
ptB = (50.939969,-2.533957)

print("\n--- Cost Maps ---")

count = 1
for key,costMap in costs.costMaps.items():
    print(str(count)+".",key)
    count += 1

print()

n = int(input("Cost map number: "))
chosenCost = list(costs.costMaps.values())[n-1]

print()

tmr = timer()
totalTime = timer()

print("Getting data...")

# print("Querying API")
rawXML = api.lineQuery(ptA,ptB)
try:
    root = ET.fromstring(rawXML)
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

print("Finished getting data. Took",tmr,"seconds")

print("\n"*2)

print("Initialising Graph...")
aGraph = graph.Graph(root)

print("Initialised graph in",tmr,"seconds")


print("Finding terminal nodes...")

# a,b = random.choices(aGraph.junctionNodes,k=2)
a = aGraph.getClosestNode(ptA)
b = aGraph.getClosestNode(ptB)

print("Got terminal nodes in",tmr,"seconds")

print("\n"*2)

print("Started pathfinding...")

route = pathfinding.aStar(aGraph,aGraph.nodes[a],aGraph.nodes[b],chosenCost)

print("Got route in",tmr,"seconds")
print("Total calculation time was",totalTime,"seconds")

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
