from math import sin,cos,atan2,sqrt,radians
from maps.constants import earthRadius

class PriorityQueue(object):
    def __init__(self):
        self.__queue = []

    def __str__(self):
        return ' '.join([str(i) for i in self.__queue])

    def isEmpty(self):
        return len(self.__queue) == 0

    def contains(self, aNode):
        ndID = aNode.getIDTuple()
        for nd in self.__queue:
            if ndID == nd.getIDTuple():
                return True
        return False

    def hasNode(self, aNode):
        for node in self.__queue:
            if node.getID() == aNode.getID():
                return node
        return None

    def remove(self,aNode):
        self.__queue.remove(aNode)

    def enqueue(self, aNode):
        if self.isEmpty():
            self.__queue.append(aNode)
        else:
            for i in range(len(self.__queue)):
                if aNode.f() < self.__queue[i].f():
                    self.__queue.insert(i,aNode)
                    return
            self.__queue.insert(i,aNode)
  
    def dequeue(self):
        return self.__queue.pop(0)
    