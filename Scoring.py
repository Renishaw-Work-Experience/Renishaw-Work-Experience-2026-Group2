# Idk if we should have logins and passwords or not
# these 2 functions work together to get a set of names to play the game
#def player_count_input():
    #while True:
        #try:
            #player_amount = int(input("How many players (must be 2 or more): "))
           # if player_amount < 2:
               # print("Must be 2 or more")
            #else:
                #return player_amount
       # except ValueError:
           # print("Input a valid integer")


def set_players():
    high_scores = read_scores()
    saved_players = list(high_scores.keys())
    players = []
    player_amount = 2  # Default player amount
    print("Players who have played before: ")
    for saved_player in saved_players:
        print(saved_player)
    print(f"""Please input the name of one of the players listed to play
as that account or use a name not shown to create a new account.
Also keep in mind that player 1 will be the dealer.""")
    i = 0
    while i < (player_amount):
        next_player = input("Input the name of the next player: ").strip()
        if next_player in players:
            print("Please do not use the name of a player that you have just used")
        else:
            players.append(next_player)
            if i == 0:
                dealer = next_player
                print(f"{dealer} will be the dealer")
            i += 1
    session_scores = dict.fromkeys(players, 10)
    print("every player has been granted 10 tokens to start")
    return session_scores


# Reads from file and creates 2 dictionaries for highscores and a changing one for current score
def read_scores():
    with open("saved_scores.txt", "r") as f:
        high_scores = {}
        for line in f:
            player, score = line.strip().split(":")
            high_scores[player] = int(score)
    return high_scores


# Idk if we should have something for every player to indivually bet or just iterate through
# every player but I did the individual one
def wager(player, session_scores, bet_amounts):
    while True:
        try:
            bet_amounts[player] = int(input(f"How much would {player} like to wager: "))
            if bet_amounts[player] > session_scores[player]:
                print(f"{player} has {session_scores[player]} tokens, they cannot bet {bet_amounts[player]}")
            elif bet_amounts[player] < 0:
                print(f"{player} cannot bet a negative number")
            else:
                session_scores[player] -= bet_amounts[player]
                return bet_amounts
        except ValueError:
            print(f"{player}, please input a valid integer")


# adds bet_amount*2 to the player's score
def win(player, session_scores, bet_amounts):
    session_scores[player] += bet_amounts[player] * 2


def lose(player, session_scores, bet_amounts):
    session_scores[player] -= bet_amounts[player]


# sets session score to be saved as a current score - could code an input for the cashout
def cashout(player, session_scores):
    high_scores = read_scores()
    try:
        if high_scores[player] < session_scores[player]:
            high_scores[player] = session_scores[player]
    except KeyError:
        high_scores[player] = session_scores[player]
    write_scores(high_scores)
    session_scores[player] = 10


# writes the saved highscores into the scores file in order
def write_scores(high_scores):
    sorted_scores = sort_dict_by_value(high_scores).items()
    with open("saved_scores.txt", "w") as f:
        for player, score in sorted_scores:
            f.write(f"{player}:{score}\n")


def sort_dict_by_value(dict1):
    list1 = []
    for key, val in dict1.items():
        list1.append((val, key))
    list1.sort()
    dict2 = {}
    for val, key in list1:
        dict2[key] = val
    return dict2
