import random
import Scoring

# graphics
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

# Possible graphics for playerscores
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

# graphics needed
def displayHands(end=False):
    for i in range(len(names)): # networking needed
        if end:
                print(f"Dealer's hand: {hands[names[0]]}")
                print(f"Dealer's score: {calculateHandValue(hands[names[0]])}")
                print(f"{names[i]}'s hand: {hands[names[i]]}")
                print(f"{names[i]}'s score: {calculateHandValue(hands[names[i]])}")
                if names[i] in nonbust:
                    determineWinner(names[i])
        else:
            print(f"Dealer's faceup card: {hands[names[0]][0]}")
            print(f"{names[i]}'s hand: {hands[names[i]]}")
            print(f"{names[i]}'s score: {calculateHandValue(hands[names[i]])}")


# possible win/lose/push(tie) screen
def determineWinner(player):
    playerScore = calculateHandValue(hands[player])
    dealerScore = calculateHandValue(hands[names[0]])
    if playerScore > dealerScore:
        Scoring.win(player)        
    elif dealerScore > playerScore:
        Scoring.lose(player)        
    else:
        print("It's a push")    
    if cashout(player, sessionscores):
        exit()

        
# cashout button
def cashout(player, sessionscores):
    print(f"{player} now has {sessionscores[player]} tokens.")
    choice = input(f"{player}, would you like to cash out? (y/n): ").lower()
    if choice == "y":
        Scoring.cashout(player, sessionscores)
        print(f"{player} has cashed out. Their score has been saved.")
        return True
    else:
        print(f"{player} has chosen not to cash out.")
        return False





# main game loop
sessionscores = Scoring.set_players()
names = list(sessionscores.keys())
while True:
    print('A new game will now begin\n')
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
    "d2",
    "d3",
    "d4",
    "d5",
    "d6",
    "d7",
    "d8",
    "d9",
    "d10",
    "dj",
    "dq",
    "dk",
    "da",]
    random.shuffle(deck)   
    nonbust = []
    betamounts, hands = Scoring.wager(sessionscores)
    for name in names: #networking needed
        drawcard(name)
        drawcard(name)
    displayHands()
    for i in reversed(range(len(names))): #networking needed again
        while True:
            if i != 0:
                playerChoice = input(f"Would {names[i]} like to hit or stand? (h/s): ").lower() #button needed to replace choice
                if playerChoice == "h":
                    drawcard(names[i])
                    displayHands()
                    score = calculateHandValue(hands[names[i]])
                    if score > 21:
                        print("Bust!")
                        Scoring.lose(names[i], sessionscores, betamounts)
                        break
                elif playerChoice == "s":
                    print("Player chose to stand.")
                    nonbust.append(names[i])

            else:
                while True:
                    dealerChoice = input("Dealer, would you like to hit or stand? (h/s): ").lower() #button needed to replace choice
                    if dealerChoice == "h":
                        drawcard([names[i]])
                        calculateHandValue(hands[names[0]])
                        displayHands()
                        score = calculateHandValue(hands[names[0]])
                        if score > 21:
                            print("Dealer busts! All non-bust players win.")
                            for name in nonbust:
                                Scoring.win(name, sessionscores, betamounts)
                                cashout(name, sessionscores) #networking needed here as well
                            break
                    elif dealerChoice == "s":
                        print("Dealer chose to stand.")
                        displayHands(True)
                        break

# Where not specified all print statements should be displayed on every computer and then extra data transfer/specific displays where mentioned
