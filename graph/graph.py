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
            # TODO: do not create new instances nodes if they already exist in graph
            neighbours += self.__ways[way].getNeighboursOnWay(node)
        return neighbours

    def getXML(self):
        return self.__xml

    def buildRouteFromJunctions(self, junctions):
        nodes = []
        previous = junctions[0]
        c = 0
        for junction in junctions[1:]:
            c+=1
            added = False
            for wayID in junction.getWays():
                way = self.__ways[wayID]
                way.getNodes(False,True)
                previousIndex = way.getNodeIndex(previous.getID())
                currentIndex = way.getNodeIndex(junction.getID())

                if previousIndex is not None and currentIndex is not None:
                    nodes += way.getNodes()[min(currentIndex,previousIndex):max(currentIndex,previousIndex)]
                    added = True
                    break
            
            assert added

            previous = junction

        return nodes

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
        return float(self.__nodeElement.attrib['lat']),float(self.__nodeElement.attrib['lon'])

    def getWays(self):
        # get all ways that this node lies on
        if self.__ways is None:
            self.__ways = [way.attrib['id'] for way in self.__xml.xpath('way[tag/@k="highway" and nd/@ref={}]'.format(self.__id))]
        return self.__ways
        
    @staticmethod
    def isJunction(ref,xml):
        l = len(xml.xpath('way[tag/@k="highway" and nd/@ref={}]'.format(ref)))
        return l > 1

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

    def getNodes(self,lowpoly=True,refresh=False):
        if refresh or self.__nodes is None:
            if lowpoly:
                self.__nodes = [Node.fromID(self.__xml,nd.attrib['ref']) for nd in self.__wayElement.findall('nd') if Node.isJunction(nd.attrib['ref'],self.__xml)]
            else:
                # print("getting all nodes on a way")
                self.__nodes = [Node.fromID(self.__xml,nd.attrib['ref']) for nd in self.__wayElement.findall('nd')]
        return self.__nodes

