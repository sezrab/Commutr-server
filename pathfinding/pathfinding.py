from graph import Node
from . import utils

def backtrack(endNode,startNode):
    currNode = endNode
    path = []
    cumulativeG = 0
    cumulativeF = 0
    while currNode != startNode:
        path.append(currNode)
        currNode = currNode.getParentNode()
        cumulativeG+=currNode.g()
        cumulativeF+=currNode.f()
    return path,cumulativeG,cumulativeF

def astar(graph, startNode, endNode):
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
    openQueue = utils.PriorityQueue()    

    # let the closedList equal empty list of nodes
    closedList = []
    
    # put the startNode on the openList (leave it's f at zero)
    startNode = pathfindingNode.fromNode(startNode, startNode, 0, 0)
    openQueue.enqueue(startNode)

    # while the openList is not empty
    while not openQueue.isEmpty():
        # print()
        # let the currentNode equal the node with the least f value
        # remove the currentNode from the openList
        currentNode = openQueue.dequeue()
        
        # add the currentNode to the closedList
        closedList.append(currentNode.getID())

        # if currentNode is the goal
            # You've found the end!

        if currentNode.getID() == endNode.getID():
            print("Finished!")
            return backtrack(currentNode,startNode)[0]

        # let the children of the currentNode equal the adjacent nodes
        neighbours = graph.getNeighbours(currentNode)
        # print("Popped node with %i neighbours from PQ"%len(neighbours))
        # for each child in the children
        for neighbour in neighbours:
            # print()
            # print("Inspecting neighbour")
            # newG = utils.haversine(neighbour.getPos(),currentNode.getPos()) + backtrack(currentNode,startNode)[1]
            # print("Total G for this neighbour is",newG)
            childNode = pathfindingNode.fromNode(
                neighbour,
                currentNode,
                utils.haversine(neighbour.getPos(),currentNode.getPos()) + backtrack(currentNode,startNode)[1],
                utils.haversine(neighbour.getPos(),endNode.getPos()),
            )

            # if child is in the closedList
                # continue to beginning of for loop
                
            if childNode.getID() in closedList:
                # print("Already visited this node")
                continue
            
            # if child is in the open list
            openQueueNode = openQueue.hasNode(childNode)

            if openQueueNode is not None:
                # print("This node is already in the PQ")
                # if the child.g is higher than the openList node's g
                if childNode.g() > openQueueNode.g():
                    # print("The node in the PQ had a lower G")
                    # continue to beginning of for loop
                    continue
            # add the child to the openList
            # print("Adding this node to the PQ")
            openQueue.enqueue(childNode)
            
    print("Did not finish.")
    return backtrack(currentNode,startNode)[0]

class pathfindingNode(Node):
    def __init__(self, nodeElement, parentNode, g, h):
        super().__init__(nodeElement)
        self.__parentNode = parentNode
        self.__g = g
        self.__h = h
        self.__f = g+h
        
    def getParentNode(self):
        return self.__parentNode

    def g(self):
        return self.__g

    def f(self):
        return self.__f
    
    @staticmethod
    def fromNode(node,parent,g,h):
        return pathfindingNode(node.getNode(),parent,g,h)