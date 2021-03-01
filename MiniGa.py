from GetParam import Param, INFINITE, random, COVERAGE, POPSIZE, PC, PM, PROBABILITY, PROP
from MiniIndividual import Individual
from GetParam import numpy as np
from Node import Node
def compare(ind: Individual):
    return ind.eval()

class GA():
    # fromparrentVertice: cac dinh da dc duyet tu truoc
    # parrent distance: khoang cach da duowc duyet tu truoc
    # domaintraivered true false all vertice
    def __init__(self, domainTraivered: np.array, parrentdistance: np.array, fromParrentVertice: np.array,param: Param, parrent: Node):
        self.parrentDistance = parrentdistance;
        self.param = param
        _daDuyet = np.full((self.param.D,), False)
        self.chuaDuyet = []
        for d in domainTraivered:
            _daDuyet[d] = True
        for d in _daDuyet:
            self.chuaDuyet.append(d)
        self.fromParrentVertice = fromParrentVertice
        self.pop = []
        self.parrent = parrent
        #set prob for gene
        self.prob = [1/(i+PROBABILITY) for i in range(len(self.chuaDuyet))]
        _sum = sum(self.prob)
        self.prob = [i/_sum for i in self.prob]

    def init(self):
        for d in self.chuaDuyet:
            ind = Individual(self.parrentDistance, self.chuaDuyet, self.param, self.fromParrentVertice)
            ind.init(d)
            _node = Node(d, parrent, self.param)
            ind.eval()
            self.Q = max(-ind.eval(), self.Q)
            self.pop.append(ind)
            self.parrent.childs[v] = _node

    def mutate(self, ind:Individual):
        i1, i2 = np.random.choice(ind.geneSize, 2, p=self.prob, replace=True)
        if i1 > i2:
            i1,i2 = i2, i1
        ind.genes[i1], ind.genes[i2] = ind.genes[i2], ind.genes[i1]
        ind.eval(self.parrent)
        return ind

    def crossover(self, par1: Individual, par2: Individual):
        i1, i2 = np.random.choice(par1.geneSize, 2, p=self.prob, replace=False)
        if i1 > i2:
            i1, i2 = i2, i1
        ##TPX and PMX:
        child1 = Individual(self.currDistance,self.chuaDuyet, self.param, self.fromParrentVertice)
        child2 = Individual(self.currDistance,self.chuaDuyet, self.param, self.fromParrentVertice)
        ## swap p1 p2
        _index1 = np.full((par1.geneSize,), -1)
        _index2 = np.full((par2.geneSize,), -1)

        for _id in range(i1, i2+1):
            child1.genes[_id] = par1.genes[_id]
            _index1[child1.genes[_id]] = _id

            child2.genes[_id] = par2.genes[_id]
            _index2[child2.genes[_id]] = _id
        for _id in range(par1.param):
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
        # child1.eval(), child2.eval()
        return child1, child2

    def run(self, show = False):
        for generation in range(COVERAGE):
            self.pop.sort(key=compare)
            newPop = self.pop[0:int(POPSIZE*PROP)]
            while (len(newPop) < POPSIZE):
                # print(len(newPop))
                i1, i2 = np.random.choice(len(self.pop), 2, p=self.prob, replace=True)
                # print(i1,i2, len(self.pop))
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
                print("Generation " + str(generation) + " : " + str(self.pop[0].eval()))
                # print(self.pop[0].kount)
                # for indddd in self.pop:
                #     indddd.show()
                # print([iii.eval() for iii in self.pop] )
        return self.pop[0].eval()
