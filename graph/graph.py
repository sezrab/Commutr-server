from math import cos
from maps.utils import haversine


class Graph(object):

    def __init__(self, xml):
        # ways is a dictionary that maps way ids to way objects
        ways = {way.attrib['id']: Way(way) for way in xml.findall('way')}

        # nodes is a dictionary that maps node ids to node objects
        nodes = {node.attrib['id']: Node(node) for node in xml.findall('node')}

        # junctions is a dictionary that maps node ids to all ways on which the corresponding node lies
        junctions = {}

        # FOR EACH way IN graph.ways:
        for way in ways.values():
            # start and end nodes
            terminalNodes = (way.nodeIDs[0], way.nodeIDs[-1])
            # search start and end nodes in every way

            # FOR EACH node IN nodes:
            for nodeID in terminalNodes:
                # IF node IN junctions.keys:
                if nodeID in junctions.keys():
                    # IF way NOT IN junctions[node]:
                    if way not in junctions[nodeID]:
                        junctions[nodeID].append(way.id)
                else:
                    junctions[nodeID] = [way.id]

        # FOR EACH way IN graph.ways:
        for way in ways.values():
            # nodes = way.nodes[1:-1]
            inbetweenNodes = way.nodeIDs[1:-1]
            # search every node in every way (apart from start and end nodes)
            # FOR EACH node IN nodes:
            for nodeID in inbetweenNodes:
                # IF node IN junctions.keys:
                if nodeID in junctions.keys():
                    # if this is node is on a junction, but this way is not marked as being on this junction
                    # IF way NOT IN junctions[node]:
                    if way not in junctions[nodeID]:
                        junctions[nodeID].append(way.id)

        # below is old unoptimised junction node code

        # for nodeID in nodes.keys():
        #             for way in ways.values():
        #                 if nodeID in [way.nodeIDs[0],way.nodeIDs[-1]]:
        #                     if nodeID in junctions.keys():
        #                         if way.id not in junctions[nodeID]:
        #                             junctions[nodeID].append(way.id)
        #                     else:
        #                         junctions[nodeID] = [way.id]
        # for wayID in ways:
        #     way = ways[wayID]
        #     waysNodes = way.nodeIDs
        #     ends = [waysNodes[0],waysNodes[-1]]
        #     for nodeID in ends:
        #         if nodeID in junctions.keys():
        #             # this node is a junction already
        #             # add this way id to the list if it is not already
        #             if wayID not in junctions[nodeID]:
        #                 junctions[nodeID].append(wayID)
        #         else:
        #             # this node hasn't been registered as a junction yet,
        #             # so register it
        #             junctions[nodeID] = [wayID]
        #     for nodeID in waysNodes:
        #         if nodeID in junctions.keys():
        #             if wayID not in junctions[nodeID]:
        #                 junctions[nodeID].append(wayID)

        self.__junctions = junctions
        self.__ways = ways
        self.__nodes = nodes

    def getNodeWayTypes(self, nodeID):
        """Returns all the different types of way (e.g. dual carriage way, footpath) that this node lies on.

        Args:
            nodeID (int): the id of the node in question

        Returns:
            list [string]: A list of string way type names
        """
        wayTypes = []
        for wayID in self.__junctions[nodeID]:
            wayTypes.append(self.__ways[wayID].wayType)
        return wayTypes

    def redetail(self, route):
        """Restores the detail in a route that has had unimportant (non-junction) nodes removed for pathfinding

        Args:
            route (list [node]): The undetailed route (output from aStar() of pathfinding.py)

        Returns:
            list [node]: The route with detail restored
        """
        detailedRoute = []
        for index in range(len(route)-1):
            juncNode = route[index]
            # for every junction node in route

            # get IDs of all ways that this junction node lies on
            wayIDs = self.junctions[juncNode.id]
            for wayID in wayIDs:
                way = self.ways[wayID]  # get way object from id
                if route[index+1].id in way.nodeIDs:
                    # if the next junction node on the route is on this way

                    # get position of current junction node in this way
                    aIndex = way.nodeIDs.index(route[index].id)

                    # get position of next junction node in this way
                    bIndex = way.nodeIDs.index(route[index+1].id)

                    # add all nodes between the two positions to the detailed list.
                    if bIndex >= aIndex:
                        detailedRoute += [self.nodes[nid]
                                          for nid in way.nodeIDs[aIndex:bIndex]]
                    else:
                        detailedRoute += [self.nodes[nid]
                                          for nid in way.nodeIDs[bIndex:aIndex][::-1]]
        return detailedRoute

    def trim(self, route, start, end):
        """Since the pathfinding always starts at a junction node, there are often too many nodes on the route,
        going past the start and end position, to the nearest junction node. This trims the route so that the specified
        start and end coordinates are the the closest to the first and last nodes on the route.

        Args:
            route (list [node]): The detailed route
            start (tuple): Start coordinate
            end (tuple): End coordinate

        Returns:
            list [node]: The trimmed route
        """
        # convert the route into the same format as the graph.nodes {id:node} so that it can be used by graph.getClosestNode()
        routeIDMap = {node.id: node for node in route}

        # get the closest node to the start
        closestToStart = self.nodes[self.getClosestNode(start, routeIDMap)]

        # get the closest node to the end
        closestToEnd = self.nodes[self.getClosestNode(end, routeIDMap)]

        # trim the list
        return route[route.index(closestToStart):route.index(closestToEnd)]

    def edgeCost(self, costMap, *nodeIDs):
        """Gets the average cost of travelling over a series of nodes

        Args:
            costMap (dict): The map of way type to cost (from graph/costs.py)

        Returns:
            float: The average cost
        """
        allWayTypes = []
        for nodeID in nodeIDs:
            allWayTypes.extend(self.getNodeWayTypes(nodeID))
            # add all the different way types of all the ways that all the given nodes lie on

        totalCost = 0
        for wayType in allWayTypes:
            if wayType in costMap.keys():
                # add the total costs
                totalCost += costMap[wayType]
            else:
                # add the unknown way type cost for this cost map
                totalCost += costMap[None]

        # return the average
        return totalCost/len(allWayTypes)

    @property
    def ways(self):
        # getter for graph.__ways
        return self.__ways

    @property
    def nodes(self):
        # getter for graph.__nodes
        return self.__nodes

    @property
    def junctions(self):
        # getter for graph.__junctions
        return self.__junctions

    @property
    def junctionNodes(self):
        # getter for the nodes that are junctions in graph.__junctions
        return list(self.__junctions.keys())

    def getClosestNode(self, latLon, nodes=None):
        """Gets the closest node in a set of nodes to a coordinate

        Args:
            latLon (tuple): The lat/lon coordinate
            nodes (map {id:node}, optional): The set of nodes. Defaults to None. If None, the map of self.nodes is used.

        Returns:
            int: The ID of the closest node
        """
        smallestDistance = None
        closestNodeID = None

        if nodes == None:
            nodes = self.junctionNodes

        for nodeID in nodes:
            node = self.nodes[nodeID]  # get node from id

            # use haversine formula to get the distance from the currently considered node to the coordinate
            d = haversine(node.position, latLon)

            # if this node is closer to the coordinatae than the closest previously considered node
            if smallestDistance is None or d < smallestDistance:
                # set this as the closest considered node
                closestNodeID = nodeID
                smallestDistance = d

        return closestNodeID

    def getNeighbouringNodes(self, node):
        """Get adjacent nodes on this graph to a specified node

        Args:
            node (node): The node to get neighbours of

        Returns:
            list [int]: The IDs of the adjacent nodes
        """
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

        return list(map(lambda x: self.nodes[x], neighbours))


class Node(object):
    def __init__(self, nodeElement):
        self.__nodeElement = nodeElement
        self.__id = nodeElement.attrib['id']

    @property
    def id(self):
        # getter for the node's id
        return self.__id

    @property
    def position(self):
        # getter for the node's position
        return float(self.__nodeElement.attrib['lat']), float(self.__nodeElement.attrib['lon'])

    def __str__(self) -> str:
        return str(self.id) + " @ " + str(self.position)


class Way(object):
    def __init__(self, element):
        self.__element = element  # xml metadata
        self.__id = element.attrib['id']
        self.__nodeIDs = [nd.attrib['ref']
                          for nd in element.findall('nd')]  # list of node ids
        self.__wayType = [e.attrib['v'] for e in element.findall(
            'tag') if e.attrib['k'] == 'highway'][0]

    @property
    def id(self):
        # getter for node.__id
        return self.__id

    @property
    def wayType(self):
        # getter for node.__wayType
        return self.__wayType

    @property
    def nodeIDs(self):
        # getter for node.__nodeIDs
        return self.__nodeIDs
