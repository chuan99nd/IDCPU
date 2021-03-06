
import random
import os
from os import path
import numpy as np
"""
Hyperparameter
"""
COVERAGE = 100
POPSIZE = 500
MAX_POPSIZE = 1200
PROP =  0.05
PC = 0.95
PM = 0.3

INFINITE = 100000000
class Param():
    def __init__(self):
        self.G = []
        self.N = self.D = self.s = self.t = -1
        self.best = INFINITE
    def buildGraph(self, path):
        self.best = INFINITE
        with open(path) as f:
            l1 = f.readline()
            self.N, self.D = (int(i) for i in l1.split(" "))
            l2 = f.readline()
            self.s, self.t = (int(i) for i in l2.split(" "))
            self.s -= 1
            self.t -= 1
            edges = f.readlines()
            for node in range(self.N):
                temp = []
                for domain in range(self.D):
                    temp.append([])
                self.G.append(temp)
            index = 0
            #modify
            modify = dict()
            for line in edges:
                index += 1
                u, v, w, d = (int(i) for i in line.split(" "))
                u -= 1
                v -= 1
                d -= 1
                if (u,v,d) in modify.keys():
                    modify[(u,v,d)] = min(modify[(u,v,d)], w)
                else:
                    modify[(u,v,d)]=w
            for key in modify:
                u,v,d = key
                w = modify[key]
                self.G[u][d].append((w,v))
            return self.G

def getTestPath(rootFolder="IDPC-DU", testSet = ["set1", "set2"]):
    testPath = []
    for setName in testSet:
        setPath = path.join(rootFolder, setName)
        for t in os.listdir(setPath):
            testPath.append((setName, t, path.join(setPath, t)))
    return testPath

if __name__ == "__main__":
    # TEST_PATH = "IDPC-DU\\set1\\idpc_45x22x43769.idpc"
    # t = Param()
    # t.buildGraph(TEST_PATH)
    # r = set()
    # kkk = 0
    # for u in range(t.N):
    #     for i in range(t.D):
    #         for aa in t.G[u][i]: 
    #             w,d = aa
    #             if w < 46:
    #                 r.add(d)
    #                 kkk+= 1
    #                 print (f"{u} -> {i} in domain {d} : {w}")

    # print(len(r), kkk)
    getTestPath()