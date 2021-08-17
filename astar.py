from utils import *
from graph import *

def backtrack(graph, currNode, startNode, path = [], cumulativeG = 0, cumulativeF = 0): # recursive back track
    path.append(currNode)
    
    if currNode.isAt(startNode):
        return path, cumulativeG, cumulativeF
    
    fromNode = currNode.getFromNode()

    cumulativeF += currNode.f()
    cumulativeG += currNode.g()

    return backtrack(graph, fromNode, startNode, path, cumulativeG, cumulativeF)

def aStarSearch(graph, startNode, endNode):
    startNode = astarNode.fromNode(startNode)
    endNode = astarNode.fromNode(endNode)

    # enqueue start node in priority queue with p = 0
    priorityQueue = PriorityQueue()
    
    startNode.setCost(0,0,startNode)
    priorityQueue.enqueue(startNode)

    visited = [] # visited is a list of coordinates.

    while not priorityQueue.isEmpty():
        # while the queue is not empty, dequeue and explore neighbors.
        currentNode = priorityQueue.dequeue()
        visited.append(currentNode.getPos())

        # print("Current distance from end is:",haversine(currentNode.getPos(),endNode.getPos()))

        if currentNode.isAt(endNode):
            return backtrack(graph,currentNode,startNode)

        nodeEdges = graph.getNodeEdges(currentNode)

        # print("This node has",len(currentNodeNeighbours),"neighbours")

        for edge in nodeEdges:

            toNode = edge.getToNode()

            if toNode.getPos() in visited:
                continue
            
            neighbourH = haversine(toNode.getPos(),endNode.getPos())
            neighbourG =  edge.getCost() + backtrack(graph,currentNode,startNode)[1]

            toNode_astar = astarNode.fromNode(toNode)

            toNode_astar.setCost(neighbourG, neighbourH, currentNode)
            
            # check if there is a path to neighbor node already
            nodeAtPos = priorityQueue.hasNodeAtPos(toNode_astar)

            if nodeAtPos is not None:
                if neighbourG < nodeAtPos.g():
                    # the new path is better than the existing path, so we update the new path.
                    priorityQueue.remove(nodeAtPos)
                else:
                    # the existing path is better so this path should be ignored
                    continue
                
            priorityQueue.enqueue(toNode_astar)


    return None,None
