from GetParam import *
from GA import *
import time
import pandas as pd

# df = pd.DataFrame(columns=["set","file", "cost","time"])
data =  {
        "set":[],
        "file":[],
        "cost":[],
        "time": []
    }
f = open("result.txt","w+")
for setName, fileName, filePath in getTestPath():
    print(fileName)
    startTime = time.time()
    ga = GA(filePath)
    best = ga.run(show=False)
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

df = pd.DataFrame(data)
print(df)
df.to_csv("result.csv")
print("Done!")
