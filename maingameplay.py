import random


deck = [
    "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "sj", "sq", "sk", "sa",
    "h2", "h3", "h4", "h5", "h6", "h7", "h8", "h9", "h10", "hj", "hq", "hk", "ha",
    "c2", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "cj", "cq", "ck", "ca",
    "d2", "d3", "d4", "d5", "d6", "d7", "d8", "d9", "d10", "d", "dq", "dk", "da"
]
dealerHand = []
playerHand = []
dealertokens = 10
playertokens = 10

random.shuffle(deck)

def drawcard():
    card = deck.pop()
    print(f"You drew: {card}")
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

while True:
    try:
        dealerWager = int(input("Dealer, how many tokens would you like to wager? "))
        dealertokens -= int(dealerWager)
        break
    except ValueError:
        print("Invalid input. Please enter a valid number of tokens.")



for x in range(2):    
    playerHand.append(drawcard())
    dealerHand.append(drawcard())



#main game loop
displayHands()

while True:
    playerChoice = input("Would you like to hit or stand? (h/s): ").lower()
    if playerChoice == "h":
        playerHand.append(drawcard())
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
                dealerHand.append(drawcard())
                calculateHandValue(dealerHand)
                displayHands()
                score = calculateHandValue(playerHand)
            if score > 21:
                print("Dealer busts! Player wins.")
                break
            elif dealerChoice == "s":
                print("Dealer chose to stand.")
        





