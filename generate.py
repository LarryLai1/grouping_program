import numpy as np
import copy

app = 0
rmv = 0

def dfs(ind: int, sep: int, temp: list, single_team: set, single_team_unused: list, level_used: np.array, team_used: np.array)->bool:
    jump = 1
    if ind == team_amount*time_amount/2:
        ans.append(temp)
        total_ans[sep] = copy.deepcopy(ans)
        print("add")
        return True
    # print(f'ind: {ind}')
    time, index = int(ind/(team_amount/2)), ind%(team_amount/2)
    tt = total_ans[sep][time]
    # print(f"temp: {temp}")

    # change level
    if index == 0:
        if time!=0:
            global app
            app += 1
            ans.append(temp)
            last_temp = copy.deepcopy(temp)
        temp = [() for _ in range(level_amount)]
        level_used = np.zeros(level_amount, dtype=int)
        team_used = np.zeros(team_amount+1, dtype=int)
        single_team = set()
        single_team_unused = []
        for i in range(0, level_amount):
            if tt[i][0]:
                team_used[tt[i][0]] = 1
                if tt[i][1]:
                    level_used[i] = 1
                    team_used[tt[i][1]] = 1
                    temp[i] = tt[i]
                    jump += 1
                else:
                    single_team_unused.append(i)
                    single_team.add(i)
    # print(f"single_team: {single_team}")
    if jump>1:
        print(f"jump a lot at {time}")
    # single team
    for id, tm in enumerate(single_team_unused):
        t1 = tt[tm][0]
        for t2 in range(3, team_amount+1):
            if team_used[t2] or tm not in level_table[t2]:
                continue
            team_used[t2] = 1
            level_used[tm] = 1
            level_table[t2].remove(tm)
            temp[tm] = (t1, t2)
            single_team_unused.pop(id)
            if dfs(ind+jump, sep, temp, single_team, single_team_unused, level_used, team_used):
                return True
            team_used[t2] = 0
            level_used[tm] = 0
            level_table[t2].add(tm)
            temp[tm] = ()
            single_team_unused.insert(id, tm)
    
    # dual team
    for t1 in range(3, team_amount+1):
        if team_used[t1]:
            continue
        team_used[t1] = 1
        for t2 in range(t1+1, team_amount+1):
            if team_used[t2]:
                continue
            if meet_table[t2][t2]:
                continue
            team_used[t2] = 1
            meet_table[t1][t2] = 1
            meet_table[t2][t1] = 1

            level_choice = level_table[t1].intersection(level_table[t2]) - single_team
            if len(level_choice) == 0:
                continue
            # print(level_choice)
            for level in level_choice:
                if level_used[level]:
                    continue
                level_table[t1].remove(level)
                level_table[t2].remove(level)
                level_used[level] = 1
                temp[level] = (t1, t2)
                if dfs(ind+jump, sep, temp, single_team, single_team_unused, level_used, team_used):
                    return True
                level_used[level] = 0
                level_table[t1].add(level)
                level_table[t2].add(level)
                temp[level] = ()
                
            team_used[t2] = 0
            meet_table[t1][t2] = 0
            meet_table[t2][t1] = 0
        team_used[t1] = 0
    if index==0 and time!=0:
        global rmv
        ans.remove(last_temp)
        rmv+=1
    # print("rollback")
    return False

level_amount = 5
time_amount = 4
team_amount = 10
seperation = 1
meet_table = np.zeros((team_amount+1, team_amount+1), dtype=int)

total_ans = [[[(None, None) for x in range(level_amount)] for a in range(time_amount)] for _ in range(seperation)]

if seperation*time_amount > team_amount-1:
    raise ValueError("Impossible Input Data")

# pre-set 1
for i in range(seperation):
    for j in range(time_amount):
        total_ans[i][j][j] = (1, None)

# pre-set 2
total_ans[0][0][0] = (1, 2)
for i in range(seperation):
    for j in range(time_amount):
        if (i==j and j==0): continue
        else:
            if i==0:
                index = j-1+2*(j%2)
            else:
                index = (j+1)%level_amount
            total_ans[i][j][index] = (2, None)

# fix more
meet_table[1][2] = 1
meet_table[2][1] = 1

for sep in range(seperation):
    level_table = [set([i for i in range(0, level_amount)]) for _ in range(team_amount+1)]
    ans = []
    print("---"*10)
    print('meet_table')
    print(meet_table)
    dfs(0, sep, [], [], [], np.zeros(level_amount, dtype=int), np.zeros(team_amount+1, dtype=int))
    print('total_ans')
    for e in total_ans[sep]:
        print(e)
    print(app, rmv)