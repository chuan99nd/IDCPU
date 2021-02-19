
import random
"""
Hyperparameter
"""
COVERAGE = 200
POPSIZE = 200
MAX_POPSIZE = 300
PROP =  0.4
PC = 0.95
PM = 0.1

INFINITE = 100000000
class Param():
    def __init__(self):
        self.G = []
        self.N = self.D = self.s = self.t = -1
        self.best = INFINITE
    def buildGraph(self, path):
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
if __name__ == "__main__":
    TEST_PATH = "IDPC-DU\\set1\\idpc_45x22x43769.idpc"
    t = Param()
    t.buildGraph(TEST_PATH)
    r = set()
    kkk = 0
    for u in range(t.N):
        for i in range(t.D):
            for aa in t.G[u][i]: 
                w,d = aa
                if w < 46:
                    r.add(d)
                    kkk+= 1
                    print (f"{u} -> {i} in domain {d} : {w}")

    print(len(r), kkk)