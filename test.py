from data import *

# Load the way data from the JSON file
ways = load()

# Set up visualisation
fig = plt.figure()
ax = fig.add_subplot(111)

nodes, junctions, ways = processWays(ways, True, False, 'c')

print(len(nodes))

aGraph = graph(nodes,ways,junctions)

clickedCoords = []
def onclick(event):
    """
    When two points on the map visual are clicked, calculate and display the shortest path between those points.
    """
    global clickedCoords

    print("Clicked... please wait")

    ix, iy = event.xdata, event.ydata
    clickedCoords.append(aGraph.closestNode((ix, iy)))

    print("Okay.")

    if len(clickedCoords) == 2:
        print("Finding route...")
        a, b = clickedCoords
        plotNodes(clickedCoords,'r')
        print("Distance is",haversine(a.getPos(),b.getPos()))
        route = astar.aStarSearch(aGraph,a,b)
        print(route)
        assert(route is not None)
        print("Done.\nPlotting...")
        plotNodes(route,'r')
        print("Plotted.")
        clickedCoords = []

cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()
