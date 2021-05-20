from GetParam import Param, INFINITE, random,C, BIAS, K
from MiniIndividual import Individual
from GetParam import np
from MiniGa import  GA
from Node import Node
from queue import heappop, heappush
import math
class MontecarloTreeSearch():
    def __init__(self, path):
        random.seed(0)  
        self.param = Param()
        self.param.buildGraph(path)
        self.N = self.param.N
        self.G = self.param.G
        self.d = self.param.D
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
    def UCT1(self, parrent:Node, child: Node, Qstd, Qmean, Hstd, Hmean):
        if Hstd == 0:
            Hstd = INFINITE
        if parrent.maxQ == parrent.minQ:
            return np.sqrt(math.log(parrent.n+BIAS)/np.sqrt(child.n+BIAS)) - K*(child.minDis-Hmean)/Hstd
            # return  - K*(child.minDis-Hmean)/Hstd

        # return (child.Q-Qmean)/Qstd + C*np.sqrt(math.log(parrent.n+BIAS)/np.sqrt(child.n+BIAS))# - K*child.minDis/self.param.best
        return  (child.Q-Qmean)/Qstd + C*np.sqrt(math.log(parrent.n+BIAS)/np.sqrt(child.n+BIAS)) - K*(child.minDis-Hmean)/Hstd

    def getStat(self, Qlist:list):
        _n = len(Qlist)
        _sum = sum(Qlist)
        _mean = _sum/_n
        _varArray = [(x-_mean)*(x-_mean) for x in Qlist]
        _std = math.sqrt(sum(_varArray)/_n)
        return _mean, _std
    def selection(self):
        _currNode = self.root
        while(len(_currNode.childs)) > 0:
            # _currNode.show()
            _bestNode = None
            _bestValue = -INFINITE
            Qlist = []
            Hlist = []
            for domain in _currNode.childs:
                if not _currNode.childs[domain].isTerminal:
                    Qlist.append(_currNode.childs[domain].Q)
                    Hlist.append(_currNode.childs[domain].minDis)
            # print("Qlist: " +str(Qlist))
            _Qmean, _Qstd = self.getStat(Qlist)
            _Hmean, _Hstd = self.getStat(Hlist)
            for domain in _currNode.childs:
                if not _currNode.childs[domain].isTerminal:
                    _temp = self.UCT1(_currNode, _currNode.childs[domain], _Qstd, _Qmean, _Hmean, _Hstd)
                    if _temp > _bestValue:
                        _bestValue = _temp
                        _bestNode = _currNode.childs[domain]
            _currNode = _bestNode
        # calculate next node
        # if _currNode.d != None: # !=root node
        #     _parrent = _currNode.par
        #     preDistance = _parrent.currDistance
        #     fromParrentVertice = _parrent.currVertice
        #     duyet = np.full((self.param.N,), False)

        #     currQueue = list()           
        #     for v in range(self.N):
        #         if fromParrentVertice[v] and self.param.best > preDistance[v]:
        #             for w, u in self.G[v][_currNode.d]:
        #                 heappush(currQueue, (preDistance[v]+w, u))

        #     distance = np.full((self.N,), INFINITE)
        #     # print(distance)
        #     while len(currQueue)>0:
        #         d_v, v= heappop(currQueue)
        #         if duyet[v]:
        #             continue
        #         distance[v] = min(d_v, distance[v])
        #         duyet[v] = True
        #         for w, u in self.G[v][_currNode.d]:
        #             if not duyet[u]:
        #                 heappush(currQueue,(d_v+w, u))
        #     _currNode.currDistance = distance
        #     _currNode.currVertice = duyet
        #     # caculate mindis:
        #     _currNode.minDis = np.amin(_currNode.currDistance)
            _currNode.n += 1
            if _currNode.minDis >= self.param.best or len(_currNode.domainTravered)==self.param.N:
                _currNode.isTerminal = True
        return _currNode

    def expandAndSimulation(self, curr: Node):
        if curr.isTerminal or curr.minDis >= self.param.best:
            # curr.show()
            # raise Exception("ngu qua")
            # curr.show()
            return None
        ga = GA(domainTraivered=curr.domainTravered, parrentdistance=curr.currDistance, fromParrentVertice=curr.currVertice,
                param=self.param, parrent=curr)
        ga.init() # add child node to curr
        #Simulation
        ga.run()
        ga.branchAndCut()
    
    def backpropagation(self, curr: Node, addN):
        # update Q, N, terminate, minDis, minQ, maxQ
        if curr == None:
            return
        # update Q:
        _min = INFINITE
        _max = -INFINITE
        _Q = -INFINITE
        _minDis = INFINITE
        for _d in curr.childs:
            curr.Q = max(curr.Q, curr.childs[_d].Q)
            _min = min(_min, curr.childs[_d].Q)
            _max = max(_max, curr.childs[_d].Q)
            _minDis = min(_minDis, curr.childs[_d].minDis)
        curr.minQ = _min
        curr.maxQ = _max
        curr.minDis = _minDis
        _par = curr.par
        curr.n += addN
        if curr.checkTerminate():
            _d = curr.d
            if _par!=None:
                del _par.childs[_d]
                _par.Q = -INFINITE
                for _d in _par.childs:
                    _par.Q = max(_par.Q, _par.childs[_d].Q)
        self.backpropagation(_par, addN)
    def run(self, STEP, testName = None, fileResult=None):
        if fileResult:
            fileResult.write("Steps "+ testName +"\n")
        depth = 0
        _maxDepth = 0
        for step in range(STEP):
            # print(f"STEP {step}")
            currNode = self.selection()
            _maxDepth = max(_maxDepth, depth)
            depth = len(currNode.domainTravered) or _maxDepth
            # print(currNode.domainTravered)
            # self.root.showChilds()
            # _bestValue = - INFINITE
            # _bestNode = None
            # Qlist = []
            # Hlist = []
            # for domain in self.root.childs:
            #     if not self.root.childs[domain].isTerminal:
            #         Qlist.append(self.root.childs[domain].Q)
            #         Hlist.append(self.root.childs[domain].minDis)
            # if len(Qlist)>0:
            #     _Qmean, _Qstd = self.getStat(Qlist)
            #     _Hmean, _Hstd = self.getStat(Hlist)
            #     for domain in self.root.childs:
            #         if not self.root.childs[domain].isTerminal:
            #             # _temp = self.UCT1(self.root, self.root.childs[domain], _std, _mean)
            #             _temp = self.UCT1(self.root, self.root.childs[domain], _Qstd, _Qmean, _Hmean, _Hstd)
            #             self.root.childs[domain].show()
            #             print("----Utc: "+ str(_temp))
            #             if _temp > _bestValue:
            #                 _bestValue = _temp
            #                 _bestNode = self.root.childs[domain]
    
            # if _bestNode!=None:
            #     _bestNode.show()
            self.expandAndSimulation(currNode)
            _addN = len(currNode.childs)
            self.backpropagation(currNode, _addN)
            if fileResult:
                fileResult.write(str(step) + " " + str(self.param.best) + " " + str(depth) + "\n")
        return self.param.best
    
if __name__ =="__main__":
    TEST_PATH = "IDPC-DU\\set1\\idpc_10x5x425.idpc"
    # TEST_PATH = "IDPC-DU\\set1\\idpc_10x10x1000.idpc"
    TEST_PATH = "IDPC-DU\\set2\\idpc_100x100x1000000.idpc"
    # TEST_PATH = "IDPC-DU\\set2\\idpc_100x200x2296097.idpc"
    # TEST_PATH = "IDPC-DU\\set1\\idpc_45x90x322081.idpc"  # hard tesst
    # TEST_PATH = "IDPC-DU\\set1\\idpc_20x20x8000.idpc"
    import sys
    # sys.stdout = open("output.txt", "w")
    tree = MontecarloTreeSearch(TEST_PATH)
    print(tree.run(250))