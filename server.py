from flask import Flask, request
from graph import graph, costs
from graph import pathfinding
import matplotlib.pyplot as plt
from lxml import etree as ET
from maps import api
import json

from maps.utils import haversine


app = Flask(__name__)

# @app.route('/', methods=['POST','GET'])
# def index():
#     return "Hello, World!"

@app.route('/route', methods=['POST'])
def result():
    print()
    print("+ New request")
    try:
        aLat,aLon = request.form['a'].split(",")
        print(" * Received a")
        bLat,bLon = request.form['b'].split(",")
        print(" * Received b")
        mode = request.form['mode']
        print(" * Received mode")
    except Exception as e:
        print(e)
        print("[X] Invalid arguments")
        return "Error: Invalid arguments"
    try:
        costMap = costs.costMaps[mode]
        print("   * Got cost map")
    except:
        print("[X] Cost map mode does not exist")
        return "Error: No such transport mode", 400 # bad request

    aPos = (float(aLat),float(aLon))
    bPos = (float(bLat),float(bLon))
    print()
    try:
        lq = api.lineQuery(aPos,bPos);
        root = ET.fromstring(api.request(api.lineQuery(aPos,bPos)))
    except:
        print(lq)
    print(" * Parsed XML")

    g = graph.Graph(root)
    print(" * Processed graph")
    print()
    aNode = g.nodes[g.getClosestNode(aPos)]
    bNode = g.nodes[g.getClosestNode(bPos)]
    print(" * Got terminal nodes")

    print(" * Finding shortest path")
    try:
        route = pathfinding.aStar(g,aNode,bNode,costMap)
        if route == None:
            print("[X] No path between these points")
            return "Error: No path between these points", 400
        route = g.redetail(route)
        route = g.trim(route, aPos, bPos)
    except Exception as e:
        print("[X] Unexpected error finding path:",e)
        return "Error: Something went wrong while finding path", 500 # internal server error?
    print(" * Found shortest path")

    route = [node.position for node in route]
    
    jsonDat = {"route":route}

    print("\n+ Request complete\n")

    return json.dumps(jsonDat), 200 # successful response

app.run(host='0.0.0.0', port=80)
