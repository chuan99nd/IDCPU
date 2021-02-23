import numpy as np
from GetParam import Param, INFINITE, random
from heapq import heappush, heappop
SCALE = 100
class Enviroment():
    def __init__(self, param: Param):
        self.param = param
        self.G = self.param.G
        self.N = self.param.N
        self.D = self.param.D
        self.bestCost = INFINITE
        # reset
        self.reset()

    def reset(self):
        self.duyetDomain = np.full((self.D+1,), False)
        self.duyetDinh = np.full((self.N,), False)
        self.distance = np.full((self.N,), INFINITE)
        self.distance[self.param.s] = 0

        self.currColor = self.D
        self.currMeanDistance = 0
        self.currQueue = []
        self.nextQueue = np.full((self.N,), 0)
        heappush(self.currQueue,(0, self.param.s))

    """
    domain: domain se di vao tiep theo
    return: Terminate, reward
    """
    def act(self, domain:int):
        self.currColor = domain
        if self.duyetDomain[domain]:
            if self.distance[self.param.t] >= INFINITE:
                return True, -INFINITE
            else:
                self.bestCost = min(self.bestCost, self.distance[self.param.t])
                return True, self.currMeanDistance - self.distance[self.param.t]*SCALE
        self.duyetDomain[domain] = True
        ###### eval
        # push to domain
        for v in range(self.N):
            if self.nextQueue[v] != 0:
                for w, u in self.G[v][domain]:
                    _tempDis = self.nextQueue[v] + w
                    # long time
                    # if _tempDis < self.distance[u]:
                    heappush(self.currQueue, (_tempDis, u))
                self.nextQueue[v] = 0
    
        ## check terminate
        if len(self.currQueue)==0:
            if self.distance[self.param.t] >= INFINITE:
                return True, -INFINITE
            else:
                self.bestCost = min(self.bestCost, self.distance[self.param.t])
                return True, self.currMeanDistance - self.distance[self.param.t]*SCALE
        
        tmpDuyet = []
        while len(self.currQueue)>0:
            d_v, v= heappop(self.currQueue)
            if self.duyetDinh[v]:
                continue
            self.distance[v] = min(d_v, self.distance[v])
            self.duyetDinh[v] = True
            tmpDuyet.append(v)
            for w, u in self.G[v][domain]:
                if not self.duyetDinh[u]:
                    heappush(self.currQueue,(d_v+w, u))
            # if d_v < self.bestCost: #branch and cut
            self.nextQueue[v] = d_v
        _sum = 0
        for i in tmpDuyet:
            self.duyetDinh[i] = False
            _sum += self.distance[i]
        _avr = _sum/len(tmpDuyet)
        reward = self.currMeanDistance - _avr
        self.currMeanDistance = _avr
        #######################
        #test
        assert(self.currMeanDistance<float("inf"))
        #########
        return False, reward

class Agent():
    def __init__(self, param:Param, env: Enviroment):
        self.param = param
        self.env = env
        self.Qtable = np.full((param.D+1, param.D), -INFINITE)
        self.N = self.param.N
        self.D = self.param.D

        self.lr = 0.1
        self.discount = 0.9
        self.eps = 0.3
        self.MAX_EPOCH = 1000

    def nextAction(self):
        currColor = self.env.currColor
        _duyet = []
        res = []
        for c in range(self.D):
            if not self.env.duyetDomain[c]:
                _duyet.append(c)
                if len(res) == 0 or self.Qtable[currColor][c] > res[0]:
                    res = [c]
                elif self.Qtable[currColor][c] == res[0]:
                    res.append(c)
        if len(res) ==0:
            # print("random when none")
            print(_duyet)
            return currColor, random.randint(0,self.D-1)
        pe = random.random()
        if pe < self.eps:
            # print("explore")
            return currColor, _duyet[random.randint(0, len(_duyet)-1)]
        else:
            # print("learning")
            return currColor, res[random.randint(0, len(res)-1)]

    def updateQ(self, node, action, reward):
        ## bellman equation
        maxxValue = np.amax(self.Qtable[action])
        self.Qtable[node][action] = (1-self.lr)*self.Qtable[node][action] + self.lr*(reward + self.discount*maxxValue)
    
    def learn(self):
        for epoch in range(self.MAX_EPOCH):
            self.env.reset()
            terminated = False
            while not terminated:
                _currColor, _act = self.nextAction()
                terminated, reward = self.env.act(_act)
                self.updateQ(_currColor, _act, reward)
                # print(f"     reward: {reward}" )
                # self.show()
            
            ## debug
            print(f"Epoch: {epoch} best cost " + str(self.env.bestCost))

    def findPath(self):
        self.eps = 0
        self.env.reset()
        terminated = False
        while not terminated:
            _currColor, _act = self.nextAction()
            terminated, reward = self.env.act(_act)
            self.updateQ(_currColor, _act, reward)
            # print(f"     reward: {reward}" )
            # self.show()  
        ## debug
        print(f"Best cost " + str(self.env.bestCost))


    def show(self):
        domain_list = list(np.where(self.env.duyetDomain))
        print("     Domain " + str(domain_list))
        print("     Current mean distance: " + str(self.env.currMeanDistance))
        print("++++++++++++++++++++++++++++")
        print(self.Qtable)

if __name__=="__main__":
    print("Begin debug --------------------------------------------")
    TEST_PATH = "IDPC-DU\\set1\\idpc_10x5x425.idpc"
    TEST_PATH = "IDPC-DU\\set1\\idpc_45x22x43769.idpc"
    p = Param()
    p.buildGraph(TEST_PATH)
    env = Enviroment(p)
    agent = Agent(p, env)
    agent.learn()
    agent.findPath()
            
