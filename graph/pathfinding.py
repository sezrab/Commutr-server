from os import fsdecode
from .graph import Node
from . import utils
from maps.utils import haversine
from math import inf

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

def astar(graph,startNode,endNode):
    # https://gist.github.com/damienstanton/7de65065bf584a43f96a

    # closedset := the empty set    // The set of nodes already evaluated.
    # openset := {start}    // The set of tentative nodes to be evaluated, initially containing the start node
    # came_from := the empty map    // The map of navigated nodes.
    closedset = []
    openSet = utils.PriorityQueue()
    openSet.enqueue(startNode,haversine(startNode.position,endNode.position))
    cameFrom = {}

    # g_score[start] := 0    // Cost from start along best known path.
    # // Estimated total cost from start to goal through y.
    # f_score[start] := g_score[start] + heuristic_cost_estimate(start, goal)
    
    gScore = {}
    gScore[startNode] = 0

    while not openSet.empty:
        # current := the node in openset having the lowest f_score[] value
        # remove current from openset
        # add current to closedset
        currentNode = openSet.dequeue()
        if currentNode.position == endNode.position:
            print("Finished")
            return
            # return reconstruct_path(came_from, goal)
        closedset.append(currentNode)
        # for each neighbor in neighbor_nodes(current)

        nbours = graph.getNeighbouringNodes(currentNode)
        print("This node has",len(nbours),"neighbours")
        print("G =",gScore[currentNode])
        print("H =",haversine(currentNode.position,endNode.position))
        for neighbour in nbours:
            # if neighbor in closedset
            #     continue
            if neighbour in closedset:
                print("This neighbour is already visited")
                continue
            # tentative_g_score := g_score[current] + dist_between(current,neighbor)
            tentative_g_score = gScore[currentNode] + haversine(currentNode.position,neighbour.position)
            # if neighbor not in openset or tentative_g_score < g_score[neighbor] 
                # came_from[neighbor] := current
                # g_score[neighbor] := tentative_g_score
                # f_score[neighbor] := g_score[neighbor] + heuristic_cost_estimate(neighbor, goal)
                # if neighbor not in openset
                #     add neighbor to openset
            if not openSet.contains(currentNode) or tentative_g_score < gScore[neighbour]:
                cameFrom[neighbour] = currentNode
                gScore[neighbour] = tentative_g_score
                if not openSet.contains(neighbour):
                    openSet.enqueue(neighbour,gScore[neighbour] + haversine(neighbour.position, endNode.position))
    print("did not finish")

# # TODO: https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode
# # TODO: educative
# # TODO: https://isaaccomputerscience.org/concepts/dsa_search_a_star?examBoard=all&stage=all
# def astar(graph, startNode, endNode):
#     # openSet := {start}
#     openSet = utils.PriorityQueue()
#     openSet.enqueue(
#         startNode,
#         haversine(startNode.position,endNode.position),
#     )
#     # cameFrom := an empty map
#     cameFrom = {}
#     # gScore := map with default value of Infinity
#     gScore = {}
#     # gScore[start] := 0
#     gScore[startNode] = 0

#     while not openSet.empty:
#         # current := the node in openSet having the lowest fScore[] value
#         currentNode = openSet.dequeue()

#         # if current = goal
#         if currentNode == endNode:
#             # return reconstruct_path(cameFrom, current)
#             print("Success")
#             return
#         # openSet.Remove(current)
#         # handled by dequeue
#         nbours = graph.getNeighbouringNodes(currentNode)
#         print(len(nbours))
#         # for each neighbor of current
#         for neighbour in nbours:
#             # tentative_gScore := gScore[current] + d(current, neighbor)
#             tentative_gScore = gScore[currentNode] + haversine(currentNode.position, neighbour.position)
#             if neighbour not in gScore.keys():
#                 gScore[neighbour] = inf
#             print("GSCORE",tentative_gScore)
#             # if tentative_gScore < gScore[neighbor]
#             if tentative_gScore < gScore[neighbour]:
#                 # This path to neighbor is better than any previous one. Record it!
#                 # cameFrom[neighbor] := current
#                 cameFrom[neighbour] = currentNode
#                 # gScore[neighbor] := tentative_gScore
#                 gScore[neighbour] = tentative_gScore

#                 # fScore[neighbor] := gScore[neighbor] + h(neighbor)
#                 # if neighbor not in openSet
#                 #     openSet.add(neighbor)

#                 if openSet.contains(neighbour):
#                     print("This node is already in the open set")
#                     openSet.remove(neighbour)
#                 openSet.enqueue(neighbour,gScore[neighbour] + haversine(neighbour.position,endNode.position))
#     print("Failure")
#     return None

class pathfindingNode(Node):
    def __init__(self, xml, nodeElement, parentNode, g, h):
        super().__init__(xml, nodeElement)
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
    def fromNode(xml,node,parent,g,h):
        return pathfindingNode(xml,node.getNode(),parent,g,h)