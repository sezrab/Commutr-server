import graph
from pathfinding import pathfinding
import random
import matplotlib.pyplot as plt

# print(root.find('node[@id="2437684359"]').attrib['id'])

aGraph = graph.Graph()

ways = list(aGraph.getWays().values())

nodes = []

for i in range(2):
    randWay = random.choice(ways)
    nodes.append(random.choice(randWay.getNodes()))

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

# print(route)

x = []
y = []

for node in route:
    lat,lon = node.getPos()
    x.append(lon)
    y.append(lat)

plt.plot(x,y,c='b')

plt.show()

# print(Node.fromID(2435710286).getNeighbours())