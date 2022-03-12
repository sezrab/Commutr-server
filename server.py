from tkinter import W
from flask import Flask, request
from graph import graph, costs
from graph import pathfinding
from lxml import etree as ET
from maps import api
import json

app = Flask(__name__)

@app.route('/route', methods=['POST'])
def result():
    print("[+] New request")
    try:
        # split the passed coordinates into the seperate lat and lon components
        aLat,aLon = request.form['a'].split(",")
        print(" * Received a")
        bLat,bLon = request.form['b'].split(",")
        print(" * Received b")
        
        # get the mode of transport
        mode = request.form['mode']
        print(" * Received mode")

    except Exception as e:
        # unexpected error
        print(e) # log for future debugging
        print("[X] Invalid arguments")

        # explain the issue to the user and return appropriate response code
        return "Error: Invalid arguments", 400 
    try:
        # try to map the given mode of transport to a cost dict
        costMap = costs.costMaps[mode]
        print("   * Got cost map")
    except:
        # the mode of transport doesn't exist
        print("[X] Cost map mode does not exist")
        return "Error: No such transport mode", 400 # explain to the user

    # convert coordinates to two tuples of floats
    aPos = (float(aLat),float(aLon))
    bPos = (float(bLat),float(bLon))

    print()

    try:
        # generate line query
        lineQuery = api.lineQuery(aPos,bPos);
        # execute query & parse result
        root = ET.fromstring(api.request(api.lineQuery(aPos,bPos)))
    except:
        print("[X] Line query generation error // XML parse error")
        print("generated query:")
        print(lineQuery)
        return "Internal server error with query", 500
    
    print(" * Parsed XML")

    # initialise graph for pathfinding
    try:
        g = graph.Graph(root)
    except:
        print("[X] graph failed")
        return "Internal server error with graph initialisation", 500

    print(" * Processed graph")
    print()

    # convert the start & end coordinates to the nearest junction nodes on the graph
    try:
        aNode = g.nodes[g.getClosestNode(aPos)]
        bNode = g.nodes[g.getClosestNode(bPos)]
    except:
        print("[X] terminal nodes failed")
        return "Internal server error with locating terminal nodes", 500

    print(" * Got terminal nodes")

    # do pathfinding
    print(" * Finding shortest path")
    try:
        # create route
        route = pathfinding.aStar(g,aNode,bNode,costMap)
        if route == None:
            # route failed but no error, therefore bad data. (give code 400 bad request)
            print("[X] No path between these points")
            return "Error: No path between these points", 400
        
        # add back in the detailed removed for pathfinding
        route = g.redetail(route)
        
        # trim the route to the start & end nodes (remove extra that goes towards nearest junction)
        route = g.trim(route, aPos, bPos)
    except Exception as e:
        print("[X] Unexpected error finding path:",e)
        return "Error: Something went wrong while finding path", 500 # internal server error?
    print(" * Found shortest path")

    # convert nodes to list of route vertices
    route = [node.position for node in route]
    
    # convert list to json
    jsonDat = {"route":route}

    print("\n+ Request complete\n")

    # return json, success code 200
    return json.dumps(jsonDat), 200 # successful response

app.run(host='0.0.0.0', port=80)
