import random
import Scoring

def init_game():
    global deck, dealerHand, playerHand
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
    "da",
]
    random.shuffle(deck)
    dealerHand = []
    playerHand = []





def drawcard(player):
    if player == "Dealer":
        card = deck.pop()
        return card
    elif player == "Player":
        card = deck.pop()
        return card


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


def displayHands():
    print(f"Dealer's ({names[0]}'s) hand: {dealerHand[0]} and [hidden]")
    print(f"{names[1]}'s hand: {playerHand}")
    print(f"{names[1]}'s score: {calculateHandValue(playerHand)}")


def determineWinner():
    playerScore = calculateHandValue(playerHand)
    dealerScore = calculateHandValue(dealerHand)

    if playerScore > dealerScore:
        print(f"{names[1]} wins!")
        Scoring.win(names[1], sessionscores, playerwager)
        
        
    elif dealerScore > playerScore:
        print(f"Dealer ({names[0]}) wins!")
        Scoring.win(names[0], sessionscores, dealerwager)
        
        
    else:
        print("It's a tie!")
    

    if cashout(names[1], sessionscores):
        print("Thanks for ending the game. Your score has been saved.")
        exit()

        

def cashout(player, sessionscores):
    print(f"{player} now has {sessionscores[player]} tokens.")
    choice = input(f"{player}, would you like to cash out? (y/n): ").lower()
    if choice == "y":
        Scoring.cashout(player, sessionscores)
        print(f"{player} has cashed out. Their score has been saved and reset to 10.")
        return True
    else:
        print(f"{player} has chosen not to cash out.")
        return False
    

def main():
    global sessionscores, names, playerwager, dealerwager
    sessionscores = Scoring.set_players()
    names = list(sessionscores.keys())

    while True:
        init_game()
        print('A new round will now begin\n')
        playerwager = Scoring.wager(names[1], sessionscores)
        dealerwager = Scoring.wager(names[0], sessionscores)
        for x in range(2):
            playerHand.append(drawcard("Player"))
            dealerHand.append(drawcard("Dealer"))

        # main game loop
        displayHands()

        while True:
            playerChoice = input(f"{names[1]}, would you like to hit or stand? (h/s): ").lower()
            if playerChoice == "h":
                playerHand.append(drawcard("Player"))
                displayHands()
                score = calculateHandValue(playerHand)
                if score > 21:
                    print(f"{names[1]} busts! Dealer ({names[0]}) wins.")
                    Scoring.win(names[0], sessionscores, dealerwager)
                    cashout(names[0], sessionscores)
                    break

            elif playerChoice == "s":
                print(f"{names[1]} chose to stand.")
                print(f"Dealer's ({names[0]}'s) hand: {dealerHand}")
                print(f"Dealer's ({names[0]}'s) score: {calculateHandValue(dealerHand)}")
                while True:
                    dealerChoice = input(f"{names[0]}, would you like to hit or stand? (h/s): ").lower()
                    if dealerChoice == "h":
                        dealerHand.append(drawcard("Dealer"))
                        calculateHandValue(dealerHand)
                        score = calculateHandValue(dealerHand)
                        print(f"Dealer's ({names[0]}'s) hand: {dealerHand}")
                        print(f"Dealer's ({names[0]}'s) score: {calculateHandValue(dealerHand)}")
                        if score > 21:
                            print(f"Dealer ({names[0]}) busts! {names[1]} wins.")
                            Scoring.win(names[1], sessionscores, playerwager)

                            cashout(names[1], sessionscores)
                            break
                    elif dealerChoice == "s":
                        print(f"Dealer ({names[0]}) chose to stand.")
                        determineWinner()
                        break


if __name__ == "__main__":
    main()
