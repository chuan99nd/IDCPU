from GetParam import Param, INFINITE, random, COVERAGE, POPSIZE, PC, PM, PROBABILITY, PROP
from MiniIndividual import Individual
from GetParam import np
from Node import Node
def compare(ind: Individual):
    return ind.eval(None)

class GA():
    # fromparrentVertice: cac dinh da dc duyet tu truoc
    # parrent distance: khoang cach da duowc duyet tu truoc
    # domaintraivered true false all vertice
    # parrent node dang duyet de tinh GA
    def __init__(self, domainTraivered: np.array, parrentdistance: np.array, fromParrentVertice: np.array,param: Param, parrent: Node):
        self.parrentDistance = parrentdistance;
        self.param = param
        _daDuyet = np.full((self.param.D,), False)
        self.chuaDuyet = []
        for d in domainTraivered:
            _daDuyet[d] = True
        for d in range(self.param.D):
            if not _daDuyet[d]:
                self.chuaDuyet.append(d)
        self.chuaDuyet = np.array(self.chuaDuyet)
        self.fromParrentVertice = fromParrentVertice
        self.pop = []
        self.parrent = parrent
        #set prob for gene
        self.prob = [1/(i+PROBABILITY) for i in range(len(self.chuaDuyet))]
        _sum = sum(self.prob)
        self.prob = [i/_sum for i in self.prob]
        self.genSize = len(self.chuaDuyet)
    def init(self):
        self.parrent.minDis = INFINITE
        for d in self.chuaDuyet:
            ind = Individual(self.parrentDistance, self.chuaDuyet, self.param, self.fromParrentVertice)
            ind.init(d)
            # print(ind.genes)
            _node = Node(d, self.parrent, self.param)
            _node.n = 1
            _node.currDistance, _node.currVertice, _node.minDis = ind.getNodeInfo(self.parrent)
            self.parrent.minDis = min(self.parrent.minDis, _node.minDis)
            self.parrent.Q = max(-ind.eval(None), self.parrent.Q)
            self.pop.append(ind)
            self.parrent.childs[d] = _node

    def mutate(self, ind:Individual):
        for _ in range(5):
            i1, i2 = np.random.choice(ind.geneSize, 2, p=self.prob, replace=True)
            if i1 > i2:
                i1,i2 = i2, i1
            ind.genes[i1], ind.genes[i2] = ind.genes[i2], ind.genes[i1]
        ind.eval(self.parrent)
        return ind

    def crossover(self, par1: Individual, par2: Individual):
        # print("par1 : " + str(par1.genes))
        # print("par2 : " + str(par2.genes))

        i1, i2 = np.random.choice(par1.geneSize, 2, replace=False)
        if i1 > i2:
            i1, i2 = i2, i1
        ##TPX and PMX:
        child1 = Individual(self.parrentDistance,self.chuaDuyet, self.param, self.fromParrentVertice)
        child2 = Individual(self.parrentDistance,self.chuaDuyet, self.param, self.fromParrentVertice)
        ## swap p1 p2
        _index1 = np.full((self.param.D,), -1)
        _index2 = np.full((self.param.D,), -1)

        for _id in range(i1, i2+1):
            child1.genes[_id] = par1.genes[_id]
            _index1[child1.genes[_id]] = _id

            child2.genes[_id] = par2.genes[_id]
            _index2[child2.genes[_id]] = _id
        for _id in range(par1.geneSize):
            if i1 <= _id <= i2:
                continue
            _val = par2.genes[_id]
            _r = _index1[_val]
            while(_r != -1):
                _val = par2.genes[_r]
                _r = _index1[_val]
            child1.genes[_id] = _val
        
            _val = par1.genes[_id]
            _r = _index2[_val]
            while(_r != -1):
                _val = par1.genes[_r]
                _r = _index2[_val]
            child2.genes[_id] = _val
        return child1, child2

    def run(self, show = False):
        if self.genSize <= 1:
            return self.pop[0].eval(None)
        for generation in range(COVERAGE):
            self.pop.sort(key=compare)
            newPop = self.pop[0:int(POPSIZE*PROP)]
            while (len(newPop) < POPSIZE):
                i1, i2 = np.random.choice(len(self.pop), 2, replace=True)
                c1, c2 = self.crossover(self.pop[i1], self.pop[i2])
                _prop = random.random()
                if (_prop < PM):
                    self.mutate(c1)
                    self.mutate(c2)
                c1.eval(self.parrent), c2.eval(self.parrent)
                newPop.append(c1)
                newPop.append(c2)
            self.pop = newPop
            if show:
                print("Generation " + str(generation) + " : " + str(self.pop[0].eval(None)))
                # _bestfit = [ind.eval(None) for ind in self.pop]
                # print(_bestfit)
                # print(self.pop[0].kount)
                # for indddd in self.pop:
                #     indddd.show()
                # print([iii.eval() for iii in self.pop] )
        return self.pop[0].eval(None)
    def branchAndCut(self):
        for d in self.chuaDuyet:
            if self.parrent.childs[d].minDis >= self.param.best:
                del self.parrent.childs[d]
if __name__ =="__main__":
    TEST_PATH = "IDPC-DU\\set1\\idpc_10x5x425.idpc"
    TEST_PATH = "IDPC-DU\\set1\\idpc_10x10x1000.idpc"
    TEST_PATH = "IDPC-DU\\set1\\idpc_15x15x3375.idpc"
    # TEST_PATH = "IDPC-DU\\set1\\idpc_45x90x322081.idpc"
    # TEST_PATH = "IDPC-DU\\set1\\idpc_15x7x1504.idpc"
    # TEST_PATH = "IDPC-DU\\set1\\idpc_20x10x2492.idpc"
    TEST_PATH = "IDPC-DU\\set2\\idpc_100x200x2296097.idpc"
    param = Param()
    param.buildGraph(TEST_PATH)
    N = param.N
    G = param.G
    d = param.D

    ########################
    _root = Node(d=None, par=None, param=param)
    _root.currDistance = np.full((param.N,), INFINITE)
    _root.currDistance[param.s] = 0
    _root.currVertice = np.full((param.N,), False)
    _root.currVertice[param.s] = True
    _root.domainTravered = np.array([], dtype="int32")
    _root.minDis = -INFINITE
    _root.maxQ = INFINITE
    _root.minQ = -INFINITE

    ga = GA(domainTraivered=_root.domainTravered, parrentdistance=_root.currDistance, fromParrentVertice=_root.currVertice,
                param=param, parrent=_root)
    ga.init() # add child node to curr
    #Simulation
    ga.run(show=True)
    print(param.best)