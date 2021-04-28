import pandas as pd
from os import path
import os
import time
import datetime
set_list = ["set1", "set2"]
root_dir = "Result"
# df = pd.DataFrame(columns=["set","file", "cost","time"])
data =  {
        "set":[],
        "file":[],
        "cost":[],
        "avg":[],
        "std":[],
        "time":[]
    }
for sett in set_list:
    d = path.join(root_dir, sett)
    for test in os.listdir(d):
        test_name = test.split(".")[0]
        # print(test_name)
        fit = []
        TT = []
        for seed in os.listdir(path.join(d, test)):
            ext = seed.split(".")[2]
            # print(ext)
            if ext == "opt":
                f = open(path.join(d, test, seed))
                content = f.read()
                fittness = int(content.split()[5])
                t = content.split()[7]
                x = time.strptime(t, '%H:%M:%S')
                T = datetime.timedelta(hours=x.tm_hour,minutes=x.tm_min,seconds=x.tm_sec).total_seconds()
                TT.append(T)
                # print(fittness)
                fit.append(fittness)
        avg = sum(fit)/len(fit)
        bp = [(a-avg)**2 for a in fit]
        std = sum(bp)/len(fit)
        std =std**0.5
        minn = min(fit)
        tttt = sum(TT)/len(TT)
        # print(test_name, avg, std, minn, tttt)
        data["set"].append(sett)
        data["file"].append(test_name)
        data["cost"].append(minn)
        data["std"].append(std)
        data["avg"].append(avg)
        data["time"].append(tttt)
df = pd.DataFrame(data)
df.to_csv("stat.csv")
    
