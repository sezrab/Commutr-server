from math import cos
from maps.utils import haversine


class Graph(object):

    def __init__(self,xml):
        ways = {way.attrib['id']:Way(way) for way in xml.findall('way')}
        nodes = {node.attrib['id']:Node(node) for node in xml.findall('node')}

        junctions = {}
        for nodeID in nodes.keys():
                    for way in ways.values():
                        if nodeID in [way.nodeIDs[0],way.nodeIDs[-1]]:
                            if nodeID in junctions.keys():
                                if way.id not in junctions[nodeID]:
                                    junctions[nodeID].append(way.id)
                            else:
                                junctions[nodeID] = [way.id]
                
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
            for nodeID in waysNodes:
                if nodeID in junctions.keys():
                    if wayID not in junctions[nodeID]:
                        junctions[nodeID].append(wayID)
        self.__junctions = junctions
        self.__ways = ways
        self.__nodes = nodes

    def getNodeWayTypes(self,nodeID):
        wayTypes = []
        for wayID in self.__junctions[nodeID]:
            wayTypes.append(self.__ways[wayID].wayType)
        return wayTypes

    def redetail(self, route):
        detailedRoute = []
        for index in range(len(route)-1):
            juncNode = route[index]
            ways = self.junctions[juncNode.id]
            for wayID in ways:
                way = self.ways[wayID]
                if route[index+1].id in way.nodeIDs:
                    aIndex = way.nodeIDs.index(route[index].id)
                    bIndex = way.nodeIDs.index(route[index+1].id)
                    if bIndex >= aIndex:
                        detailedRoute += [self.nodes[nid] for nid in way.nodeIDs[aIndex:bIndex]]
                    else:
                        detailedRoute += [self.nodes[nid] for nid in way.nodeIDs[bIndex:aIndex][::-1]]
        return detailedRoute

    def trim(self,route,start,end):
        routeIDMap = {node.id:node for node in route}
        closestToStart = self.nodes[self.getClosestNode(start,routeIDMap)]
        closestToEnd = self.nodes[self.getClosestNode(end,routeIDMap)]
        return route[route.index(closestToStart):route.index(closestToEnd)]

    def edgeCost(self, costMap, *nodeIDs):
        allWayTypes = []
        for nodeID in nodeIDs:
            allWayTypes.extend(self.getNodeWayTypes(nodeID))
        totalCost = 0
        for wayType in allWayTypes:
            if wayType in costMap.keys():
                totalCost += costMap[wayType]
            else:
                totalCost += costMap[None] # unknown way type cost
        return totalCost/len(allWayTypes)


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

    def getClosestNode(self, latLon, nodes=None):
        smallestDistance = None
        closestNodeID = None
        if nodes == None:
            nodes = self.junctionNodes
        for nodeID in nodes:
            node = self.nodes[nodeID]
            d = haversine(node.position,latLon)
            if smallestDistance is None or d < smallestDistance:
                closestNodeID = nodeID
                smallestDistance = d
        return closestNodeID


    def getNeighbouringNodes(self,node):
        wayIDs = self.__junctions[node.id]
        # print("This node is on",len(wayIDs),"ways")
        neighbours = []

        for wayID in wayIDs:
            # print()
            # print("WAY:",wayID)
            way = self.__ways[wayID]
            # print("this way:",wayID)
            # get nodes on this way that are also junctions

            # print("way nodes",len(way.nodeIDs))
            # print("junc node",len(self.junctionNodes))

            # https://stackoverflow.com/questions/1388818/how-can-i-compare-two-lists-in-python-and-return-matches
            # junctionsOnWay = list(set(way.nodeIDs).intersection(self.junctionNodes)) # This answer has good algorithmic performance, as only one of the lists (shorter should be preferred) is turned into a set for quick lookup, and the other list is traversed looking up its items in the set
            
            junctionsOnWay = []
            for nodeID in way.nodeIDs:
                if nodeID in self.junctionNodes:
                    junctionsOnWay.append(nodeID)
            
            # this line appears to be causing inconsistencies

            # print("juncs on way",len(junctionsOnWay))

            # junctionsOnWay = list(set(way.nodeIDs) & set(self.junctionNodes))

            # print("num juncs:",len(junctionsOnWay))
            # remove self from neighbours
            # junctionsOnWay.remove(node.id)

            # below was wrong
            # neighbours += junctionsOnWay

            # get index in order of junctions on way
            nodeOrderIndex = junctionsOnWay.index(node.id)
            # print("node order index",nodeOrderIndex)
            # print(junctionsOnWay)
            # find adjacent junctions
            adjacent = []
            if nodeOrderIndex < len(junctionsOnWay) - 1:
                adjacent.append(junctionsOnWay[nodeOrderIndex+1])
            if nodeOrderIndex > 0:
                adjacent.append(junctionsOnWay[nodeOrderIndex-1])
            
            neighbours += adjacent

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

    def __str__(self) -> str:
        return str(self.id) + " @ " + str(self.position)


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