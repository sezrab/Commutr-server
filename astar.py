from utils import *
from graph import *
from data import *

# def backtrack(graph, currNode, startNode, path = [], pathCoords=[], cumulativeG = 0, cumulativeF = 0): # recursive back track
#     path.append(currNode)
#     pathCoords.append(currNode.getPos())
#     # print(currNode.getPos(),startNode.getPos())
    
#     if currNode.isAt(startNode):
#         return path, pathCoords, cumulativeG, cumulativeF
    
#     if currNode.isAt(startNode):
#         print("ITS HERE")

#     fromNode = currNode.getEdge().getFromNode()

#     if fromNode.isAt(currNode):
#         print("ITS HERE!!")

#     cumulativeF += currNode.f()
#     cumulativeG += currNode.g()

#     return backtrack(graph, fromNode, startNode, path, pathCoords, cumulativeG, cumulativeF)

def backtrack(endNode,startNode):
    currNode = endNode
    path = []
    cumulativeG = 0
    cumulativeF = 0
    while currNode != startNode:
        path.append(currNode)
        currNode = currNode.getEdge().getFromNode()
        cumulativeG+=currNode.g()
        cumulativeF+=currNode.f()
    return path,cumulativeG,cumulativeF

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
        
        if currentNode.isAt(endNode):
            return backtrack(currentNode,startNode)[0]

        visited.append(currentNode.getPos())

        print("Current distance from end is:",haversine(currentNode.getPos(),endNode.getPos()))

        nodeEdges = graph.getNodeEdges(currentNode)

        print("This node has",len(nodeEdges),"edges")

        for edge in nodeEdges:

            toNode = edge.getToNode()

            if toNode.getPos() in visited:
                print("Node is already visited")
                continue

            neighbourH = haversine(toNode.getPos(),endNode.getPos())
            neighbourG =  edge.getCost() + backtrack(currentNode,startNode)[1]

            toNode_astar = astarNode.fromNode(toNode)

            toNode_astar.setCost(neighbourG, neighbourH, edge)
            
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


class astarNode(node):
    def __init__(self, pos, wayType, wayID):
        super().__init__(pos, wayType, wayID)
        self.__g = None
        self.__h = None
        self.__f = None
        self.__edge = None

    def getEdge(self):
        return self.__edge

    def setCost(self, g, h, edge):
        self.__g = g
        self.__h = h
        self.__f = g+h
        self.__edge = edge

    def g(self):
        return self.__g

    def f(self):
        return self.__f

    def h(self):
        return self.__h

    @staticmethod
    def fromNode(aNode):
        pos, wayType, wayID = aNode.getInfo()
        return astarNode(pos, wayType, wayID)
