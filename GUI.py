import pygame

import maingameplay
import Scoring


pygame.init()
pygame.font.init()
pygame.display.set_caption("BlackJack")

scrn = pygame.display.set_mode((600, 800))
table_img = pygame.image.load("BlackJack_Table.jpg")
hitButton = pygame.image.load("hitbuttonred.png").convert_alpha()
standButton = pygame.image.load("standbuttonred.png").convert_alpha()
blankCard = pygame.image.load("blank card.jpg").convert_alpha()
blankCard = pygame.transform.scale(blankCard, (int(blankCard.get_width() * 0.2), int(blankCard.get_height() * 0.2)))


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
                        return {name1: 10, name2: 10}
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
    maingameplay.init_game()
    maingameplay.playerHand.append(maingameplay.drawcard("Player"))
    maingameplay.playerHand.append(maingameplay.drawcard("Player"))
    maingameplay.dealerHand.append(maingameplay.drawcard("Dealer"))
    maingameplay.dealerHand.append(maingameplay.drawcard("Dealer"))


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
run = True

hit_button = Button(50, 600, hitButton, 0.2)
stand_button = Button(450, 600, standButton, 0.2)

while run:
    scrn.fill((37, 64, 85))
    scrn.blit(table_img, (0, 200))

    for i in range(len(maingameplay.dealerHand)):
        x = 30 + i * 50
        scrn.blit(blankCard, (x, 425))
    for i in range(len(maingameplay.playerHand)):
        x = 350 + i * 50
        scrn.blit(blankCard, (x, 425))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if not round_over and hit_button.clicked(event):
            maingameplay.playerHand.append(maingameplay.drawcard("Player"))
            player_total = maingameplay.calculateHandValue(maingameplay.playerHand)
            if player_total > 21:
                Scoring.win(dealer_name, session_scores, dealer_wager)
                status_text = f"{player_name} busts - {dealer_name} wins"
                round_over = True

        if not round_over and stand_button.clicked(event):
            while maingameplay.calculateHandValue(maingameplay.dealerHand) < 17:
                maingameplay.dealerHand.append(maingameplay.drawcard("Dealer"))
            dealer_total = maingameplay.calculateHandValue(maingameplay.dealerHand)
            if dealer_total > 21:
                Scoring.win(player_name, session_scores, player_wager)
                status_text = f"{dealer_name} busts - {player_name} wins"
            else:
                status_text = settle_round()
            round_over = True

        if round_over and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if pygame.Rect(50, 740, 200, 50).collidepoint(event.pos):
                dealer_wager, player_wager = wager_screen(dealer_name, player_name, session_scores)
                start_round()
                round_over = False
                status_text = "Hit or stand"
            if pygame.Rect(350, 740, 200, 50).collidepoint(event.pos):
                Scoring.cashout(dealer_name, session_scores)
                Scoring.cashout(player_name, session_scores)
                run = False

    if not round_over:
        hit_button.draw()
        stand_button.draw()
    else:
        pygame.draw.rect(scrn, (0, 140, 0), (50, 740, 200, 50))
        draw_text("New Round", 30, (255, 255, 255), 75, 754)
        pygame.draw.rect(scrn, (160, 0, 0), (350, 740, 200, 50))
        draw_text("Save & Exit", 30, (255, 255, 255), 373, 754)

    draw_text(f"Dealer ({dealer_name}) total: {maingameplay.calculateHandValue(maingameplay.dealerHand)}", 32, (255, 255, 255), 25, 40)
    draw_text(f"{player_name} total: {maingameplay.calculateHandValue(maingameplay.playerHand)}", 38, (255, 255, 255), 25, 85)
    draw_text(f"{dealer_name} tokens: {session_scores[dealer_name]}", 32, (255, 255, 255), 25, 130)
    draw_text(f"{player_name} tokens: {session_scores[player_name]}", 32, (255, 255, 255), 25, 165)
    draw_text(f"Bets - {dealer_name}: {dealer_wager}, {player_name}: {player_wager}", 30, (255, 255, 255), 25, 205)
    draw_text(status_text, 36, (255, 255, 255), 25, 700)

    pygame.display.update()

pygame.quit()