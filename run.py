from GetParam import *
import time
from MontecarloTreeSearch import MontecarloTreeSearch
import pandas as pd
import os
import sys
# df = pd.DataFrame(columns=["set","file", "cost","time"])
# print(sys.argv)
l, h = (int(i) for i in sys.argv[1:])
if not h:
    raise Exception("None parameter")
data =  {
        "set":[],
        "file":[],
        "cost":[],
        "time": []
    }
f = open("result.txt","w+")
resultRoot = "Result"
for shit in range(l, h):
    for setName, fileName, filePath in getTestPath():
        resultPath = os.path.join(resultRoot, setName, fileName)
        try:
            os.makedirs(resultPath,exist_ok = True)
        except:
            pass
        random.seed(shit)
        np.random.seed(shit)
        genFile = fileName + "_seed_" + str(shit) + ".gen"
        optFile = fileName + "_seed_" + str(shit) + ".opt"
        print(fileName)
        print(f"shit {l} -> {h}")
        startTime = time.time()
        gen = open(os.path.join(resultPath, genFile), "w+")
        t = MontecarloTreeSearch(filePath)
        best = t.run(STEP, testName=fileName, fileResult=gen)
        endTime = time.time()
        strTIme = time.strftime("%H:%M:%S", time.gmtime(int(endTime-startTime)))
        opt = open(os.path.join(resultPath, optFile), "w+")
        content =  f"""Filename: {fileName}
Seed: {shit}
Fitness: {best}
Time: {strTIme}"""
        opt.write(content)
        opt.close()
        gen.close()
        # row = {
        #     "set":setName,
        #     "file":fileName,
        #     "cost":best,
        #     "time":int(endTime-startTime)
        # }
        # data["set"].append(setName)
        # data["file"].append(fileName)
        # data["cost"].append(best)
        # data["time"].append(int(endTime-startTime))
        # f.write(str(row) + "\n")

# df = pd.DataFrame(data)
# print(df)
# df.to_csv("result.csv")
# print("Done!")
