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
        self.genes = np.full((self.geneSize,), -1)
    def init(self, first, par = None):
        _index = np.random.permutation(self.geneSize)
        self.genes = self.chuaduyet[_index]
        for i in range(self.geneSize):
            if self.genes[i]==first:
                self.genes[i], self.genes[0] = self.genes[0], self.genes[i]
                break
        self.eval(par)

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
        distance = np.copy(preDistance)
        while len(currQueue) > 0 and currColorIndex < self.geneSize:
            tmpDuyet = []
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
        if parrent!=None:
            parrent.childs[self.genes[0]].Q = max(-self.cost, parrent.childs[self.genes[0]].Q)
            parrent.childs[self.genes[0]].n += 1
        return self.cost

    def getNodeInfo(self, parrent: Node):
        _color = self.genes[0]
        preDistance = parrent.currDistance
        fromParrentVertice = parrent.currVertice
        duyet = np.full((self.param.N,), False)

        currQueue = list()           
        for v in range(self.N):
            if fromParrentVertice[v] and self.param.best > preDistance[v]:
                for w, u in self.G[v][_color]:
                    heappush(currQueue, (preDistance[v]+w, u))

        distance = np.full((self.N,), INFINITE)
        # print(distance)
        while len(currQueue)>0:
            d_v, v= heappop(currQueue)
            if duyet[v]:
                continue
            distance[v] = min(d_v, distance[v])
            duyet[v] = True
            for w, u in self.G[v][_color]:
                if not duyet[u]:
                    heappush(currQueue,(d_v+w, u))
        _minDis = np.amin(distance)
        return distance, duyet, _minDis
        
if __name__ == "__main__":
    TEST_PATH = "IDPC-DU\\set1\\idpc_10x10x1000.idpc"
    # TEST_PATH = "IDPC-DU\\set1\\idpc_10x5x425.idpc"
    TEST_PATH = "IDPC-DU\\set1\\idpc_45x90x322081.idpc"
    TEST_PATH = "IDPC-DU\\set1\\idpc_20x20x8000.idpc"
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
        # ind.init(i%ind.geneSize)
        # print(ind.genes)
        # print(t.best)
        ind.genes = [45, 80, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199]
        # ind.eval()
        print("Eval " + str(ind.eval(None)))


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