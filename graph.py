import utils, constants

class graph(object):
    def __init__(self,nodes):
        self.nodes = nodes

    def edgeCost(self, fromNode, toNode): # generate a cost as  if there is an edge there.
        return (self.nodeCost(fromNode)+self.nodeCost(toNode))/2

    def nodeCost(self,aNode):
        return constants.cyclingWayCostMap[aNode.wayType]

    def getNodeNeighbors(self, fromNode):
        edges = []
        for aNode in self.nodes:
            if aNode.distanceFrom(fromNode) <= 1:
                edges.append(routeNode(aNode))
        return edges

class node(object):
    def __init__(self,pos,wayType,wayID):
        self.pos = pos
        self.wayType = wayType
        self.wayID = wayID

    def toJson(self):
        return {'pos':self.pos, 'wayID':self.wayID}

    def distanceFrom(self,other):
        return utils.haversine(self.pos,other.pos)

    @staticmethod
    def fromJson(data):
        return node(data['pos'],data['wayID'])
    
    def __str__(self):
        return str(self.pos)

class edge(object):
    def __init__(self, fromNode, toNode, cost):
        self.fromNode = fromNode
        self.toNode = toNode
        self.cost = cost

class routeNode(object):
    def __init__(self, aNode, predecessor = None, g=0, h=0, f=0):
        self.h = h
        self.g = g
        self.f = f
        self.__visited = False
        self.predecessor = predecessor
        self.__node = aNode
    
    def visit(self):
        self.__visited = True
    
    def visited(self):
        return self.__visited

    def node(self):
        return self.__node