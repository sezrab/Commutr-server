from data import *

# Load the way data from the JSON file
ways = load()

# Set up visualisation
fig = plt.figure()
ax = fig.add_subplot(111)

nodes, junctions, ways = processWays(ways, True, False, False, 'c')

print(len(nodes))

aGraph = graph(nodes,ways,junctions)

clickedCoords = []
def onclick(event):
    """
    When two points on the map visual are clicked, calculate and display the shortest path between those points.
    """
    global clickedCoords

    ix, iy = event.xdata, event.ydata
    clickedCoords.append(aGraph.closestNode((ix, iy)))

    print("Click no.",len(clickedCoords))

    if len(clickedCoords) == 2:
        print("Finding route...")
        a, b = clickedCoords

        # plotNodes(clickedCoords,'r')

        route = astar.aStarSearch(aGraph,a,b)
        
        assert(route is not None)

        print("Route finding done.")

        print("Plotting visuals...")

        plotNodes(route,'r')

        print("Done.")
        
        clickedCoords = []

cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()
