from map import api
from lxml import etree as ET

class Graph(object):
    def __init__(self):
        self.__ways = {way.attrib['id']:Way(way) for way in root.findall('way')}
    
    def getWays(self):
        return self.__ways
    
    def getNeighbours(self,node):
        ways = node.getWays()
        neighbours = []
        for way in ways:
            neighbours += self.__ways[way].getNeighboursOnWay(node)
        return neighbours


class Node(object):
    def __init__(self, nodeElement):
        self.__nodeElement = nodeElement
        self.__id = nodeElement.attrib['id']
        self.__ways = None

    def getNode(self):
        return self.__nodeElement

    def getID(self):
        return self.__id

    def getPos(self):
        node = self.getNode()
        return float(node.attrib['lat']),float(node.attrib['lon'])

    def getWays(self): # TODO: do not create new ways.
        # get all ways that this node lies on
        if self.__ways is None:
            self.__ways = [way.attrib['id'] for way in root.xpath('way[tag/@k="highway" and nd/@ref={}]'.format(self.__id))]
        return self.__ways

    @staticmethod
    def fromID(id):
        return Node(Node.getNodeElementByID(id))
        
    @staticmethod
    def getNodeElementByID(id):
        return root.find('node[@id="{}"]'.format(id))


class Way(object):
    def __init__(self, wayElement):
        self.__wayElement = wayElement
        self.__nodes = None

    def getNodeIndex(self,nodeID):
        count = 0
        for node in self.getNodes():
            if node.getID() == nodeID:
                return count
            count += 1
        return None

    def getNeighboursOnWay(self,node):
        nodeIndex = self.getNodeIndex(node.getID())
        maxIndex = len(self.getNodes())-1
        neighbours = []
        if nodeIndex > 0:
            neighbours.append(self.getNodes()[nodeIndex-1])
        if nodeIndex < maxIndex:
            neighbours.append(self.getNodes()[nodeIndex+1])
        return neighbours

    def getNodes(self):
        if self.__nodes is None:
            self.__nodes = [Node.fromID(nd.attrib['ref']) for nd in self.__wayElement.findall('nd')]
        return self.__nodes

sherborne = (50.950340,-2.520400) # lat, lon

root = ET.fromstring(api.roadQuery(sherborne,1))