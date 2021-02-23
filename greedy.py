from GetParam import Param, random, INFINITE
import numpy as np
from queue import heappop, heappush

class GreedyRandom():
    def __init__(self, param:Param):
        self.param = param
        self.N = param.N
        self.D = param.D
        self.s = param.s
        self.t = param.t
        self.G = param.G
        random.seed(0)

    def run(self, show = False):
        _currDis = np.full((self.N,), INFINITE)
        _currDis[self.s] = 0
        _currList = np.full((self.N,), False)
        _currList[self.s] = True
        _currRand = INFINITE
        _ssss = 0
        duyetDomain = np.full((self.D,), False)
        while(True):
            _bestState = None
            _currRand = INFINITE
            _bestColor = INFINITE
            for _color in range(self.D):
            # for _color in range(4,5):
                if duyetDomain[_color]:
                    continue
                _temp = self.stat(_currDis, _currList, _color)
                _tempMin, _tempMax, _tempDis, _tempVertice = _temp
                self.param.best = min(self.param.best, _tempDis[self.t])
                # print(f"-----Temp {_color}: {_tempMin} {_tempMax}")
                if self.param.best > _tempMin:
                    _tempRand = random.randint(_tempMin, _tempMax)
                    # print(f"--------Get rand: {_tempRand}")
                    if _currRand > _tempRand:
                        _currRand = _tempRand
                        _bestState = _temp
                        _bestColor = _color
            if not _bestState:
                break
            duyetDomain[_bestColor] = True
            _minnnn, _maxxxx, _currDis, _currList = _bestState
            if show:
                print(duyetDomain)
                print(f"    Step {_ssss} chose color: {_bestColor}")
                print(_minnnn,_maxxxx)
                print(_currDis)
            _ssss += 1
        return min(_currDis[self.t], self.param.best)

    # return min max dis array, list of next vetice
    def stat(self, preDis: np.array, preVertice: np.array, nextColor):
        dis = np.full((self.N,), INFINITE)
        duyet = np.full((self.N,), False)
        currQueue = []
        for v in range(self.N):
            if preVertice[v]:
                for w, u in self.G[v][nextColor]:
                    heappush(currQueue, (preDis[v] + w, u))
        
        #process
        _min, _max = INFINITE, -INFINITE
        while(len(currQueue)>0):
            d_v, v = heappop(currQueue)
            if duyet[v]:
                continue
            duyet[v] = True
            dis[v] = min(dis[v], d_v)
            _min = min(dis[v], _min)
            _max = max(dis[v], _max)
            for w, u in self.G[v][nextColor]:
                if not duyet[u]:
                    heappush(currQueue, (d_v+w, u))
        
        if _min >= self.param.best:
            return INFINITE, INFINITE, dis, duyet
        else:
            return _min, _max, dis, duyet
        
if __name__=="__main__":
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
    print()
    print()
    print()
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

    # TEST_PATH = "IDPC-DU\\set1\\idpc_10x5x425.idpc"
    TEST_PATH = "IDPC-DU\\set1\\idpc_45x22x43769.idpc"
    TEST_PATH = "IDPC-DU\\set1\\idpc_15x7x1504.idpc"
    TEST_PATH = "IDPC-DU\\set1\\idpc_45x90x322081.idpc"
    p = Param()
    p.buildGraph(TEST_PATH)
    ####
    t = p
    # for u in range(t.N):
    #     for i in range(t.D):
    #         for aa in t.G[u][i]: 
    #             w,d = aa
    #             if w < 13:
    #                 print (f"{u} -> {d} in domain {i} : {w}")


    gr = GreedyRandom(p)
    for i in range(10000):
        print("Epoch " + str(i) + " value : " + str(gr.run(show=False)))