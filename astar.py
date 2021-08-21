from utils import *
from graph import *
from data import *

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

# https://mat.uab.cat/~alseda/MasterOpt/AStar-Algorithm.pdf
def aStarSearch(graph, startNode, endNode, verbose=False):
    startNode = astarNode.fromNode(startNode, 0, 0, edge(startNode,startNode,0))

    # enqueue start node in priority queue with p = 0
    
    # Put node_start in the OPEN list with f(node_start) = h(node_start) (initialization)
    openQueue = PriorityQueue()    
    openQueue.enqueue(startNode)
    
    closedLi = closedList()

    # consists on nodes that have been visited and expanded (sucessors have been explored already and
    # included in the open list, if this was the case).

    # while the OPEN list is not empty {
    while not openQueue.isEmpty():
        # while the queue is not empty, dequeue and explore neighbors.
        
        # Take from the open list the node node_current with the lowest F cost
        currentNode = openQueue.dequeue()

        # if node_current is node_goal we have found the solution; break
        if currentNode.isAt(endNode):
            return backtrack(currentNode,startNode)[0]

        if verbose:
            print("Current distance from end is:",haversine(currentNode.getPos(),endNode.getPos()))

        nodeEdges = graph.getNodeEdges(currentNode)

        if verbose:
            print("This node has",len(nodeEdges),"edges")

        # for each node_successor of node_current
        for anEdge in nodeEdges:

            successorNode = anEdge.getToNode()
            # Set successor_current_cost = g(node_current) + w(node_current, node_successor)
            successorNodeGCost =  anEdge.getCost() + backtrack(currentNode,startNode)[1]
            
            successor_open = openQueue.hasNodeAtPos(successorNode)
            successor_closed = closedLi.hasNodeAtPos(successorNode)
            
            successorNeighbours = graph.getNodeEdges(successorNode)

            # if node_successor is in the OPEN list
            if successor_open is not None and successor_open.g() <= successorNodeGCost:
                # if g(node_successor) ≤ successor_current_cost continue
                continue            
            # else if node_successor is in the CLOSED list
            elif successor_closed is not None and successor_closed.g() <= successorNodeGCost:
                # if g(node_successor) ≤ successor_current_cost continue
                if len(graph.getNodeEdges(successor_closed)) != len(successorNeighbours):
                    continue
            else:        
                # Else add node_successor to the OPEN list
                successorNodeHCost = haversine(successorNode.getPos(),endNode.getPos())
                openQueue.enqueue(astarNode.fromNode(successorNode,successorNodeGCost,successorNodeHCost,anEdge))
        
            # Set g(node_successor) = successor_current_cost
            # Set the parent of node_successor to node_current
        
        # Add node_current to the CLOSED list
        closedLi.append(currentNode)

    print("Algorithm finished. At end node? -",currentNode.isAt(endNode))

    return backtrack(currentNode,startNode)[0]

class closedList(object):
    def __init__(self):
        self.__closedList = []
    
    def append(self,obj):
        self.__closedList.append(obj)

    def hasNodeAtPos(self,aNode):
        for nd in self.__closedList:
            if aNode.isAt(nd):
                return nd
        return None

class astarNode(node):
    def __init__(self, pos, wayType, wayID, g, h, anEdge):
        super().__init__(pos, wayType, wayID)
        self.__g = g
        self.__h = h
        self.__f = g+h
        self.__edge = anEdge

    def getEdge(self):
        return self.__edge

    def g(self):
        return self.__g

    def f(self):
        return self.__f

    def h(self):
        return self.__h

    @staticmethod
    def fromNode(aNode, g, h, anEdge):
        pos, wayType, wayID = aNode.getInfo()
        return astarNode(pos, wayType, wayID, g, h, anEdge)
