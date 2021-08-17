import utils
import constants


class graph(object):
    def __init__(self, nodes, ways, junctionNodes):
        self.__nodes = nodes # TODO: Remove after debugging since it uses uneccessary memory
        self.__ways = ways
        self.__junctionNodes = junctionNodes

    def edgeCost(self, fromNode, toNode):
        """
        The openstreetmap data does not contain edges, so this function generates a cost of travelling between two nodes as if there were pre set edges.
        """
        return toNode.distanceFrom(fromNode) * ((self.nodeCost(fromNode)+self.nodeCost(toNode))/2)

    def nodeCost(self, aNode):
        """
        Get the favourability of travelling along this node.
        For example, travelling over a main road will have a very high cost for cyclists since it is an unpleasant way to travel, and a cycleway will have a low cost.
        TODO: Specify type of travel
        """
        return constants.cyclingWayCostMap[aNode.getWayType()]

    def nodeIsOnJunction(self,aNode):
        for juncNode in self.__junctionNodes:
            if juncNode.isAt(aNode.getPos()):
                return juncNode
        return False

    def getNodeEdges(self,aNode):
        edges = []
        neighbours = []
        isOnJunc = self.nodeIsOnJunction(aNode)
        wayID = aNode.getWayID()

        thisWay = self.__ways[wayID]
        neighbours += thisWay.getNodeNeighboursOnWay(aNode)
        if isOnJunc:
            neighbours.append(isOnJunc)
        
        for neighbour in neighbours:
            edges.append(aNode, neighbour, edge(self.edgeCost(aNode,neighbour)))
        
        return edges

    def closestNode(self, coords):
        closestNode = None
        closestDistance = None
        for aNode in self.__nodes:
            d = utils.haversine(aNode.getPos(),coords)
            if closestNode is None or d < closestDistance:
                closestDistance = d
                closestNode = aNode
        return closestNode

    def getClosestTo(self, aNode, nodesList=None, exclusions=[]):
        """
        Get closest node to a coordinate.
        """
        if nodesList is None:
            nodesList = self.__nodes

        closestNode = None
        closestDistance = None
        closestIndex = None
        for i in range(len(nodesList)):
            nd = nodesList[i]
            if nd.isAt(aNode) or nd.getPos() in exclusions:
                continue
            d = utils.haversine(aNode.getPos(), nd.getPos())
            if closestNode is None or d < closestDistance:
                closestDistance = d
                closestIndex = i
                closestNode = nd

        return closestNode, closestIndex

class edge(object):
    def __init__(self,fromNode,toNode,cost):
        self.__fromNode = fromNode
        self.__toNode = toNode
        self.__cost = cost

    def getCost(self):
        return self.__cost

    def getFromNode(self):
        return self.__fromNode

    def getToNode(self):
        return self.__toNode

class way(object):
    def __init__(self,nodes):
        self.__nodes = nodes
    
    def getNodeNeighboursOnWay(self, aNode):
        nNodes = len(self.__nodes)
        for i in range(len(self.__nodes)):
            if self.__nodes[i].isAt(aNode.getPos()):
                break
        if i == 0:
            return [self.__nodes[i+1]]
        elif i == nNodes-1:
            return [self.__nodes[i-1]]
        else:
            return [self.__nodes[i-1],self.__nodes[i+1]]


class node(object):
    def __init__(self, pos, wayType, wayID):
        self.__pos = pos
        self.__wayType = wayType
        self.__wayID = wayID

    def getInfo(self):
        return self.__pos, self.__wayType, self.__wayID

    def getPos(self):
        return self.__pos

    def isAt(self, aNode):
        return self.getPos() == aNode.getPos()

    def getWayType(self):
        return self.__wayType

    def getWayID(self):
        return self.__wayID

    def toJson(self):
        return {'pos': self.__pos, 'wayType': self.__wayType, 'wayID': self.__wayID}

    def distanceFrom(self, other):
        return utils.haversine(self.__pos, other.getPos())

    @staticmethod
    def fromJson(data):
        return node(data['pos'], data['wayType'], data['wayID'])

    def __str__(self):
        return str(self.__pos)


class astarNode(node):
    def __init__(self, pos, wayType, wayID):
        super().__init__(pos, wayType, wayID)
        self.__g = None
        self.__h = None
        self.__f = None
        self.__fromNode = None

    def getFromNode(self):
        return self.__fromNode

    def setCost(self, g, h, fromNode):
        self.__g = g
        self.__h = h
        self.__f = g+h
        self.__fromNode = fromNode

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
