from os import altsep

from maps.utils import haversine
from . import utils

def rebuildRoute(cameFrom,start,end):
    """Uses the cameFrom dictionary of aStar() to backtrack from the end node to the start node, returning the route in order

    Args:
        cameFrom (dict): cameFrom dictionary from the aStar function
        start (node): Start node of the pathfinding
        end (node): End node of the pathfinding

    Returns:
        list: The route, in order of start node to finish node
    """
    route = []
    
    prev = cameFrom[end]
    while prev != start:
        route.append(prev)
        prev = cameFrom[prev]
    
    return route[::-1]

def aStar(graph,startNode,endNode,costMap,verbose=False):

    if verbose:
        print("Starting with",startNode)

    # let the openList equal empty list of nodes
    openSet = utils.PriorityQueue()
    # let the closedList equal empty list of nodes
    closedSet = {}

    cameFrom = {}

    # put the startNode on the openList (leave its f at zero)
    openSet.enqueue(startNode,0)
    
    gCosts = {startNode:0}

    # while the openList is not empty
    while not openSet.empty:
        # let the currentNode equal the node with the least f value
        # remove the currentNode from the openList
        currentNode = openSet.dequeue()
        # add the currentNode to the closedList
        closedSet[currentNode] = 0

        # if currentNode is the goal
            # end reached
        
        if currentNode == endNode:
            if verbose:
                print("Completed")
            return rebuildRoute(cameFrom,startNode,endNode)
    
        # let the children of the currentNode equal the adjacent nodes
        neighbours = graph.getNeighbouringNodes(currentNode)
        if verbose:
            print()
            print("NODE:",currentNode)
            # print(closedSet)
            print("-"*10)
            print("Node has",len(neighbours),"neighbours")
            print("Node is",haversine(currentNode.position,endNode.position),"m from the end")
        # for each child in the children
        for neighbour in neighbours:
            if verbose:
                print("Neighbour:")
                print("   This neighbour is",neighbour)

            # if child is in the closedList
                # continue
            
            

            # child.g = currentNode.g + distance between child and current
            # child.h = distance from child to end
            # child.f = child.g + child.h
            
            h = haversine(endNode.position,neighbour.position)
            g = gCosts[currentNode] + (haversine(currentNode.position,neighbour.position) * graph.edgeCost(costMap,currentNode.id,neighbour.id))
            f = g + h

            if neighbour in closedSet.keys():
                if (closedSet[neighbour] < f):
                    if verbose:
                        print("   This neigbour is in the closed set.")
                    # if a node with the same position as successor  is in the CLOSED list which has a lower f than successor,
                    # skip this successor otherwise, add the node to the open list end (for loop)
                    continue
                else:
                    closedSet.pop(neighbour)

            # if child.position is in the openList's nodes positions
            #     if the child.g is higher than the openList node's g
            #         continue to beginning of for loop

            if openSet.contains(neighbour):
                if g > gCosts[neighbour]:
                    if verbose:
                        print("   (this node is already in the open set... continue)")
                    continue
                else:
                    openSet.remove(neighbour)
                
            # add the child to the openList
            
            gCosts[neighbour] = g
            cameFrom[neighbour] = currentNode
            openSet.enqueue(neighbour,f)
    if verbose:
        print("Did not finish")
