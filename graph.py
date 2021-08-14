import utils, constants

class graph(object):
    def __init__(self,nodes):
        self.nodes = nodes

    def edgeCost(self, fromNode, toNode): # generate a cost as if there is an edge there.
        return toNode.distanceFrom(fromNode) #* ((self.nodeCost(fromNode)+self.nodeCost(toNode))/2)

    def nodeCost(self,aNode):
        return constants.cyclingWayCostMap[aNode.getWayType()]

    def getNodeNeighbors(self, fromNode, exclusions = []):
        # get the four closest nodes
        # nodes = []
        # for aNode in self.nodes:
        #     if aNode.distanceFrom(fromNode) <= 10:
        #         if aNode.getPos() != fromNode.getPos():
        #             nodes.append(astarNode.fromNode(aNode))
        # return nodes
        nodesList = self.nodes
        closestNodes = []

        for i in range(4):
            closest, index = self.getClosestTo(fromNode,nodesList, exclusions)
            nodesList = nodesList[:index]+nodesList[index+1:]
            closestNodes.append(astarNode.fromNode(closest))

        return closestNodes

    def getClosestTo(self, aNode, nodesList=None, exclusions=[]):
        if nodesList is None:
            nodesList = self.nodes

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

class node(object):
    def __init__(self,pos,wayType,wayID):
        self.__pos = pos
        self.__wayType = wayType
        self.__wayID = wayID

    def getInfo(self):
        return self.__pos, self.__wayType, self.__wayID

    def getPos(self):
        return self.__pos

    def isAt(self,aNode):
        return self.getPos() == aNode.getPos()

    def getWayType(self):
        return self.__wayType

    def getWayID(self):
            return self.__wayID

    def toJson(self):
        return {'pos':self.__pos, 'wayType':self.__wayType, 'wayID':self.__wayID}

    def distanceFrom(self,other):
        return utils.haversine(self.__pos,other.getPos())

    @staticmethod
    def fromJson(data):
        return node(data['pos'], data['wayType'], data['wayID'])
    
    def __str__(self):
        return str(self.__pos)

class astarNode(node):
    def __init__(self,pos,wayType,wayID):
        super().__init__(pos,wayType,wayID)
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
        pos,wayType,wayID = aNode.getInfo()
        return astarNode(pos,wayType,wayID)