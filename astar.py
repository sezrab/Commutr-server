from utils import *
from graph import *

def aStarSearch(graph, startNode, endNode):

    startNode = routeNode(startNode)
    endNode = routeNode(endNode)

    openSet = PriorityQueue()
    openSet.enqueue(startNode)

    currentNode = routeNode(startNode)
    
    while not openSet.isEmpty():
        # print("-")
        currentNode = openSet.dequeue()
        print(len(openSet.queue))
        if currentNode == endNode:
            return openSet.queue

        currentNode.visit()

        for neighbour in graph.getNodeNeighbors(currentNode.node()):
            # print(currentNode.g)
            if neighbour.visited():
                print("already visited")
                continue
            
            # F is the total cost of the node.
            # G is the distance between the current node and the start node.
            # H is the heuristic — estimated distance from the current node to the end node.

            neighbourG = currentNode.g + ((neighbour.node().distanceFrom(currentNode.node())+1)*constants.cyclingWayCostMap[neighbour.node().wayType])

            print(neighbourG)

            if openSet.contains(neighbour) and neighbourG >= neighbour.g:
                continue
                
            neighbour.g = neighbourG
            h = neighbour.node().distanceFrom(endNode.node())
            neighbour.h = h
            f = neighbourG + h
            neighbour.f = f

            if openSet.contains(neighbour):
                openSet.remove(neighbour) # remove so the cost can be updated

            openSet.enqueue(neighbour)
        
    return openSet.queue
