
TEST_PATH = "IDPC-DU\\test.txt"
# T = "IDPC-DU\\set2\\idpc_100x200x2296097.idpc"
class Param():
    def __init__(self):
        self.G = []
        self.N = self.D = self.s = self.t = -1
    def buildGraph(self, path):
        with open(path) as f:
            l1 = f.readline()
            self.N, self.D = (int(i) for i in l1.split(" "))
            print(self.N, self.D)
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
            for line in edges:
                index += 1
                u, v, w, d = (int(i) for i in line.split(" "))
                u -= 1
                v -= 1
                d -= 1
                self.G[u][d].append((w, v))
            return self.G
if __name__ == "__main__":
    t = Param()
    print(t.buildGraph(TEST_PATH))
    # print(t.buildGraph(T))