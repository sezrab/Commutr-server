from time import time
import json
from utils import haversine, timer
from overpass import *
from clipboard import copy
import matplotlib.pyplot as plt
import astar
from graph import *

def aquire(radius):
    print("Acquiring data...")
    t = timer()

    data = doQuery(queries.getSurroundingWays("highway",radius*1000,50.950340,-2.520400))

    print("Got {} items in {:.3f} seconds".format(len(data),t.elapsed()))

    return data
    
def save(ways):
    with open('nodes.json','w') as f:
        json.dump(ways,f)

def load():
    with open('nodes.json') as json_file:
        return json.load(json_file)

def plotNodes(nds,color = ''):
    x = []
    y = []
    for nd in nds:
        coord = nd.node().pos
        x.append(coord[0])
        y.append(coord[1])
    plt.plot(x,y,color)
    update()

def closestNode(coords,nodes):
    closestNode = None
    closestDistance = None
    for aNode in nodes:
        d = haversine(aNode.pos,coords)
        if closestNode is None or d < closestDistance:
            closestDistance = d
            closestNode = aNode
    return closestNode

def processWays(ways, plot=False, color = ''):
    nodes = []
    for way in ways:
        x = []
        y = []

        for latlon in way['geometry']:
            xp,yp = latlon['lon'],latlon['lat']
            newNode = node((xp,yp),way['tags']['highway'],way['id'])
            nodes.append(newNode)
            if plot:
                x.append(xp)
                y.append(yp)

        if plot:
            plt.plot(x,y,color)

    return nodes

def update():
    plt.draw()  
    plt.pause(0.05)

if __name__ == "__main__":
    import random

    ways = load()

    fig = plt.figure()
    ax = fig.add_subplot(111)

    nodes = processWays(ways, True, 'c')
    
    wayTypes = []

    for node in nodes:
        if node.wayType not in wayTypes:
            wayTypes.append(node.wayType)
    
    aGraph = graph(nodes)

    clickedCoords = []
    def onclick(event):
        global clickedCoords

        print("Clicked... please wait")

        ix, iy = event.xdata, event.ydata
        clickedCoords.append(closestNode((ix, iy),nodes))

        print("Okay.")

        if len(clickedCoords) == 2:
            print("Finding route...")
            a,b = clickedCoords
            route = list(astar.aStarSearch(aGraph,a,b)[0].keys())
            print("Done.\nPlotting...")
            plotNodes(route,'r')
            print("Plotted.")
            clickedCoords = []
        

    cid = fig.canvas.mpl_connect('button_press_event', onclick)

    plt.show()

    # print("A: acquire from api")
    # print("AS: acquire and save to file")
    # print("L: load from file")

    # inp = input(" - ").lower()

    # if inp[0] == "a":   
    #     ways = aquire(5)

    # elif inp == "l":
    #     ways = load()
    
    # if inp == "as":
    #     save(ways)

    # processWays(ways)
    
    # plt.show()
