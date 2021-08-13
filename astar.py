from utils import *

def aStarSearch(graph, startNode, endNode):
    pq = PriorityQueue()
    pq.insert(startNode, 0)

    came_from = {}
    cost_so_far = {}


    came_from[startNode] = None
    cost_so_far[startNode] = 0
    
    current = None
    
    while not pq.isEmpty() and current != endNode:
        current = pq.pop()
        for next in graph.getNodeNeighbors(current):
            new_cost = cost_so_far[current] + graph.edgeCost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + haversine(next.pos, endNode.pos)
                pq.insert(next, priority)
                came_from[next] = current
    
    return came_from, cost_so_far