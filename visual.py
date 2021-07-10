import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
df = pd.read_csv("stat.csv")
col = list(range(len(df)))
# df = df.append(col)
# df["chuan"] = col

# print(df)
col = ["S_" + str(i) if i <24 else "L_" + str(i) for i in col]
df["test_id"] = col
print(df.columns[1:])
df = df.drop(columns = df.columns[0:2])
# df.to_csv("final.csv", index=False)


collate_df = pd.read_csv("relate.csv")
# cac = [i.split(".")[0] for i in collate_df["file"]]
# collate_df["file"] = cac
# collate_df.to_csv("relate.csv")
print(len(df), len(collate_df))
final_df = pd.merge(left=collate_df, right=df, left_on="file", right_on="file", how="inner")
print(final_df)
# final_df.to_csv("chuan.csv")


def show(l, r):
    labels = list(final_df["test_id"][l:(r+l)//2])
    print(labels)
    best_MFEA = list(final_df["MFEA"][l:(r+l)//2])
    best_GA = list(final_df["cost"][l:(r+l)//2])
    best_propose = list(final_df["avg"][l:(r+l)//2])


    labels1 = list(final_df["test_id"][(r+l)//2: r])
    print(labels1)
    best_MFEA1 = list(final_df["MFEA"][(r+l)//2: r])
    best_GA1 = list(final_df["cost"][(r+l)//2: r])
    best_propose1 = list(final_df["avg"][(r+l)//2: r])

    x = np.arange(len(labels))  # the label locations
    width = 0.2 # the width of the bars

    fig, ax = plt.subplots(2)

    rects21 = ax[0].bar(x , best_MFEA, width, label='MFEA')
    rects11 = ax[0].bar(x-width , best_GA, width, label='GA')
    rects31 = ax[0].bar(x+width, best_propose, width, label="GA-MCTS")
    ax[0].set_xticks(x)

    x = np.arange(len(labels1))  # the label locations

    rects2 = ax[1].bar(x , best_MFEA1, width, label='MFEA')
    rects1 = ax[1].bar(x-width , best_GA1, width, label='GA')
    rects3 = ax[1].bar(x+width, best_propose1, width, label="GA-MCTS")
   
    ax[0].set_xticklabels(labels)
    ax[1].set_xticklabels(labels1)
    ax[1].set_xlabel('Test id')
    ax[1].set_ylabel('Mean objective values')
    ax[1].set_xticks(x)
    ax[0].set_xlabel('Test id')
    ax[0].set_ylabel('Mean objective values')
    # for axt in ax:
        # axt.set_xlabel('  ')
        # axt.set_xticks(x)
        # axt.set_xticklabels(labels)
        # axt.legend()

    # ax.bar_label(rects1, padding=10)
    # ax.bar_label(rects2, padding=3)
    # ax.bar_label(rects3, padding=3)
    ax[0].legend(labels=["MFEA", "GA", "GA-MCTS"], loc = "upper left")
    fig.tight_layout()
    # axt[0].set_title('Shortest path founded by algorithms')
    # ax.set_ylabel('Best found')
    # plt.xlabel("Test id")
    # plt.ylabel("Mean objective values")
    plt.show()

def show1(l, r):
    labels = list(final_df["test_id"][l:r])
    print(labels)
    best_MFEA = list(final_df["MFEA"][l:r])
    best_GA = list(final_df["cost"][l:r])
    best_propose = list(final_df["avg"][l:r])


    x = np.arange(len(labels))  # the label locations
    width = 0.2 # the width of the bars

    fig, ax = plt.subplots()

    rects21 = ax.bar(x , best_MFEA, width, label='MFEA')
    rects11 = ax.bar(x-width , best_GA, width, label='GA')
    rects31 = ax.bar(x+width, best_propose, width, label="GA-MCTS")
    ax.set_xticks(x)

    
   
    ax.set_xticklabels(labels)
    ax.set_xticks(x)
    ax.set_xlabel('Test id')
    ax.set_ylabel('Mean objective values')
    # for axt in ax:
        # axt.set_xlabel('  ')
        # axt.set_xticks(x)
        # axt.set_xticklabels(labels)
        # axt.legend()

    # ax.bar_label(rects1, padding=10)
    # ax.bar_label(rects2, padding=3)
    # ax.bar_label(rects3, padding=3)
    ax.legend(labels=["MFEA", "GA", "GA-MCTS"], loc = "upper right")
    fig.tight_layout()
    # axt[0].set_title('Shortest path founded by algorithms')
    # ax.set_ylabel('Best found')
    # plt.xlabel("Test id")
    # plt.ylabel("Mean objective values")
    plt.ylim(0,115)
    plt.show()
show1(24,42)
# show1(0,24)
# show(25,42)