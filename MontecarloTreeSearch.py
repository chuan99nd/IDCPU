from GetParam import Param, INFINITE, random,C
from MiniIndividual import Individual
from GetParam import numpy as np
from MiniGa import  GA
from Node import Node
from queue import heappop, heappush
import math
class MontecarloTreeSearch():
    def __init__(self, path):
        self.param = Param()
        self.param.buildGraph(path)
        _root = Node(d=None, par=None, param=self.param)
        _root.currDistance = np.full((self.param.N,), INFINITE)
        _root.currDistance[self.param.s] = 0
        _root.currVertice = np.full((self.param.N,), False)
        _root.currVertice[self.param.s] = True
        _root.domainTravered = np.array([], dtype="int32")
        _root.minDis = -INFINITE
        _root.maxQ = INFINITE
        _root.minQ = -INFINITE
        self.root = _root
        # nammoadidaphat
    def UCT1(self, parrent:Node, child: Node):
        if parrent.maxQ == parrent.minQ:
            return np.sqrt(math.log(parrent.n+1)/np.sqrt(child.n+1))
        return (child.Q-parrent.minQ)/(parrent.maxQ-parrent.minQ) + C*np.sqrt(math.log(parrent.n+1)/np.sqrt(child.n+1))
    def selection(self):
        _currNode = self.root
        while(len(_currNode.childs)) > 0:
            _bestNode = None
            _bestValue = -INFINITE
            for domain in _currNode.childs:
                if not _currNode.childs[domain].isTerminal:
                    if self.UCT1(_currNode, _currNode.childs[domain]) > _bestValue:
                        _bestNode = _currNode.childs[domain]
            _currNode = _bestNode
        # calculate next node
        if _currNode.d != None: # root node
            _parrent = _currNode.par
            preDistance = _parrent.currDistance
            fromParrentVertice = _parrent.currVertice
            duyet = np.full((self.param.N,), False)

            currQueue = list()           
            for v in range(self.N):
                if fromParrentVertice[v] and self.param.best > preDistance[v]:
                    for w, u in self.G[v][_currNode.d]:
                        heappush(currQueue, (preDistance[v]+w, u))

            distance = np.full((self.N,), INFINITE)
            # print(distance)
            while len(currQueue)>0:
                d_v, v= heappop(currQueue)
                if duyet[v]:
                    continue
                distance[v] = min(d_v, distance[v])
                duyet[v] = True
                for w, u in self.G[v][_currNode.d]:
                    if not duyet[u]:
                        heappush(currQueue,(d_v+w, u))
            _currNode.currDistance = distance
            _currNode.currVertice = duyet
            _currNode.domainTravered.append(_currNode.d)
            # caculate mindis:
            _currNode.minDis = np.amin(_currNode.currDistance)
            _currNode.n += 1
            if _currNode.minDis >= self.param.best or len(_currNode.domainTravered)==self.param.N:
                _currNode.isTerminal = True
        return _currNode

    def expandAndSimulation(self, curr: Node):
        if curr.isTerminal:
            return None
        ga = GA(domainTraivered=curr.domainTravered, parrentdistance=curr.currDistance, fromParrentVertice=curr.currVertice,
                param=self.param, parrent=curr)
        ga.init() # add child node to curr
        #Simulation
        ga.run()
    
    def backpropagation(self, curr: Node):
        # update Q, N, terminate, minDis, minQ, maxQ
        if curr.par == None:
            return
        # update Q:
        _min = INFINITE
        _max = -INFINITE
        for _d in curr.childs:
            curr.Q = max(curr.Q, curr.childs[_d].Q)
            _min = min(_min, curr.childs[_d].Q)
            _max = max(_max, curr.childs[_d].Q)
        curr.minQ = _min
        curr.maxQ = _max
        if curr.checkTerminate():
            _d = curr.d
            curr = curr.par
            del curr.childs[_d]
        self.backpropagation(curr.par)
    def run(self, STEP):
        for step in range(STEP):
            currNode = self.root
        
