import pandas as pd

data = pd.read_excel("lechua.xlsx", header=None)
def mod(lline):
    ll = ""
    n = ""
    for i in lline:
        if i.isnumeric():
            n += i
        else:
            if n.isnumeric():
                aaa = int(n) + 1
                ll += str(aaa)
            n = ""
            ll += i
    return ll
data[2] = data[2].apply(mod)
print(data[2])
data.to_excel("new2021.xlsx")