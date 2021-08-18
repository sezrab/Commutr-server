from time import time
import json
from utils import haversine, timer
from overpass import *
from clipboard import copy
import matplotlib.pyplot as plt
import astar
from graph import *

def aquire(radius,lat,lon):
    """
    Query all raw osm highway data for a radius around of a lat/lon point
    """
    print("Acquiring data...")
    t = timer()

    data = doQuery(queries.getSurroundingWays("highway",radius*1000,lat,lon))

    print("Got {} items in {:.3f} seconds".format(len(data),t.elapsed()))

    return data
    
def save(ways):
    """
    Save a list ways to a json file (for debugging)
    """
    with open('nodes.json','w') as f:
        json.dump(ways,f)

def load():
    """
    Load a list of ways from JSON file (for debugging)
    """
    with open('nodes.json') as json_file:
        return json.load(json_file)

def plotNodes(nds,color = 'c',scatter=False):
    """
    Plot a list of nodes to a matplotlib graph.
    """
    x = []
    y = []
    for nd in nds:
        coord = nd.getPos()
        print(coord)
        x.append(coord[0])
        y.append(coord[1])
    if scatter:
        plt.scatter(x,y,5,color)
    else:
        plt.plot(x,y,color)
    update()

def processWays(wayData, plot=False, scatter=False, color = 'c'):
    """
    Processes the raw OSM data for pathfinding & visualisation. Returns two lists of nodes.
    """
    nodes = []
    ways = {}
    junctionNodes = []

    for aWay in wayData:
        x = []
        y = []

        wayNodes = []

        geom = aWay['geometry'] # geometry is a property of way that contains all the lat/lon points on the polyline.
        numNodes = len(geom)

        for i in range(numNodes):
            latlon = geom[i]
            
            lon,lat = latlon['lon'],latlon['lat']
            newNode = node((lon,lat),aWay['tags']['highway'],aWay['id'])

            if i == numNodes-1 or i == 0: # append the first and last nodes of a way to the junctions list
                junctionNodes.append(newNode)
                plt.scatter(lon, lat, c='r')

            wayNodes.append(newNode)

            ways[aWay['id']] = way(wayNodes)

            if plot:
                x.append(lon)
                y.append(lat)

        nodes += wayNodes

        # plot for debugging purposes.
        if plot:
            if scatter:
                plt.scatter(x, y, 0.5, color)
            else:
                plt.plot(x,y,color)

    return nodes,junctionNodes,ways

def update():
    """
    This function refreshes the graph visual
    """
    plt.draw()  
    plt.pause(0.05)

if __name__ == "__main__":
    print("A: acquire from api")
    print("AS: acquire and save to file")
    print("L: load from file")

    inp = input(" - ").lower()

    if inp[0] == "a":   
        ways = aquire(int(input("Radius km: ")),50.950340,-2.520400)

    elif inp == "l":
        ways = load()
    
    if inp == "as":
        save(ways)

    processWays(ways)

    plt.show()
