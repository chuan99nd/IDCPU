from GetParam import Param, random, INFINITE, np
from heapq import heappush, heappop
from queue import PriorityQueue
import time
class Individual():
    def __init__(self, param: Param):
        self.param = param
        self.G = param.G
        self.geneSize = param.D
        self.cost = 0
        self.genes = np.zeros((param.D,), dtype=np.int32)
        self.isEval = False

        self.kount = 0

    def init(self):
        self.genes = np.random.permutation(self.param.D)
        self.eval()
    def isValidGene(self):
        s = set(self.genes)
        if len(s) == len(self.genes):
            return True
        return False
    
    def eval(self):
        if self.isEval:
            return self.cost
        distance = np.full((self.param.N,), INFINITE, dtype=np.int64)
        duyet = np.full((self.param.N,), False)
        distance[self.param.s] = 0

        currQueue = list()
        currColorIndex = 0
        heappush(currQueue,(0, self.param.s))
        while len(currQueue) > 0 and currColorIndex < self.param.D:
            tmpDuyet = []
            nextQueue = []
            while len(currQueue)>0:
                d_v, v= heappop(currQueue)
                self.kount += 1
                if duyet[v]:
                    continue
                distance[v] = min(d_v, distance[v])
                duyet[v] = True
                tmpDuyet.append(v)
                for w, u in self.G[v][self.genes[currColorIndex]]:
                    if not duyet[u]:
                        heappush(currQueue,(d_v+w, u))
                if currColorIndex +1 < self.param.D:
                    for w, u in self.G[v][self.genes[currColorIndex+1]]:
                        _thisvar = d_v +w
                        if distance[u] > _thisvar:
                            distance[u] = _thisvar
                            heappush(nextQueue,(_thisvar, u))
            currQueue = nextQueue
            currColorIndex += 1
            for i in tmpDuyet:
                duyet[i] = False
        self.isEval = True
        self.cost = distance[self.param.t]
        return self.cost

    def fake(self):
        if self.isEval:
            return self.cost
        distance = np.full((self.param.N,), float('inf'))
        duyet = np.full((self.param.N,), False)
        distance[self.param.s] = 0
        trace = [(-1, -1,-1, 0)]*self.param.N
        q = PriorityQueue()
        q.put((0,self.param.s, -1, -1, 0))
        while (not q.empty()):
            d_v, v, _t, _c,_w = q.get()
            if duyet[v]:
                continue
            duyet[v] = True
            trace[v] = (_t, _c, _w)
            distance[v] = min(d_v, distance[v])
            for i in range(self.param.D):
                for pair in self.G[v][i]:
                    w, u = pair
                    if not duyet[u]:
                        q.put((d_v+w, u, v, i,w))
                        # print((d_v+w, u, v, i))
        return (distance[self.param.t], trace)

    def processTrace(self, trace, u, v):
        end = v
        s = set()
        l = []
        last = -1
        while trace[end] != (-1, -1, 0):
            u, c, w = trace[end]
            print(f"{u} -> {end}: {w} color {c}")
            end = u
            if c!= last:
                if c in s:
                    print("Fail")
                    return
                else:
                    last = c
                    l.append(c)
                    s.add(c)
        print("True")
        print(s)
        l.reverse()
        print(l)
    def show(self):
        print(self.genes)
if __name__ == "__main__":
    # TEST_PATH = "IDPC-DU\\test.txt"
    # TEST_PATH = "IDPC-DU\\set1\\idpc_10x10x1000.idpc"
    TEST_PATH = "IDPC-DU\\set1\\idpc_10x5x425.idpc"
    TEST_PATH = "IDPC-DU\\set1\\idpc_45x22x43769.idpc"
    TEST_PATH = "IDPC-DU\\set1\\idpc_10x10x1000.idpc"
    TEST_PATH = "IDPC-DU\\set1\\idpc_20x20x8000.idpc"
    TEST_PATH = "IDPC-DU\\set1\\idpc_45x90x322081.idpc"

    t = Param()
    t.buildGraph(TEST_PATH)
    from itertools import permutations
    ll = []
    for i in range(t.D):
        ll.append(i)
    # per = permutations(ll)
    # res = float('inf')
    # iii = 0
    # for gene in per:
    #     i = Individual(t)
    #     i.genes = gene
    #     # print(i.eval())]
    #     if i.eval()==7:
    #         print(gene)
    #     res = min(res, i.eval())
    #     iii += 1
    #     if iii%10000==0:
    #         print(f'{iii}/{res}')
            # print(gene)
    i = Individual(t)
    res, trace = i.fake()
    i.processTrace(trace, i.param.s, i.param.t)
    print(res)

