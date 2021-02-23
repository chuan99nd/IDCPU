from GetParam import Param, random
from GetParam import (COVERAGE, MAX_POPSIZE,PROP,
                      PM, PC, POPSIZE)
from Individual import Individual
import numpy as np

def compare(ind: Individual):
    return ind.eval()
class GA():
    def __init__(self, dataPath):
        self.param = Param()
        self.param.buildGraph(dataPath)
        self.D = self.param.D
        self.N = self.param.N
        self.pop = list()
    def init(self):
        for i in range(POPSIZE):
            ind = Individual(self.param)
            ind.init()
            self.pop.append(ind)
    
    def mutate(self, ind: Individual):
        i1 = random.randint(0, self.D-1)
        i2 = random.randint(0, self.D-1)
        while(i2==i1):
            i2 = random.randint(0, self.D-1)
        ind.genes[i1], ind.genes[i2] = ind.genes[i2], ind.genes[i1]
        ind.eval()
        return ind
    
    def crossover(self, par1: Individual, par2: Individual):
        i1 = random.randint(0, self.D-1)
        i2 = random.randint(0, self.D-1)
        if i1 > i2:
            i1, i2 = i2, i1
        ##TPX and PMX:
        child1 = Individual(self.param)
        child2 = Individual(self.param)
        ## swap p1 p2
        _index1 = np.full((self.D,), -1)
        _index2 = np.full((self.D,), -1)

        for _id in range(i1, i2+1):
            child1.genes[_id] = par1.genes[_id]
            _index1[child1.genes[_id]] = _id

            child2.genes[_id] = par2.genes[_id]
            _index2[child2.genes[_id]] = _id
        for _id in range(self.D):
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
        child1.eval(), child2.eval()
        return child1, child2
                
    def run(self, show=True):
        self.init()
        for generation in range(COVERAGE):
            self.pop.sort(key=compare)
            newPop = self.pop[0:int(POPSIZE*PROP)]
            while (len(newPop) < POPSIZE):
                # print(len(newPop))
                i1 = random.randint(0, POPSIZE-1)
                i2 = random.randint(0, POPSIZE-1)
                while(i1==i2):
                    i2 = random.randint(0,POPSIZE-1)
                # print(i1,i2, len(self.pop))
                c1, c2 = self.crossover(self.pop[i1], self.pop[i2])
                _prop = random.random()
                if (_prop < PM):
                    self.mutate(c1)
                    self.mutate(c2)
                newPop.append(c1)
                newPop.append(c2)
                # print(len(newPop))
            self.pop = newPop
            if show:
                print("Generation " + str(generation) + " : " + str(self.pop[0].eval()))
                # print(self.pop[0].kount)
                # for indddd in self.pop:
                #     indddd.show()
                # print([iii.eval() for iii in self.pop] )
        return self.pop[0].eval()
if __name__ == "__main__":
    # TEST_PATH = "IDPC-DU\\set1\\idpc_10x5x425.idpc"
    # TEST_PATH = "IDPC-DU\\set1\\idpc_35x17x13934.idpc"
    TEST_PATH = "IDPC-DU\\set1\\idpc_45x90x322081.idpc"
    # TEST_PATH = "IDPC-DU\\set1\\idpc_45x22x43769.idpc"
    # TEST_PATH = "IDPC-DU\\set1\\idpc_25x25x15625.idpc"
    # TEST_PATH = "IDPC-DU\\set1\\idpc_10x10x1000.idpc"
    # TEST_PATH = "IDPC-DU\\set1\\idpc_20x20x8000.idpc"
    t = Param()
    t.buildGraph(TEST_PATH)
    ga = GA(TEST_PATH)
    # p1 = Individual(t)
    # p1.init()
    # print(p1.genes)
    # ga.mutate(p1)
    # print(p1.genes)
    # import time
    # start_time = time.time()
    # N = 1
    # for i in range(N):
    #     ga.run(show=True)
    # print("total time: " + str((time.time()-start_time)/N))
    # # print(p1.eval())
    # print(int(p1.kount/N))
    for i in range(1):
        p1 = Individual(t)
        p1.init()
        p2 = Individual(t)
        p2.init()
        c1, c2 = ga.crossover(p1,p2)
        if c1.isValidGene():
            p1.show()
            p2.show()
            c1.show()
            c2.show()
    
    
    ga.run(show=True)


        


