from GetParam import *
import time
import pandas as pd
from MontecarloTreeSearch import MontecarloTreeSearch

# df = pd.DataFrame(columns=["set","file", "cost","time"])
data =  {
        "set":[],
        "file":[],
        "cost":[],
        "time": []
    }
f = open("result.txt","w+")
for setName, fileName, filePath in getTestPath(testSet=["set2"]):
    print(fileName)
    startTime = time.time()
    t = MontecarloTreeSearch(filePath)
    best = t.run(1000)
    endTime = time.time()
    row = {
        "set":setName,
        "file":fileName,
        "cost":best,
        "time":int(endTime-startTime)
    }
    data["set"].append(setName)
    data["file"].append(fileName)
    data["cost"].append(best)
    data["time"].append(int(endTime-startTime))
    f.write(str(row) + "\n")
    print(row)

df = pd.DataFrame(data)
print(df)
df.to_csv("result.csv")
print("Done!")