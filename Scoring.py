import random


def player_count_input():
    while True:
        try:
            player_amount = int(input("How many players (must be 2 or more): "))
            if player_amount < 2:
                print("Must be 2 or more")
            else:
                return player_amount
        except ValueError:
            print("Input a valid integer")


def set_players():
    high_scores = read_scores()
    saved_players = list(high_scores.keys())
    players = []
    player_amount = player_count_input() 
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
        elif ':' in next_player:
            print('No colons in names')
        else:
            players.append(next_player)
            if i == 0:
                dealer = next_player
                print(f"{dealer} will be the dealer")
            i += 1
    session_scores = dict.fromkeys(players, 10)
    print("every player has been granted 10 tokens to start")
    return session_scores



def read_scores():
    with open("saved_scores.txt", "r") as f:
        high_scores = {}
        for line in f:
            player, score = line.strip().split(":")
            high_scores[player] = int(score)
    return high_scores


def wager(session_scores):
    names = list(session_scores.keys())
    playernames = names.copy()
    playernames.remove(names[0]) 
    bet_amounts = {}
    for name in playernames:
        bet_amounts[name] = 0  
    for player in playernames:
        while True:
            try:
                bet_amounts[player] = int(input(f"How much would {player} like to wager: "))
                if bet_amounts[player] > session_scores[player]:
                    print(f"{player} has {session_scores[player]} tokens, they cannot bet {bet_amounts[player]}")
                elif bet_amounts[player] < 0:
                    print(f"{player} cannot bet a negative number")
                elif bet_amounts[player] == 0:
                    print('You have to gamble!')
                    if session_scores[player] == 0:
                        print(f"But {player} has no tokens left and will be removed from the game")
                        names.remove(player)
                        if len(playernames) == 0:
                            cashout(names[0], session_scores)
                            exit('Everyone ran out of tokens')
                else:
                    session_scores[player] -= bet_amounts[player]
                    session_scores[names[0]] += bet_amounts[player]
                    break
            except ValueError:
                print(f"please input a valid integer")
        hands = {}
        for name in names:
            hands[name] = []
    return bet_amounts, hands



def win(player, session_scores, bet_amounts):
    names = list(session_scores.keys())
    session_scores[player] += bet_amounts[player] * 2
    session_scores[names[0]] -= bet_amounts[player] * 2


def push(player, session_scores, bet_amounts):
    names = list(session_scores.keys())
    session_scores[player] += bet_amounts[player]
    session_scores[names[0]] -= bet_amounts[player]




def cashout(player, session_scores):
    high_scores = read_scores()
    try:
        if high_scores[player] < session_scores[player]:
            high_scores[player] = session_scores[player]
    except KeyError:
        high_scores[player] = session_scores[player]
    write_scores(high_scores)
    session_scores[player] = 10



def write_scores(high_scores):
    sorted_scores = sort_dict_by_value(high_scores).items()
    with open("saved_scores.txt", "w") as f:
        for player, score in sorted_scores:
            f.write(f"{player}:{score}\n")


def sort_dict_by_value(dict1):
    dict1 = {k: v for k, v in sorted(dict1.items(), key=lambda item: item[1], reverse=True)}
    return dict1
