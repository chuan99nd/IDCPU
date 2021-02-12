from queue import PriorityQueue
from GetParam import Param
class Environment():
    """
    state: array of color list
    action: a color
    reward: reward after impliment action
    """
    def __init__(self, param:Param):
        self.graph = param.G
        self.state = []
        self.colorSet = {}
        self.currColor = 0

        self.currQueue = PriorityQueue()
        self.nextQueue = PriorityQueue()
    
    def reset(self, param):
        self.__init__(param)


       