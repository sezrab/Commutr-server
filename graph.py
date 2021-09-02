class Graph(object):
    def __init__(self,xml):
        self.__ways = {way.attrib['id']:Way(xml,way) for way in xml.findall('way')}
        self.__xml = xml

    def getWays(self):
        return self.__ways
    
    def getNeighbours(self,node):
        ways = node.getWays()
        neighbours = []
        for way in ways:
            neighbours += self.__ways[way].getNeighboursOnWay(node)
        return neighbours

    def getXML(self):
        return self.__xml

class Node(object):
    def __init__(self, xml, nodeElement):
        self.__nodeElement = nodeElement
        self.__id = nodeElement.attrib['id']
        self.__ways = None
        self.__xml = xml

    def getNode(self):
        return self.__nodeElement

    def getID(self):
        return self.__id

    def getPos(self):
        node = self.getNode()
        return float(node.attrib['lat']),float(node.attrib['lon'])

    def getWays(self):
        # get all ways that this node lies on
        if self.__ways is None:
            self.__ways = [way.attrib['id'] for way in self.__xml.xpath('way[tag/@k="highway" and nd/@ref={}]'.format(self.__id))]
        return self.__ways

        
    @staticmethod
    def fromID(xml,id):
        return Node(xml,Node.getNodeElementByID(xml,id))
        
    @staticmethod
    def getNodeElementByID(xml,id):
        return xml.find('node[@id="{}"]'.format(id))


class Way(object):
    def __init__(self, xml, wayElement):
        self.__wayElement = wayElement
        self.__nodes = None
        self.__xml = xml

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
            self.__nodes = [Node.fromID(self.__xml,nd.attrib['ref']) for nd in self.__wayElement.findall('nd')]
        return self.__nodes
