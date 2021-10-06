class Graph(object):

    def __init__(self,xml):
        ways = {way.attrib['id']:Way(way) for way in xml.findall('way')}
        nodes = {node.attrib['id']:Node(node) for node in xml.findall('node')}

        # something is wrong here.
        junctions = {}

        for wayID in ways:
            way = ways[wayID]
            waysNodes = way.nodeIDs
            ends = [waysNodes[0],waysNodes[-1]]
            for nodeID in ends:
                if nodeID in junctions.keys():
                    # this node is a junction already
                    # add this way id to the list if it is not already
                    if wayID not in junctions[nodeID]:
                        junctions[nodeID].append(wayID)
                else:
                    # this node hasn't been registered as a junction yet,
                    # so register it
                    junctions[nodeID] = [wayID]

        for nodeID in nodes.keys():
            for way in ways.values():
                if nodeID in [way.nodeIDs[0],way.nodeIDs[-1]]: # possibly only check first and last
                    if nodeID in junctions.keys():
                        if way.id not in junctions[nodeID]:
                            junctions[nodeID].append(way.id)
                    else:
                        junctions[nodeID] = [way.id]
        
        self.__junctions = junctions
        self.__ways = ways
        self.__nodes = nodes


    @property
    def ways(self):
        return self.__ways
    
    @property
    def nodes(self):
        return self.__nodes

    @property
    def junctions(self):
        return self.__junctions

    @property
    def junctionNodes(self):
        return list(self.__junctions.keys())

    def getNeighbouringNodes(self,node):
        wayIDs = self.__junctions[node.id]

        neighbours = []

        for wayID in wayIDs:
            way = self.__ways[wayID]

            # https://stackoverflow.com/questions/1388818/how-can-i-compare-two-lists-in-python-and-return-matches
            junctionsOnWay = set(way.nodeIDs).intersection(self.junctionNodes) # This answer has good algorithmic performance, as only one of the lists (shorter should be preferred) is turned into a set for quick lookup, and the other list is traversed looking up its items in the set
            junctionsOnWay.remove(node.id)

            neighbours += junctionsOnWay

        return list(map(lambda x: self.nodes[x],neighbours))

class Node(object):
    def __init__(self, nodeElement):
        self.__nodeElement = nodeElement
        self.__id = nodeElement.attrib['id']

    @property
    def id(self):
        return self.__id

    @property
    def position(self):
        return float(self.__nodeElement.attrib['lat']),float(self.__nodeElement.attrib['lon'])



class Way(object):
    def __init__(self, element):
        self.__element = element # xml metadata
        self.__id = element.attrib['id']
        self.__nodeIDs = [nd.attrib['ref'] for nd in element.findall('nd')] # list of node ids
        self.__wayType = [e.attrib['v'] for e in element.findall('tag') if e.attrib['k'] == 'highway'][0]

    @property
    def id(self):
        return self.__id

    @property
    def wayType(self):
        return self.__wayType

    @property
    def nodeIDs(self):
        return self.__nodeIDs