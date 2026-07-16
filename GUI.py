import pygame

import maingameplay
import Scoring
import time


pygame.init()
pygame.font.init()
pygame.display.set_caption("BlackJack")

scrn = pygame.display.set_mode((600, 700))
table_img = pygame.image.load("background.jpg")
hitButton = pygame.image.load("hitbuttonred.png").convert_alpha()
standButton = pygame.image.load("standbuttonred.png").convert_alpha()
blankcard = pygame.image.load("blank card.jpg").convert_alpha()
blankcard = pygame.transform.scale(blankcard, (int(blankcard.get_width() * 0.2), int(blankcard.get_height() * 0.2)))
backcard = pygame.image.load("back card.jpg").convert_alpha()
backcard = pygame.transform.scale(backcard, (int(backcard.get_width() * 0.2), int(backcard.get_height() * 0.2)))
spadecard = pygame.image.load("spade card.jpg").convert_alpha()
spadecard = pygame.transform.scale(spadecard, (int(spadecard.get_width() * 0.2), int(spadecard.get_height() * 0.2)))
diamondcard = pygame.image.load("diamond card.jpg").convert_alpha()
diamondcard = pygame.transform.scale(diamondcard, (int(diamondcard.get_width() * 0.2), int(diamondcard.get_height() * 0.2)))
clubcard = pygame.image.load("club card.jpg").convert_alpha()
clubcard = pygame.transform.scale(clubcard, (int(clubcard.get_width() * 0.2), int(clubcard.get_height() * 0.2)))
heartcard = pygame.image.load("heart card.jpg").convert_alpha()
heartcard = pygame.transform.scale(heartcard, (int(heartcard.get_width() * 0.2), int(heartcard.get_height() * 0.2)))



class Button:
    def __init__(self, x, y, image, scale):
        self.image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        scrn.blit(self.image, (self.rect.x, self.rect.y))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)


def draw_text(text, font_size, color, x, y):
    font = pygame.font.SysFont(None, font_size)
    text_surface = font.render(text, True, color)
    scrn.blit(text_surface, (x, y))


def setup_screen():
    """pygame UI replacement for Scoring.set_players()."""
    high_scores = Scoring.read_scores()
    saved_players = list(high_scores.keys())
    saved_text = ", ".join(saved_players) if saved_players else "None"

    inputs = ["", ""]
    active = 0
    error = ""

    while True:
        scrn.fill((37, 64, 85))
        draw_text("Blackjack - Player Setup", 44, (255, 255, 255), 55, 30)
        draw_text("Previous players: " + saved_text, 24, (180, 180, 180), 50, 90)
        draw_text("Player 1 will be the dealer.", 26, (255, 220, 0), 50, 125)

        labels = ["Dealer (Player 1) name:", "Player 2 name:"]
        for i, (label, value) in enumerate(zip(labels, inputs)):
            y = 200 + i * 150
            draw_text(label, 30, (255, 255, 255), 50, y)
            box_color = (255, 255, 0) if i == active else (200, 200, 200)
            pygame.draw.rect(scrn, box_color, (50, y + 38, 500, 42), 2)
            draw_text(value + ("|" if i == active else ""), 30, (255, 255, 255), 58, y + 48)

        if error:
            draw_text(error, 26, (255, 80, 80), 50, 540)

        pygame.draw.rect(scrn, (0, 160, 0), (190, 590, 220, 55))
        draw_text("Start Game", 32, (255, 255, 255), 215, 605)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i in range(2):
                    y = 200 + i * 150
                    if pygame.Rect(50, y + 38, 500, 42).collidepoint(event.pos):
                        active = i
                if pygame.Rect(190, 590, 220, 55).collidepoint(event.pos):
                    name1, name2 = inputs[0].strip(), inputs[1].strip()
                    if not name1 or not name2:
                        error = "Both names are required."
                    elif name1 == name2:
                        error = "Names must be different."
                    elif ":" in name1 or ":" in name2:
                        error = "Names cannot contain a colon (:)."
                    else:
                        return {name1: 100, name2: 100}
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    active = (active + 1) % 2
                elif event.key == pygame.K_RETURN:
                    active = (active + 1) % 2
                elif event.key == pygame.K_BACKSPACE:
                    inputs[active] = inputs[active][:-1]
                    error = ""
                else:
                    if len(inputs[active]) < 20:
                        inputs[active] += event.unicode
                    error = ""

        pygame.display.update()


