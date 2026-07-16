import random
import Scoring


def drawcard(player):
    card = deck.pop()
    if player == names[0]:
        if len(hands[player]) == 1:
            print(f"The dealer ({player}) drew in secret")
        else:
            print(f"The dealer ({player}) drew {card}")
    else:
        print(f"{player} drew: {card}") #networking needed 
    hands[player].append(card)


def calculateHandValue(hand):
    value = 0
    aces = 0
    for card in hand:
        if card[1] in ["j", "q", "k"]:
            value += 10
        elif card[1] == "a":
            aces += 1
            value += 11
        else:
            value += int(card[1:])
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value


def displayHands(end=False):
    for i in range(len(names)): 
        if end:
                print(f"Dealer's ({names[0]}'s) hand: {hands[names[0]]}")
                print(f"Dealer's score: {calculateHandValue(hands[names[0]])}")
                print(f"{names[i]}'s hand: {hands[names[i]]}")
                print(f"{names[i]}'s score: {calculateHandValue(hands[names[i]])}")
                if names[i] in nonbust:
                    determineWinner(names[i])
        else:
            print(f"Dealer's faceup card: {hands[names[0]][0]}")
            print(f"{names[i]}'s hand: {hands[names[i]]}")
            print(f"{names[i]}'s score: {calculateHandValue(hands[names[i]])}")

def displayHand(player):
    if player == names[0]:
        print(f"Dealer's ({names[0]}'s) hand: {hands[names[0]]}")
        print(f"Dealer's ({names[0]}'s) score: {calculateHandValue(hands[names[0]])}")
    else:
        print(f"Dealer's faceup card: {hands[names[0]][0]}")
        print(f"{player}'s hand: {hands[player]}")
        print(f"{player}'s score: {calculateHandValue(hands[player])}")



def determineWinner(player):
    playerScore = calculateHandValue(hands[player])
    dealerScore = calculateHandValue(hands[names[0]])
    if playerScore > dealerScore:
        print(f"{player} wins")
        Scoring.win(player, sessionscores, betamounts)              
    elif playerScore == dealerScore:
        print("It's a push")    
        Scoring.push(player, sessionscores, betamounts)
    else:
        print(f"{player} loses")
    cashout(player, sessionscores)


        

def cashout(player, sessionscores):
    print(f"{player} now has {sessionscores[player]} tokens.")
    choice = input(f"{player}, would you like to cash out? (y/n): ").lower()
    if choice == "y" and sessionscores[player] > 10:
        Scoring.cashout(player, sessionscores)
        print(f"{player} has cashed out. Their score has been saved.")
        return True    
    elif choice == "n":
        print(f"{player} has chosen not to cash out.")
        return False
    else:
        print(f"{player} cannot cash out with less than 10 tokens.")
        return False

def init_game():
    print('A new game will now begin\n')
    global deck, nonbust, betamounts, hands
    deck = [
    "s2",
    "s3",
    "s4",
    "s5",
    "s6",
    "s7",
    "s8",
    "s9",
    "s10",
    "sj",
    "sq",
    "sk",
    "sa",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "h7",
    "h8",
    "h9",
    "h10",
    "hj",
    "hq",
    "hk",
    "ha",
    "c2",
    "c3",
    "c4",
    "c5",
    "c6",
    "c7",
    "c8",
    "c9",
    "c10",
    "cj",
    "cq",
    "ck",
    "ca",
    "d2",]
    random.shuffle(deck)   
    nonbust = []
    betamounts, hands = Scoring.wager(sessionscores)
    for name in names: 
    for name in names: 
        drawcard(name)
        drawcard(name)

# main game loop
sessionscores = Scoring.set_players()
names = list(sessionscores.keys())
while True:
    init_game()
    displayHands()
    for i in reversed(range(len(names))):
    for i in reversed(range(len(names))):
        displayHand(names[i])
        if i != 0:
            while True:
                playerChoice = input(f"Would {names[i]} like to hit or stand? (h/s): ").lower() 
                playerChoice = input(f"Would {names[i]} like to hit or stand? (h/s): ").lower() 
                if playerChoice == "h":
                    drawcard(names[i])
                    displayHand(names[i])
                    score = calculateHandValue(hands[names[i]])
                    if score > 21:
                        print("Bust!")
                        cashout(names[i], sessionscores)
                        break
                elif playerChoice == "s":
                    print(f"{names[i]} chose to stand.")
                    nonbust.append(names[i])
                    break
        else:
            while True:
                dealerChoice = input(f"Dealer ({names[0]}), would you like to hit or stand? (h/s): ").lower() 
                dealerChoice = input(f"Dealer ({names[0]}), would you like to hit or stand? (h/s): ").lower() 
                if dealerChoice == "h":
                    drawcard(names[0])
                    calculateHandValue(hands[names[0]])
                    displayHand(names[0])
                    score = calculateHandValue(hands[names[0]])
                    if score > 21:
                        print("Dealer busts! All non-bust players win.")
                        for name in nonbust:
                            Scoring.win(name, sessionscores, betamounts)
                            cashout(name, sessionscores) 
                            cashout(name, sessionscores) 
                        break
                elif dealerChoice == "s":
                    print("Dealer chose to stand.")
                    displayHands(True)
                    break
