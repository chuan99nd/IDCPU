from GetParam import Param, INFINITE, random, COVERAGE, POPSIZE, PC, PM, PROBABILITY, PROP
from MiniIndividual import Individual
from GetParam import numpy as np

class Node():
    def __init__(self, d, par: Node, param:Param):
        self.d = d
        self.Q = -INFINITE
        self.minQ = None
        self.maxQ =None
        self.n = 0

        self.minDis = None
        self.currDistance = None  # (N,) distance from s to v in colorpath of node
        self.currVertice = None  # v TRue false if xet cac dinh ke vs v
        self.domainTravered = None # array cac domain da duyet
        self.isTerminal = False
        self.param = param

        self.childs = {} # {v: node(v)}
        self.par = par
    def checkTerminate(self):
        if not self.isTerminal:
            if self.minDis >= self.param.best or len(self.childs)==0:
                self.isTerminal = True
        return self.isTerminal