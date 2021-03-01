from GetParam import Param, random, INFINITE
from GetParam import np
from heapq import heappush, heappop
from Node import Node
class Individual():
    # parrentDistance: N: kc tu s toi v
    # chuy duyet (gensize,): array cac domain chua duyet
    # from... true neu no nam trong tap cac node bien
    def __init__(self, parrentDistance: np.array, chuaDuyet: np.array, param: Param, fromParrentVertice: np.array):
        self.geneSize = len(chuaDuyet)
        self.parrentDistance = parrentDistance
        self.chuaduyet = chuaDuyet
        self.param = param
        self.fromParrentVertice = fromParrentVertice

        self.D = param.D
        self.N = param.N
        self.G = param.G
        self.isEval = False
        self.cost = INFINITE

    def init(self, first):
        _index = np.random.permutation(self.geneSize)
        self.genes = self.chuaduyet[_index]
        for i in range(self.geneSize):
            if self.genes[i]==first:
                self.genes[i], self.genes[0] = self.genes[0], self.genes[i]
                break
        self.eval()

    def eval(self, parrent: Node):
        if self.isEval:
            return self.cost

        preDistance = self.parrentDistance
        duyet = np.full((self.param.N,), False)

        currQueue = list()
        currColorIndex = 0
        nextQueue = list()
        
        for v in range(self.N):
            if self.fromParrentVertice[v]:
                for w, u in self.G[v][self.genes[currColorIndex]]:
                    heappush(currQueue, (preDistance[v]+w, u))

        while len(currQueue) > 0 and currColorIndex < self.geneSize:
            tmpDuyet = []
            distance = np.full((self.N,), INFINITE)
            # print(distance)
            while len(currQueue)>0:
                d_v, v= heappop(currQueue)
                if duyet[v]:
                    continue
                distance[v] = min(d_v, distance[v])
                duyet[v] = True
                tmpDuyet.append(v)
                for w, u in self.G[v][self.genes[currColorIndex]]:
                    if not duyet[u]:
                        heappush(currQueue,(d_v+w, u))
                if currColorIndex +1 < self.geneSize and d_v < self.param.best:
                    for w, u in self.G[v][self.genes[currColorIndex+1]]:
                        _thisvar = d_v +w
                        if distance[u] > _thisvar:
                            distance[u] = _thisvar
                            heappush(nextQueue,(_thisvar, u))
            currQueue = nextQueue
            nextQueue = []
            currColorIndex += 1
            for i in tmpDuyet:
                duyet[i] = False
            self.cost = min(self.cost, distance[self.param.t])
        self.isEval = True
        if self.param.best >= self.cost:
            self.param.best = self.cost
            self.param.indBest = self
        parrent.childs[self.genes[0]].Q = max(-self.cost, parrent.childs[self.genes[0]].Q)
        return self.cost

if __name__ == "__main__":
    TEST_PATH = "IDPC-DU\\set1\\idpc_10x10x1000.idpc"
    # TEST_PATH = "IDPC-DU\\set1\\idpc_10x5x425.idpc"
    t = Param()
    t.buildGraph(TEST_PATH)

    chuaDuyet = np.asarray([4,5,1,2,3])
    # print(chuaDuyet)
    ## init
    preVertice = np.full((t.N,), False)
    preVertice[t.s] = True
    preDistance = np.full((t.N,), INFINITE)
    preDistance[t.s] = 0
    chuaDuyet = np.arange(t.D)
    ind = Individual(preDistance, chuaDuyet, t, preVertice)
    for i in range(100):
        ind = Individual(preDistance, chuaDuyet, t, preVertice)
        ind.init(i%ind.geneSize)
        # print(ind.genes)
        # print(t.best)
        # ind.genes = [4,0,3,2,1]
        # target = np.array([4,1,3,2,0])
        # ind.eval()
        print("Eval " + str(ind.eval()))


    # from itertools import permutations
    # ll = []
    # for i in range(t.D):
    #     ll.append(i)
    # per = permutations(ll)
    # res = float('inf')
    # iii = 0
    # for gene in per:
    #     i = Individual(preDistance, chuaDuyet, t, preVertice)
    #     i.genes = gene
    #     # print(gene)
    #     # print(i.eval())
    #     if i.eval()==7:
    #         print("sdafasfas")
    #     res = min(res, i.eval())
    #     iii += 1
    #     if iii%10000==0:
    #         print(f'{iii}/{res}')
    #         print(gene)