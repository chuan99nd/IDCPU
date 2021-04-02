from GetParam import *
from GA import *
import time
import pandas as pd
import os
# df = pd.DataFrame(columns=["set","file", "cost","time"])
data =  {
        "set":[],
        "file":[],
        "cost":[],
        "time": []
    }
f = open("result.txt","w+")
resultRoot = "Result"
for shit in range(30):
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
        startTime = time.time()
        ga = GA(filePath)
        gen = open(os.path.join(resultPath, genFile), "w+")
        best = ga.run(show=False, testName=fileName, fileResult=gen)
        endTime = time.time()
        strTIme = time.strftime("%H:%M:%S", time.gmtime(int(endTime-startTime)))
        opt = open(os.path.join(resultPath, optFile), "w+")
        content =  f""" Filename: {fileName}
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
