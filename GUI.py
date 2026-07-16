try:
    import pygame
except ModuleNotFoundError:
    import pygame_ce as pygame

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


def start_round():
    maingameplay.init_game()


def settle_round():
    for name in maingameplay.names[1:]:
        maingameplay.determineWinner(name)
    return "Round over. Start a new round."


session_scores = Scoring.set_players()
players = list(session_scores.keys())
dealer_name = players[0]

# Share names with maingameplay so drawcard() and related helpers work as expected.
maingameplay.names = players
sessionscores = maingameplay.sessionscores
betamounts = maingameplay.betamounts
hands = maingameplay.hands



start_round()

for name in maingameplay.names:

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

    hit_button.draw()
    stand_button.draw()

    draw_text(f"Dealer ({dealer_name}) total: {maingameplay.calculateHandValue(maingameplay.dealerHand)}", 32, (255, 255, 255), 25, 40)
    draw_text(f"{player_name} total: {maingameplay.calculateHandValue(maingameplay.playerHand)}", 38, (255, 255, 255), 25, 85)
    draw_text(f"{dealer_name} tokens: {session_scores[dealer_name]}", 32, (255, 255, 255), 25, 130)
    draw_text(f"{player_name} tokens: {session_scores[player_name]}", 32, (255, 255, 255), 25, 165)
    draw_text(f"Bets - {dealer_name}: {dealer_wager}, {player_name}: {player_wager}", 30, (255, 255, 255), 25, 205)
    draw_text(status_text, 36, (255, 255, 255), 25, 700)

    pygame.display.update()

pygame.quit()