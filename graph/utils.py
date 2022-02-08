class PriorityQueue(object):
    def __init__(self):
        # PriorityQueue.__queue takes form [ [node (Node), fCost (float)], ... ] 
        self.__queue = []

    @property
    def empty(self):
        """Property that returns true if the queue has no items.

        Returns:
            bool: True if empty
        """
        return len(self.__queue) == 0

    def contains(self,node):
        """To check whether the queue contains a certian node

        Args:
            node (Node)

        Returns:
            bool: True if node is present in queue
        """
        for item in self.__queue:
            if node in item:
                return True
        return False

    def remove(self,node):
        """For removing a node from the queue without dequeueing

        Args:
            node (Node): node to remove
        """
        for item in self.__queue:
            if node in item:
                self.__queue.remove(item)

    def enqueue(self, node, f):
        """Enqueue a node with a certain F cost.

        Args:
            node (Node): Node to enqueue
            f (float): F cost of the node
        """
        if self.empty:
            self.__queue.append([node,f])
        else:
            for i in range(len(self.__queue)):
                if f < self.__queue[i][1]:
                    self.__queue.insert(i,[node,f])
                    return
            self.__queue.insert(i,[node,f])
  
    def dequeue(self):
        """Dequeue the node with the least F cost

        Returns:
            Node
        """
        assert not self.empty
        return self.__queue.pop(0)[0]
    
    def __str__(self) -> str:
        """String representation of PriorityQueue. For debugging

        Returns:
            string
        """
        return str(list(map(lambda x: x[1], self.__queue)))