def wager_screen(dealer_name, player_name, session_scores):
    """pygame UI replacement for Scoring.wager() calls."""
    inputs = ["", ""]
    active = 0
    error = ""

    while True:
        scrn.fill((37, 64, 85))
        draw_text("Place Your Wagers", 44, (255, 255, 255), 130, 30)

        labels = [
            f"{dealer_name} (Dealer) - {session_scores[dealer_name]} tokens:",
            f"{player_name} - {session_scores[player_name]} tokens:",
        ]
        for i, (label, value) in enumerate(zip(labels, inputs)):
            y = 180 + i * 180
            draw_text(label, 28, (255, 255, 255), 50, y)
            box_color = (255, 255, 0) if i == active else (200, 200, 200)
            pygame.draw.rect(scrn, box_color, (50, y + 38, 300, 42), 2)
            draw_text(value + ("|" if i == active else ""), 30, (255, 255, 255), 58, y + 48)

        if error:
            draw_text(error, 26, (255, 80, 80), 50, 575)

        pygame.draw.rect(scrn, (0, 160, 0), (190, 625, 220, 55))
        draw_text("Place Bets", 32, (255, 255, 255), 220, 640)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i in range(2):
                    y = 180 + i * 180
                    if pygame.Rect(50, y + 38, 300, 42).collidepoint(event.pos):
                        active = i
                if pygame.Rect(190, 625, 220, 55).collidepoint(event.pos):
                    try:
                        w_dealer = int(inputs[0])
                        w_player = int(inputs[1])
                        if w_dealer <= 0 or w_player <= 0:
                            error = "Wagers must be at least 1."
                        elif w_dealer > session_scores[dealer_name]:
                            error = f"{dealer_name} does not have enough tokens."
                        elif w_player > session_scores[player_name]:
                            error = f"{player_name} does not have enough tokens."
                        else:
                            session_scores[dealer_name] -= w_dealer
                            session_scores[player_name] -= w_player
                            return w_dealer, w_player
                    except ValueError:
                        error = "Please enter whole numbers only."
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    active = (active + 1) % 2
                elif event.key == pygame.K_RETURN:
                    active = (active + 1) % 2
                elif event.key == pygame.K_BACKSPACE:
                    inputs[active] = inputs[active][:-1]
                    error = ""
                elif event.unicode.isdigit():
                    inputs[active] += event.unicode
                    error = ""

        pygame.display.update()


def start_round():
    global dealer_revealed
    maingameplay.init_game()
    maingameplay.playerHand.append(maingameplay.drawcard("Player"))
    maingameplay.playerHand.append(maingameplay.drawcard("Player"))
    maingameplay.dealerHand.append(maingameplay.drawcard("Dealer"))
    maingameplay.dealerHand.append(maingameplay.drawcard("Dealer"))
    dealer_revealed = False


def settle_round():
    player_total = maingameplay.calculateHandValue(maingameplay.playerHand)
    dealer_total = maingameplay.calculateHandValue(maingameplay.dealerHand)

    if player_total > dealer_total:
        Scoring.win(player_name, session_scores, player_wager)
        return f"{player_name} wins"
    if dealer_total > player_total:
        Scoring.win(dealer_name, session_scores, dealer_wager)
        return f"{dealer_name} wins"
    return "Tie"

def displaycard(x, card = None):
    if card == None:
        scrn.blit(backcard, (x, 425))
    elif card[0] == "s":
        scrn.blit(spadecard, (x, 425))
    elif card[0] == "d":
        scrn.blit(diamondcard, (x, 425))
    elif card[0] == "c":
        scrn.blit(clubcard, (x, 425))
    elif card[0] == "h":
        scrn.blit(heartcard, (x, 425))

    

