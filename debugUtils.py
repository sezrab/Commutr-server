import time
class timer():
    def __init__(self):
        self.__startTime = None
        self.reset()

    def reset(self):
        self.__startTime = time.time()

    def getTime(self):
        return time.time() - self.__startTime

    def __str__(self) -> str:
        s = "{:.2f}".format(self.getTime())
        self.reset()
        return s