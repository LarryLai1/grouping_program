import numpy as np
import copy
try:
    import args
except:
    print("missing args.py\nusing default args\n")

# set arguments
if 'args' in dir():
    args = args.args
    level_amount = args.level if bool(args.level) else 5
    time_amount = args.time if bool(args.time) else 4
    team_amount = args.team if bool(args.team) else 10
    seperation = args.seperation if bool(args.seperation) else 2
    show_level = args.show_level if bool(args.show_level) else True
    show_team = args.show_team if bool(args.show_team) else False
    show_meet = args.show_meet if bool(args.show_meet) else False
else:
    level_amount = 5
    time_amount = 4
    team_amount = 10
    seperation = 2
    show_level = True
    show_team = False
    show_meet = False

# some additional variables
app = 0
rmv = 0

# finding function
def dfs(ind: int, sep: int, temp: list, level_used: np.array, team_used: np.array)->bool:
    jump = 1
    threshold = 0 if sep==0 or ind<team_amount*time_amount/4 else 1

    # stop condition
    if ind == team_amount*time_amount/2:
        ans.append(temp)
        total_ans[sep] = copy.deepcopy(ans)
        return True
    
    time, index = int(ind/(team_amount/2)), ind%(team_amount/2)

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
    
    # matching
    for t1 in range(1, team_amount+1):
        if team_used[t1]:
            continue
        team_used[t1] = 1
        for t2 in range(t1+1, team_amount+1):
            if team_used[t2]:
                continue
            if meet_table[t1][t2]>threshold:
                continue
            team_used[t2] = 1
            meet_table[t1][t2] += (sep+1)
            meet_table[t2][t1] += (sep+1)

            level_choice = level_table[t1].intersection(level_table[t2])
            if len(level_choice) == 0:
                continue
            for level in level_choice:
                if level_used[level]:
                    continue
                level_table[t1].remove(level)
                level_table[t2].remove(level)
                level_used[level] += 1
                temp[level] = (t1, t2)
                if dfs(ind+jump, sep, temp, level_used, team_used):
                    return True
                level_used[level] = 0
                level_table[t1].add(level)
                level_table[t2].add(level)
                temp[level] = ()
            team_used[t2] = 0
            meet_table[t1][t2] -= (sep+1)
            meet_table[t2][t1] -= (sep+1)
        team_used[t1] = 0
    if index==0 and time!=0:
        if last_temp in ans:
            global rmv
            ans.remove(last_temp)
            rmv+=1
    return False

print(f"Seperation:  {seperation:2d}\nTeam Amount:  {team_amount:2d}\nLevel per Sep:  {level_amount:2d}\nTime per Sep:  {time_amount:2d}")

# store answer
meet_table = np.zeros((team_amount+1, team_amount+1), dtype=int)
total_ans = [[[(None, None) for x in range(level_amount)] for a in range(time_amount)] for _ in range(seperation)]
# run dfs for each seperation
for sep in range(seperation):
    level_table = [set([i for i in range(0, level_amount)]) for _ in range(team_amount+1)]
    ans = []
    dfs(0, sep, [], np.zeros(level_amount, dtype=int), np.zeros(team_amount+1, dtype=int))

# show results
if show_level:
    print("--"*20)
    print("Time Table for Levels: ")
    for d in total_ans:
        for e in d:
            print(e)

if show_team:
    print("--"*20)
    print("Time Table for Teams: ")
    for tm in range(1, team_amount+1):
        print(f"Team {tm:2}: ", end=" ")
        for sep in range(seperation):
            for time in range(0, time_amount):
                for level in range(0, level_amount):
                    if tm in total_ans[sep][time][level]:
                        print(level+level_amount*sep+1, end="->")
                        break
        print("ED")

if show_meet:
    print("--"*20)
    print("Meet Table: ")
    print(meet_table[1:,1:])