session_scores = setup_screen()
players = list(session_scores.keys())
dealer_name = players[0]
player_name = players[1]

# Share names with maingameplay so drawcard() and related helpers work as expected.
maingameplay.names = players

dealer_wager, player_wager = wager_screen(dealer_name, player_name, session_scores)

start_round()

round_over = False
status_text = "Hit or stand"
dealer_revealed = False
run = True

hit_button = Button(50, 600, hitButton, 0.2)
stand_button = Button(450, 600, standButton, 0.2)

while run:
    scrn.fill((37, 64, 85))
    scrn.blit(table_img, (0, 200))

    for i in range(len(maingameplay.dealerHand)):
        time.sleep(0.2) 
        x = 250 - i * 50
        if i == 0 and not dealer_revealed:
            displaycard(x, None)
        else:
            displaycard(x, maingameplay.dealerHand[i])

    for i in range(len(maingameplay.playerHand)):
        x = 350 + i * 50
        displaycard(x, maingameplay.playerHand[i])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if not round_over and hit_button.clicked(event):
            maingameplay.playerHand.append(maingameplay.drawcard("Player"))
            time.sleep(0.2) 
            displaycard(350 + (len(maingameplay.playerHand) - 1) * 50, maingameplay.playerHand[-1])
            player_total = maingameplay.calculateHandValue(maingameplay.playerHand)
            if player_total > 21:
                dealer_revealed = True
                Scoring.win(dealer_name, session_scores, dealer_wager)
                status_text = f"{player_name} busts - {dealer_name} wins"
                round_over = True

        if not round_over and stand_button.clicked(event):
            dealer_revealed = True
            draw_text(f"Dealer ({dealer_name}) total: {maingameplay.calculateHandValue(maingameplay.dealerHand)}", 32, (255, 255, 255), 25, 40)
            displaycard(30, maingameplay.dealerHand[0])
            while maingameplay.calculateHandValue(maingameplay.dealerHand) < 17:
                maingameplay.dealerHand.append(maingameplay.drawcard("Dealer"))
                time.sleep(0.2)
                displaycard(30 + (len(maingameplay.dealerHand) - 1) * 50, maingameplay.dealerHand[-1])
            dealer_total = maingameplay.calculateHandValue(maingameplay.dealerHand)
            if dealer_total > 21:
                Scoring.win(player_name, session_scores, player_wager)
                status_text = f"{dealer_name} busts - {player_name} wins"
            else:
                status_text = settle_round()
            round_over = True

        if round_over and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if pygame.Rect(50, 640, 200, 50).collidepoint(event.pos):
                dealer_wager, player_wager = wager_screen(dealer_name, player_name, session_scores)
                start_round()
                round_over = False
                status_text = "Hit or stand"
            if pygame.Rect(350, 640, 200, 50).collidepoint(event.pos):
                Scoring.cashout(dealer_name, session_scores)
                Scoring.cashout(player_name, session_scores)
                run = False

    if not round_over:
        hit_button.draw()
        stand_button.draw()
    else:
        time.sleep(1)
        pygame.draw.rect(scrn, (0, 140, 0), (50, 640, 200, 50))
        draw_text("New Round", 30, (255, 255, 255), 75, 654)
        pygame.draw.rect(scrn, (160, 0, 0), (350, 640, 200, 50))
        draw_text("Save & Exit", 30, (255, 255, 255), 373, 654)
        
    draw_text(f"{player_name} total: {maingameplay.calculateHandValue(maingameplay.playerHand)}", 38, (255, 255, 255), 25, 85)
    draw_text(f"{dealer_name} tokens: {session_scores[dealer_name]}", 32, (255, 255, 255), 25, 130)
    draw_text(f"{player_name} tokens: {session_scores[player_name]}", 32, (255, 255, 255), 25, 165)
    draw_text(f"Bets - {dealer_name}: {dealer_wager}, {player_name}: {player_wager}", 30, (255, 255, 255), 25, 205)
    draw_text(status_text, 36, (255, 255, 255), 230, 600)

    pygame.display.update()

pygame.quit()