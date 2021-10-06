from sys import path
from graph import graph
from lxml import etree as ET
import random

from graph import pathfinding

root = ET.parse('map.osm.xml')
g = graph.Graph(root)

randJunc = g.nodes[random.choice(g.junctionNodes)]

print(randJunc.id)
print("Has neighbours:")
print(g.getNeighbouringNodes(randJunc))

print(g.ways[g.junctions[randJunc.id][0]].wayType)

print("testing pathfinding")

pathfinding.astar(g,randJunc,g.nodes[random.choice(g.junctionNodes)])