from math import sin,cos,atan2,sqrt,radians
from maps.constants import earthRadius

class PriorityQueue(object):
    def __init__(self):
        self.__queue = []

    def __str__(self):
        return ' '.join([str(i) for i in self.__queue])

    @property
    def empty(self):
        return len(self.__queue) == 0

    def contains(self,node):
        for item in self.__queue:
            if node in item:
                return True
        return False

    def remove(self,node):
        for item in self.__queue:
            if node in item:
                self.__queue.remove(item)
        return False

    def enqueue(self, node, f):
        if self.empty:
            self.__queue.append([node,f])
        else:
            for i in range(len(self.__queue)):
                if f < self.__queue[i][1]:
                    self.__queue.insert(i,[node,f])
                    return
            self.__queue.insert(i,[node,f])
  
    def dequeue(self):
        return self.__queue.pop(0)[0]
    