from flask import Flask, request
from graph import graph, costs
from graph import pathfinding
import matplotlib.pyplot as plt
from lxml import etree as ET
from math import inf
from maps import api
import json

from maps.utils import haversine


app = Flask(__name__)

# @app.route('/', methods=['POST','GET'])
# def index():
#     return "Hello, World!"

@app.route('/', methods=['POST','GET'])
def result():
    aLat = request.form['aLat']
    aLon = request.form['aLon']
    bLat = request.form['bLat']
    bLon = request.form['bLon']

    mode = request.form['mode']
    costMap = costs.costMaps[mode]

    a = (float(aLat),float(aLon))
    b = (float(bLat),float(bLon))
    root = ET.fromstring(api.lineQuery(a,b))

    g = graph.Graph(root)

    a = g.getClosestNode(a)
    b = g.getClosestNode(b)

    # closestA = None
    # distanceA = inf
    # closestB = None
    # distanceB = inf

    # get closest nodes to a and b
    # for junctionNodeID in g.junctionNodes:
    #     jNode = g.nodes[junctionNodeID]
    #     thisADistance = haversine(jNode.position, a)
    #     thisBDistance = haversine(jNode.position, b)
    #     if thisADistance < distanceA:
    #         closestA = jNode
    #         distanceA = thisADistance
    #     if thisBDistance < distanceB:
    #         closestB = jNode
    #         distanceB = thisBDistance

    route = pathfinding.aStar(g,a,b,costMap)
    route = [node.position for node in route]
    
    jsonDat = {"route":route}

    return json.dumps(jsonDat)

app.run(host='0.0.0.0', port=80)
