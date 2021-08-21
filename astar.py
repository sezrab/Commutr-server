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

# https://www.edureka.co/blog/a-search-algorithm/
def aStarSearch(graph, startNode, endNode, verbose=False):
    """
    let the openList equal empty list of nodes +
    let the closedList equal empty list of nodes +
    put the startNode on the openList (leave it's f at zero) +
    while the openList is not empty +
        let the currentNode equal the node with the least f value +
        remove the currentNode from the openList +
        add the currentNode to the closedList +
        if currentNode is the goal +
            You've found the end! +
        let the children of the currentNode equal the adjacent nodes +
        for each child in the children +
            if child is in the closedList +
                continue to beginning of for loop +
            child.g = currentNode.g + distance between child and current +
            child.h = distance from child to end +
            child.f = child.g + child.h +
            if child.position is in the openList's nodes positions
                if the child.g is higher than the openList node's g
                    continue to beginning of for loop
            add the child to the openList
    """
    # let the openList equal empty list of nodes
    openQueue = PriorityQueue()    
    # let the closedList equal empty list of nodes
    closedLi = closedList()
    
    # put the startNode on the openList (leave it's f at zero)
    startNode = astarNode.fromNode(startNode, 0, 0, edge(startNode,startNode,0))
    openQueue.enqueue(startNode)

    # while the openList is not empty
    while not openQueue.isEmpty():
        # let the currentNode equal the node with the least f value
        # remove the currentNode from the openList
        currentNode = openQueue.dequeue()
        
        # add the currentNode to the closedList
        closedLi.append(currentNode)

        # if currentNode is the goal
            # You've found the end!

        if currentNode.isAt(endNode):
            print("FOUND!")
            break

        # let the children of the currentNode equal the adjacent nodes
        nodeEdges = graph.getNodeEdges(currentNode)
        # for each child in the children
        for anEdge in nodeEdges:
            
            childNode = astarNode.fromNode(
                anEdge.getToNode(),
                anEdge.getCost() + backtrack(currentNode,startNode)[1],
                haversine(anEdge.getToNode().getPos(),endNode.getPos()),
                anEdge,
            )

            # if child is in the closedList
                # continue to beginning of for loop
                
            if closedLi.hasUniqueNode(childNode):
                continue
            
            # if child.position is in the openList's nodes positions
            openQueueNode = openQueue.hasNodeAtPos(childNode)
            if openQueueNode is not None:
                # if the child.g is higher than the openList node's g
                if childNode.g() > openQueueNode.g():
                    # continue to beginning of for loop
                    continue
            # add the child to the openList
            openQueue.enqueue(childNode)
            

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

    def hasUniqueNode(self,aNode):
        ndID = aNode.getIDTuple()
        for nd in self.__closedList:
            if nd.getIDTuple() == ndID:
                return True
        return False

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
