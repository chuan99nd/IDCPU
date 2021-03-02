from GetParam import Param, INFINITE, random, COVERAGE, POPSIZE, PC, PM, PROBABILITY, PROP
from GetParam import np

class Node():
    def __init__(self, d, par, param:Param):
        self.d = d
        self.Q = -INFINITE
        self.minQ = None
        self.maxQ =None
        self.n = 0

        self.minDis = None
        self.currDistance = None  # (N,) distance from s to v in colorpath of node
        self.currVertice = None  # v TRue false if xet cac dinh ke vs v
        if par!= None:
            self.domainTravered = np.append(par.domainTravered, d) # array cac domain da duyet
        self.isTerminal = False
        self.param = param

        self.childs = {} # {v: node(v)}
        self.par = par
    def checkTerminate(self):
        if not self.isTerminal:
            if self.minDis >= self.param.best or len(self.childs)==0:
                self.isTerminal = True
        return self.isTerminal
    
    def show(self):
        print("--Color: "+str(self.domainTravered)+ " Q value: "+ str(self.Q) + " minDis: " + str(self.minDis) + " N: "+ str(self.n))
    
    def showChilds(self):
        print("Child node of "+ str(self.domainTravered))
        for d in self.childs:
            self.childs[d].show()