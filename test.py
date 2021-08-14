from data import *

ways = load()

fig = plt.figure()
ax = fig.add_subplot(111)

nodes = processWays(ways, True, True, 'c')

aGraph = graph(nodes)

# total = 0
# n = 400
# for nd in nodes[:n]:
#     total += len(aGraph.getNodeNeighbors(nd))
# print(total/n)
# input()

def closestNode(coords,nodes):
    closestNode = None
    closestDistance = None
    for aNode in nodes:
        d = haversine(aNode.getPos(),coords)
        if closestNode is None or d < closestDistance:
            closestDistance = d
            closestNode = aNode
    return closestNode

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
        # plotNodes(clickedCoords,'r')
        plotNodes(aGraph.getNodeNeighbors(a),'r',True)
        plotNodes(aGraph.getNodeNeighbors(b),'r',True)
        # print("Distance is",haversine(a.getPos(),b.getPos()))
        # route = astar.aStarSearch(aGraph,a,b)[0]
        # assert(route is not None)
        # print("Done.\nPlotting...")
        # plotNodes(route,'r')
        # print("Plotted.")
        clickedCoords = []
    

cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()
