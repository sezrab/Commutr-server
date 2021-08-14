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

def plotNodes(nds,color = '',scatter=False):
    x = []
    y = []
    for nd in nds:
        coord = nd.getPos()
        x.append(coord[0])
        y.append(coord[1])
    if scatter:
        plt.scatter(x,y,5,color)
    else:
        plt.plot(x,y,color)
    update()

def processWays(ways, plot=False, scatter=False, color = 'b'):
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
            if scatter:
                plt.scatter(x, y, 0.5, color)
            else:
                plt.plot(x,y,color)

    return nodes

def update():
    plt.draw()  
    plt.pause(0.05)

if __name__ == "__main__":
    print("A: acquire from api")
    print("AS: acquire and save to file")
    print("L: load from file")

    inp = input(" - ").lower()

    if inp[0] == "a":   
        ways = aquire(int(input("Radius km: ")))

    elif inp == "l":
        ways = load()
    
    if inp == "as":
        save(ways)

    processWays(ways)

    plt.show()
