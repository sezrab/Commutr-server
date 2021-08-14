from math import sin,cos,atan2,sqrt,radians
import time
import constants


def haversine(a, b):
    '''
    determines the great-circle distance between two GPS points
    https://en.wikipedia.org/wiki/Haversine_formula
    '''
    lat1, long1, lat2, long2 = map(radians, [a[0], a[1], b[0], b[1]])
    
    dlon = long2 - long1
    dlat = lat2 - lat1
    
    a = (sin(dlat/2))**2 + cos(lat1) * cos(lat2) * (sin(dlon/2))**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    d = c * constants.earthRad

    return d

class timer(object):
    def __init__(self):
        self.__start = time.time()
        
    def elapsed(self):
        return time.time() - self.__start
        
    def reset(self):
        self.__start = time.time()


class PriorityQueue(object):
    def __init__(self):
        self.queue = []
  
    def __str__(self):
        return ' '.join([str(i) for i in self.queue])
  
    def isEmpty(self):
        return len(self.queue) == 0
  
    def contains(self, aNode):
        return aNode in self.queue

    def remove(self,aNode):
        self.queue.remove(aNode)

    def enqueue(self, aNode):
        if self.isEmpty():
            self.queue.append(aNode)
        else:
            for i in range(len(self.queue)):
                if aNode.f < i:
                    self.queue.insert(i,aNode)
                    return
            self.queue.insert(i,aNode)
  
    def dequeue(self):
        return self.queue.pop(0)