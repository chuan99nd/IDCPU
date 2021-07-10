import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def readFile(path):
    f = open(path, "r")
    lines = f.readlines()
    costs = []
    depths = []
    for line in lines[1:]:
        step, cost, depth = (int(i) for i in line.split())
        # print(step, cost, depth)
        costs.append(cost)
        depths.append(depth)
    return costs, depths

def fakeList(l):
    r = []
    m = 10000
    for i in l:
        m = min(m, i)
        r.append(m)
    return r
def readTrashFile(path):
    f = open(path, "r")
    lines = f.readlines()
    costs = []
    depths = []
    for line in lines[1:]:
        step, cost = (int(i) for i in line.split())
        # print(step, cost, depth)
        costs.append(cost)
        # depths.append(depth)
    return costs

def showCost(oldMethod, newMethod): # shape 5000
    oldMethod = oldMethod[::100]
    newMethod = newMethod[::100]
    print(oldMethod)
    print(newMethod)
    t = np.arange(0, 50000, 1000)
    data1 = oldMethod
    data2 = newMethod

    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Số lần đánh giá')
    ax1.set_ylabel('Giá trị hàm mục tiêu')
    ax1.plot(t, data1, color=color, linestyle = "dashed",label= "GA")
    color = 'tab:blue'
    ax1.plot(t, data2, color=color,linestyle = "dotted", label = "GA-MCTS")
    # ax2.tick_params(axis='y', labelcolor=color)

    # fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.legend()
    plt.show()

################
gaMethodPath = "Analyst\\set1\\45x45x91125\\45x45x91125_seed_0.gen"
newMethodPath = "Analyst\\set1\\45x45x91125\\new.txt"
ga_cost = readTrashFile(gaMethodPath)
mc_cost = readTrashFile(newMethodPath)

for i in range(len(mc_cost), 5000):
    mc_cost.append(mc_cost[-1])
print(len(mc_cost))
print(len(ga_cost))
ga = []

for i in ga_cost:
    for _ in range(10):
        ga.append(i)

ga = fakeList(ga)
mc_cost = fakeList(mc_cost)
showCost(ga, mc_cost)

###########
gaMethodPath = "Analyst\\set2\\80x80x512000\\80x80x512000_seed_0.gen"
newMethodPath = "AnalystMC\\set2\\80x80x512000\\80x80x512000_seed_0.gen"
ga_cost = readTrashFile(gaMethodPath)
mc_cost = readTrashFile(newMethodPath)

for i in range(len(mc_cost), 5000):
    mc_cost.append(mc_cost[-1])
print(len(mc_cost))
print(len(ga_cost))
ga = []

for i in ga_cost:
    for _ in range(10):
        ga.append(i)

ga = fakeList(ga)
mc_cost = fakeList(mc_cost)
showCost(ga, mc_cost)
