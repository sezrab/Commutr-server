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

        # for each node_successor of node_current
        nodeEdges = graph.getNodeEdges(currentNode)

        print("Attempt on",str(currentNode))

        # Add node_current to the CLOSED list
        closedLi.append(currentNode)

        for anEdge in nodeEdges:

            if anEdge.getToNode().isAt(currentNode):
                continue 

            successorNode = astarNode.fromNode(
                anEdge.getToNode(),
                # Set successor_current_cost = g(node_current) + w(node_current, node_successor)
                anEdge.getCost() + backtrack(currentNode,startNode)[1],
                haversine(anEdge.getToNode().getPos(),endNode.getPos()),
                anEdge,
            )

            successorNeighbours = graph.getNodeEdges(successorNode)

            successor_closed = closedLi.hasNodeAtPos(successorNode)

            if successor_closed:
                print("this node has already been visited")
                # this node has already been visited
                if (len(successorNeighbours) > len(graph.getNodeEdges(successor_closed))) or successorNode.g() < successor_closed.g():
                    # the new node at this position has more neighbors or a better cost, so we should unvisit.
                    print("Unvisiting node because we have more neighbors")
                    closedLi.remove(successor_closed)
                else:
                    print("moving on from this pre-visited node")
                    # move on since we've tried a better path down this route already.
                    continue
                
            # if node_successor is in the OPEN list
            successor_open = openQueue.hasNodeAtPos(successorNode)
            if successor_open is not None and successorNode.g() <= successor_open.g():
                print("Removing successor from open list")
                # we found a route with a lower G cost, so remove the old one from the open list
                openQueue.remove(successor_open)

            # add node_successor to the OPEN list
            print("adding ",successorNode)
            openQueue.enqueue(successorNode)
        
    print("Algorithm finished. At end node? -",currentNode.isAt(endNode))

    return backtrack(currentNode,startNode)[0]

class closedList(object):
    def __init__(self):
        self.__closedList = []
    
    def append(self,obj):
        self.__closedList.append(obj)

    def remove(self,item):
        self.__closedList.remove(item)

    def hasNodeAtPos(self,aNode):
        ndID = aNode.getIDTuple()
        for nd in self.__closedList:
            if aNode.isAt(nd) and ndID != nd.getIDTuple():
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
