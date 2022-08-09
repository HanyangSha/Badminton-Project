import pandas as pd
import numpy as np
import math
import scipy.stats as ss

df = pd.read_csv("ms.csv")
rank = pd.read_csv("historical_bwf_ranking.csv")

df = df[["tournament", "date", 'game_1_score', 'game_2_score', 'game_3_score', 'team_one_players', 'team_two_players']]
r = df.shape[0]

df["sorted1"] = ""
df["sorted2"] = ""

for i in range(0, r):
    df.at[i, "sorted1"] = df.loc[i].at["team_one_players"].lower().split()
    df.at[i, "sorted1"].sort()

    df.at[i, "sorted2"] = df.loc[i].at["team_two_players"].lower().split()
    df.at[i, "sorted2"].sort()

    t = df.at[i, "date"].split("-")
    df.at[i, "date"] = "{}-{}-{}".format(t[2], t[0], t[1])

rr = rank.shape[0]
m = {} # maps name to row idx

rank["sorted"] = ""
for i in range(0, rr):
    rank.at[i, "First name"] = str(rank.at[i, "First name"])
    rank.at[i, "Last name"] = str(rank.at[i, "Last name"])
    n = []
    n = n + rank.at[i, "Last name"].split()
    n = n + rank.at[i, "First name"].split()
    n.sort()
    rank.at[i, "sorted"] = n

    m[tuple(n)] = i

diffrank_lists = [[],[]]
bound00 = 1
bound01 = 10
bound10 = 20
bound11 = 30 

weeks = list(rank.columns)

for i in range(0, r): 
    week = df.at[i, "date"]
    p1 = df.at[i, "sorted1"]
    p2 = df.at[i, "sorted2"]

    if (type(df.at[i, "game_1_score"]) != str or type(df.at[i, "game_2_score"]) != str):
        continue

    t = df.at[i, "game_1_score"].split("-")
    t = [int(t[0]), int(t[1])]

    g1 = (t[0] - (t[0] + t[1])/2) * (t[0] - (t[0] + t[1])/2)
    #g1 = abs(t[0] - (t[0] + t[1])/2)

    t = df.at[i, "game_2_score"].split("-")
    t = [int(t[0]), int(t[1])]

    g2 = (t[0] - (t[0] + t[1])/2) * (t[0] - (t[0] + t[1])/2)
    #g2 = abs(t[0] - (t[0] + t[1])/2)

    idx = 3 # first 3 columns are not ranks
    while (idx < len(weeks)):
        if (weeks[idx] > week):
            break
        idx += 1
    idx -= 1

    '''
    for j in range(0, rr): 
        if (rank.at[j, "sorted"] == p1): 
            #p1_rank = rank.loc[rank["sorted"] == p1]
            week_rank1 = rank.iloc[j, idx]
        if (rank.at[j, "sorted"] == p2):
            #p2_rank = rank.loc[rank["sorted"] == p2]
            week_rank2 = rank.iloc[j, idx]
    '''

    if (m.get(tuple(p1)) == None or m.get(tuple(p2)) == None):
        continue

    rank1 = rank.iloc[m[tuple(p1)], idx]
    rank2 = rank.iloc[m[tuple(p2)], idx]

    diff = abs(rank1 - rank2)
    if (diff >= bound00 and diff <= bound01): 
        diffrank_lists[0].append(g1)
        diffrank_lists[0].append(g2)
    if (diff >= bound10 and diff <= bound11): 
        diffrank_lists[1].append(g1)
        diffrank_lists[1].append(g2)

sets = []

for i in range(0, len(diffrank_lists)):

    a = np.asarray(diffrank_lists[i])
    q3, q1 = np.percentile(a, [75, 25])
    iqr = q3 - q1
    low_fence = q1 - 1.5* iqr
    high_fence = q3 + 1.5 * iqr

    idx = np.where((a >= low_fence) & (a <= high_fence))
    a = a[idx]

    mu = np.mean(a)
    s = np.std(a)
    n = len(a)
    
    sets.append((mu, s, n))

    print((mu, s, n))

for i in range(0, len(sets)):
    for j in range(i+1, len(sets)):
        a = sets[i]
        b = sets[j]

        test_statistic = (a[0] - b[0])/math.sqrt(a[1]*a[1]/a[2] + b[1]*b[1]/b[2])

        dof = min(a[2], b[2])
        if (test_statistic < 0):
            p = ss.t.cdf(x= test_statistic, df = dof) *2
        else: 
            p = (1- ss.t.cdf(x= test_statistic, df = dof)) *2
        
        print(p)
        if (p < 0.05):
            print("There is enough evidence at alpha = 0.05 that there is a score difference gap between players of rankings differences in [{}, {}] and in [{}, {}]".format(bound00, bound01, bound10, bound11))
        else: 
            print("There is NOT enough evidence at alpha = 0.05 that there is a score difference gap between players of rankings differences in [{}, {}] and in [{}, {}]".format(bound00, bound01, bound10, bound11))
