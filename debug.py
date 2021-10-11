from sys import path
from graph import graph
from lxml import etree as ET
import matplotlib.pyplot as plt
from graph import pathfinding

root = ET.parse('map.osm.xml')
g = graph.Graph(root)

way = g.ways["145071574"]

node = g.nodes["939851692"]

nbours = g.getNeighbouringNodes(node)

print()

print("neighbour count:",len(nbours))

# for n in g.getNeighbouringNodes(node):
#     print(n)

plt.show()