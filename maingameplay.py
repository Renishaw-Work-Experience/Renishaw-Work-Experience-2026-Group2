import random

#Idk if we should have logins and passwords or not
#these 2 functions work together to get a set of names to play the game
def player_count_input():
    while True:
        try:           
            player_amount = int(input('How many players (must be 2 or more): ')) 
            if player_amount < 2:
                print('Must be 2 or more')
        except ValueError:
            print('Input a valid integer')
    return player_amount()

def set_players():
    high_scores = read_scores()
    saved_players = list(high_scores.keys())
    players = []
    player_amount = player_count_input()
    for player in saved_players: print(saved_player)
    print(f"""Please input the name of one of the players listed to play
as that account or use a name not shown to create a new account.
Also keep in mind that player 1 will be the dealer.""")
    i = 0                 
    while i < (player_amount):
        next_player = input('Input the name of the next player').strip()
        if next_player in players:
            print('Please do not use the name of a player that you have just used')
        else:
            players.append(next_player)
            if i == 0:
                dealer = next_player
                print(f"{player} will be the dealer")
            i += 1
    session_scores = dict.fromkeys(players, 10)
    print('every player has been granted 10 tokens to start')
    return session_scores


# Reads from file and creates 2 dictionaries for highscores and a changing one for current score
def read_scores():
    with open('saved_scores.txt', 'r') as f:
        high_scores = {}
        for line in f:
            player, score = line.strip().split(':')
            high_scores[player] = int(score)
    return high_scores
        
        

#Idk if we should have something for every player to indivually bet or just iterate through
# every player but I did the individual one
def wager(player, session_scores, bet_amounts):
    while True:
        try:           
            bet_amounts[player] = int(input('How much would you like to wager: ')) 
            if bet_amounts[player] > session_scores[player]:
                print(f"You have {session_scores[player]} tokens, you cannot bet {bet_amounts[player]}")
            elif bet_amounts[player] < 0:
                print('Cannot bet a negative number')
            else:
                session_scores[player] -= bet_amounts[player]
                return bet_amounts
        except ValueError:
            print('Input a valid integer')


# adds bet_amount*2 to the player's score
def win(player):
    session_scores[player] += bet_amounts[player]*2

def lose(player):
    session_scores[player] -= bet_amounts[player]

    
# sets session score to be saved as a current score - could code an input for the cashout
def cashout(player):
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
    with open('saved_scores.txt', 'w') as f:
        for player, score in sorted_scores.items():
            f.write(f"{player}:{score}\n")

def sort_dict_by_value(dict1):
    list1 =[]
    for key, val in dict1.items():
        list1.append((val,key))
    list1.sort()
    dict2 = {}
    for val, key in list1:
        dict2[key] = val
    return dict2

deck = [
    "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "sj", "sq", "sk", "sa",
    "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9", "h10", "hj", "hq", "hk", "ha",
    "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "cj", "cq", "ck", "ca",
    "d2", "d3", "d4", "d5", "d6", "d7", "d8", "d9", "d10", "dj", "dq", "dk", "da"
]
dealerHand = []
playerHand = []
dealertokens = 10
playertokens = 10

random.shuffle(deck)

def drawcard(player):
    if player == "Dealer":
        card = deck.pop()
        return card
    elif player == "Player":
        card = deck.pop()
        print(f"Player drew: {card}")
        return card

def calculateHandValue(hand):
    value = 0
    aces = 0
    for card in hand:
        if card[1] in ['j', 'q', 'k']:
            value += 10
        elif card[1] == 'a':
            aces += 1
            value += 11
        else:
            value += int(card[1:])
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

def displayHands():
    print(f"Dealer's hand: {dealerHand[1]}")
    print(f"Player's hand: {playerHand}")
    print(f"Player's score: {calculateHandValue(playerHand)}")

def determineWinner():
    playerScore = calculateHandValue(playerHand)
    dealerScore = calculateHandValue(dealerHand)

    if playerScore > dealerScore:
        print("Player wins!")
    elif dealerScore > playerScore:
        print("Dealer wins!")
    else:
        print("It's a tie!")

while True:
    try:
        dealerWager = int(input("Dealer, how many tokens would you like to wager? "))
        if dealerWager > dealertokens or dealerWager <= 0:
            print("Invalid wager. Please enter a valid number of tokens.")
        else:
            dealertokens -= int(dealerWager)
            break
        
    except:
        print("Invalid input. Please enter a valid number of tokens.")
while True:
    try:
        playerWager = int(input("Player, how many tokens would you like to wager? "))
        if playerWager > playertokens or playerWager <= 0:
            print("Invalid wager. Please enter a valid number of tokens.")
            continue
        playertokens -= int(playerWager)
        break
    except ValueError:
        print("Invalid input. Please enter a valid number of tokens.")


for x in range(2):    
    playerHand.append(drawcard("Player"))
    dealerHand.append(drawcard("Dealer"))



#main game loop
displayHands()

while True:
    playerChoice = input("Would you like to hit or stand? (h/s): ").lower()
    if playerChoice == "h":
        playerHand.append(drawcard("Player"))
        displayHands()
        score = calculateHandValue(playerHand)
        if score > 21:
            print("Player busts! Dealer wins.")
            break
        
    elif playerChoice == "s":
        print("Player chose to stand.")
        while True:
            dealerChoice = input("Dealer, would you like to hit or stand? (h/s): ").lower()
            if dealerChoice == "h":
                dealerHand.append(drawcard("Dealer"))
                calculateHandValue(dealerHand)
                displayHands()
                score = calculateHandValue(dealerHand)
            if score > 21:
                print("Dealer busts! Player wins.")
                break
            elif dealerChoice == "s":
                print("Dealer chose to stand.")
                determineWinner()
                break











