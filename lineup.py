import re, time

############ Functions ############

# Set player list from text file
def get_players():
    file_name = input("Your .txt file name: ")
    if ".txt" in file_name:
        pass
    else:
        file_name+=".txt"

    params = []
    min_avg_min = int(input("Minimum average minutes to include: "))
    min_games = int(input("Minimum number of games to include: "))
    params.append(min_avg_min)
    params.append(min_games)

    file = open(file_name,"r")

    player_lists = file.readlines()
    players = []

    for unit in player_lists:
        temp = re.split(r'\t+', unit)
        temp[len(temp)-1] = temp[len(temp)-1][:-1]

        for position in range(2,6):
            if position is 2:
                temp[position] = int(temp[position])/100
            if position is 5:
                temp[position] = int(temp[position])
            else:
                temp[position] = float(temp[position])

        players.append(temp)

    to_remove_spots = []
    for spot in range(len(players)):
        if players[spot][4] < params[0] or players[spot][5] < params[1]:
            to_remove_spots.append(spot)

    to_remove_spots.reverse()
    for spot in to_remove_spots:
        del players[spot]

    return players

def optimize(players,included,positions):

    max_price = 500

    for player in included:
        max_price-=player[2]

    players.sort(reverse = True, key = lambda players: players[1]/players[2])

    knapsack(max_price,players,positions,included)

def knapsack(max_price, players, positions, included):

    players_needed = 8-len(included)
    table = [[[0 for w in range(max_price + 1)] for j in range(len(players) + 1)] for k in range(players_needed + 1)]

    for k in range(1, players_needed + 1):
        for j in range(1, len(players) + 1):
            name, val, wt = players[j-1]
            for w in range(1, max_price + 1):
                if wt > w:
                    table[k][j][w] = table[k][j-1][w]
                else:
                    table[k][j][w] = max(table[k][j-1][w],table[k-1][j-1][w-wt] + val)

    result = []
    w = max_price
    k = players_needed
    starting_player = len(players)+1
    correct = False
    round = 0

    while not correct:

        result = []
        w = max_price

        if starting_player < players_needed and w != 0:
            round+=1
            starting_player=len(players)+1
            w-=round

        starting_player-=1
        for j in range(starting_player, 0, -1):
            print("Max Price: ",max_price," K: ",k," J: ",j," w: ",w)
            try:
                was_added = table[k][j][w] != table[k][j-1][w]
            except:
                print("BROKE--")

            if was_added:
                name, val, wt = players[j-1]
                result.append(players[j-1])
                w -= wt

        for player in included:
            result.append(player)

        correct = verify(result,positions)
        if round == len(players)+1:
            break

    forwards = []
    midfielders = []
    defenders = []
    keepers = []
    total_val = 0
    total_price = 0

    for player in result:
        player[1] = player[1]/100
        total_val+=player[1]
        player[2] = player[2]*100
        total_price+=player[2]
        if player[0] in positions[0]:
            forwards.append(player)
        if player[0] in positions[1]:
            midfielders.append(player)
        if player[0] in positions[2]:
            defenders.append(player)
        if player[0] in positions[3]:
            keepers.append(player)

    if len(result) > 0:
        print("Forwards: ",forwards)
        print("Midfielders: ",midfielders)
        print("Defenders: ",defenders)
        print("Keeper: ",keepers)
        print("Final value: ",total_val)
        print("Final price: ",total_price)
        print()
    else:
        print("Couldn't find a lineup...")

def verify(players,positions):

    if len(players) != 8:
        return False

    for_count = 0
    mid_count = 0
    def_count = 0

    for player in players:
        if player[0] in positions[0]:
            for_count+=1
        if player[0] in positions[1]:
            mid_count+=1
        if player[0] in positions[2]:
            def_count+=1

    if for_count >= 2 and mid_count >= 2 and def_count >= 2:
        print("Verified! ",players)
        return True

    return False

##################################

players = get_players()

player_names = []
for player in players:
    player_names.append(player[0])
print()
print("Possible players: ",player_names)
print()

included_names = []
include = input("Any players you want to include? Player or [N]: ")
while include != "N":
    if include in player_names:
        included_names.append(include)
        include = input("Any other players you want to include? Player or [N]: ")
    else:
        include = input("Player not found. Try again. Player or [N]: ")

excluded_names = []
exclude = input("Any players you want to exclude? Player or [N]: ")
while exclude != "N":
    if exclude in player_names and exclude not in included_names:
        excluded_names.append(exclude)
        exclude = input("Any other players you want to exclude? Player or [N]: ")
    else:
        if player in included_names:
            exclude = input("Player is already included. Try again. Player or [N]: ")
        else:
            exclude = input("Player not found. Try again. Player or [N]: ")
print()

forwards = []
mids = []
defenders = []
keepers = []

for player in players:
    if player[1] == "F" or player[1] == "M/F":
        forwards.append(player[0])
    if player[1] == "M" or player[1] == "M/F":
        mids.append(player[0])
    if player[1] == "D":
        defenders.append(player[0])
    if player[1] == "GK":
        keepers.append(player[0])
    player[1]=player[3]*100
    player[2]=int(player[2])
    del player[-3:]

included = []
for player in players:
    if player[0] in included_names:
        included.append([player[0],player[1],int(player[2])])
        del players[players.index(player)]
    elif player[0] in excluded_names:
        del players[players.index(player)]

# Removes keepers
for i in range(len(players)-1,-1,-1):
    if players[i][0] in keepers:
        del players[i]

positions = [forwards,mids,defenders,keepers]

optimize(players,included,positions)
