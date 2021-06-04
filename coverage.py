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

    
def showCost(oldMethod, newMethod):
    oldMethod = oldMethod[::5]
    newMethod = newMethod[::5]
    print(oldMethod)
    print(newMethod)
    t = np.arange(0, 250, 5)
    data1 = oldMethod
    data2 = newMethod

    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Step')
    ax1.set_ylabel('Formal Strategy cost',  color=color)
    ax1.plot(t, data1, marker="^", color=color, linestyle = "dashed")
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('Propose Strategy cost', color=color)  # we already handled the x-label with ax1
    ax2.plot(t, data2, "bo", color=color,linestyle = "dotted")
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()

def showDepth(oldMethod, newMethod):
    oldMethod = oldMethod[::5]
    newMethod = newMethod[::5]
    print(oldMethod)
    print(newMethod)
    t = np.arange(0, 250, 5)
    data1 = oldMethod
    data2 = newMethod

    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Step')
    ax1.set_ylabel('Formal Strategy depth',  color=color)
    ax1.plot(t, data1, color=color, linestyle = "dashed")
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('Propose Strategy depth', color=color)  # we already handled the x-label with ax1
    ax2.plot(t, data2,  color=color,linestyle = "dotted")
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()
pureMethodPath = "Analyst\\set1\\45x45x91125\\45x45x91125_seed_0.gen"
newMethodPath = "Result\set1\idpc_45x45x91125.idpc\idpc_45x45x91125.idpc_seed_0.gen"

pureC, pureD = readFile(pureMethodPath)
newC, newD = readFile(newMethodPath)
showCost(newC, pureC)
showCost(newD, pureD)