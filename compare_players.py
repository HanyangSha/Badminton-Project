import pandas as pd

df = pd.read_csv("ms.csv")

df = df[["tournament", "round", "winner", "nb_sets", 'game_1_score', 'game_2_score', 'game_3_score', 'team_one_players', 'team_two_players']]
r = df.shape[0]
c = df.shape[1]

'''
def process(v):
    v["team_one_players"] = v["team_one_players"].split().sort()
    return v

df = df.apply(process, axis = 1)
'''

df["sorted1"] = ""
df["sorted2"] = ""

for i in range(0, r):
    df.at[i, "sorted1"] = df.loc[i].at["team_one_players"].split()
    df.at[i, "sorted1"].sort()

    df.at[i, "sorted2"] = df.loc[i].at["team_two_players"].split()
    df.at[i, "sorted2"].sort()

    # flip the data to be in "x bt y" format
    if (df.at[i, "winner"] == 2):
        #df.at[i, "winner"] =1

        t = df.at[i, "team_one_players"]
        df.at[i, "team_one_players"] = df.at[i, "team_two_players"]
        df.at[i, "team_two_players"] = t

        t = df.at[i, "sorted1"]
        df.at[i, "sorted1"] = df.at[i, "sorted2"]
        df.at[i, "sorted2"] = t
        
        t = df.at[i, "game_1_score"].split("-")
        df.at[i, "game_1_score"] = "{}-{}".format(t[1], t[0])

        t = df.at[i, "game_2_score"].split("-")
        df.at[i, "game_2_score"] = "{}-{}".format(t[1], t[0])

        if (df.at[i, "nb_sets"] == 3):
            t = df.at[i, "game_3_score"].split("-")
            df.at[i, "game_3_score"] = "{}-{}".format(t[1], t[0])

class Player:
    def __init__(self, name):
        self.name = name
        name = name.split()
        name.sort()
        self.sorted = name
        self.win = []
        self.runnerup = []

    def out(self):
        print(self.name, ": ")

        print("wins: {}".format(len(self.win)))
        if (len(self.win) == 0):
            print("none")
        else: 
            for i in self.win: 
                print(df.at[i, "tournament"])

        print("runner ups: {}".format(len(self.runnerup)))
        if (len(self.runnerup) == 0):
            print("none")
        else: 
            for i in self.runnerup: 
                print(df.at[i, "tournament"])

        print()

class comparision: 
    def __init__(self, a, b):
        self.players = [Player(a), Player(b)]
        self.h2h = [0,0]
    
    def out(self):
        for p in self.players: 
            p.out()
        print("Head to head: {} {}-{} {}".format(self.players[0].name, self.h2h[0], self.h2h[1], self.players[1].name))
    
    def check(self, x, y): 
        return (x == self.players[0].sorted and y == self.players[1].sorted) or (x == self.players[1].sorted and y == self.players[0].sorted)


cmp = comparision("Kento Momota", "Viktor Axelsen")

'''
player = "Kento Momota"
name1 = player.split()
name1.sort()

player2 = "Lee Chong Wei"
name2 = player2.split()
name2.sort()

players = [Player("Kento Momota"), Player("Lee Chong Wei")]

win1 = []
runnerup1 = []
win2 = []
runnerup2 = []
'''

'''
df1 = df.loc[df['team_one_players'] == "Chong Wei Lee"]
print(df1)

df2 = df.loc[df['team_two_players'] == "Chong Wei Lee"]
print(df2)
'''

ndf = pd.DataFrame(columns = ["tournament", "round", 'team_one_players', 'team_two_players', 'game_1_score', 'game_2_score', 'game_3_score'])

for i in range(0,r):

    if (cmp.check(df.at[i, "sorted1"], df.at[i, "sorted2"])):

        '''
        print(df.at[i, "sorted1"])
        print(cmp.players[0].sorted)
        print(df.at[i, "sorted2"])
        print(cmp.players[1].sorted)
        '''

        tmp = df.loc[[i], ["tournament", "round", 'team_one_players', 'team_two_players', 'game_1_score', 'game_2_score', 'game_3_score']]
        ndf = pd.concat([ndf, tmp], ignore_index = True)
        ndf.reset_index()

        if (df.at[i, "sorted1"] == cmp.players[0].sorted):
            cmp.h2h[0] += 1
        else: 
            cmp.h2h[1] += 1

    for p in cmp.players: 
        if (df.at[i, "sorted1"] == p.sorted and df.at[i, "round"] == "Final"):
            p.win.append(i)
        
        if (df.at[i, "sorted2"] == p.sorted and df.at[i, "round"] == "Final"):
            p.runnerup.append(i)

    '''
    if (df.at[i, "sorted1"] == name2 and df.at[i, "round"] == "Final"):
        win2.append(i)
    
    if (df.at[i, "sorted2"] == name2 and df.at[i, "round"] == "Final"):
        runnerup2.append(i)
    '''

'''
print(player, ": ")
print("wins: ")
if (len(win1) == 0):
    print("none")
else: 
    for i in win1: 
        print(df.at[i, "tournament"])
print("runner ups: ")
if (len(runnerup1) == 0):
    print("none")
else: 
    for i in runnerup1: 
        print(df.at[i, "tournament"])

print()

print(player2, ": ")
print("wins: ")
if (len(win2) == 0):
    print("none")
else: 
    for i in win2: 
        print(df.at[i, "tournament"])
print("runner ups: ")
if (len(runnerup2) == 0):
    print("none")
else: 
    for i in runnerup2: 
        print(df.at[i, "tournament"])
'''

cmp.out()
print(ndf)