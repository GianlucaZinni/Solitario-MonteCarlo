import pygame
from Deck import Deck
from Waste import Waste
from Foundation import Foundation
from Table import Table
from pygame.locals import RESIZABLE
from tkinter import messagebox
import time


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Solitario")

        info = pygame.display.Info()
        self.window_size = (info.current_w, info.current_h)
        self.screen = pygame.display.set_mode(self.window_size, RESIZABLE)
        self.backgroundImage = pygame.image.load("assets/backgroundd.jpg")

        self.game_is_running = True

        self.deck = Deck()
        self.deck.shuffle()

        self.waste = Waste()
        self.clock = pygame.time.Clock()

        self.holding_cards = []
        self.holding_card_group = None
        self.mouse_cords = ()
        self.moves = 0
        self.timer = 0

        self.place_sound = pygame.mixer.Sound("assets/flip.wav")
        self.shuffle_sound = pygame.mixer.Sound("assets/shuffle.wav")
        self.shuffle_sound.play()

        self.tables = self.create_tables()
        self.foundations = self.create_foundations()
        self.check_if_lock = []

    def create_tables(self):
        tables = []
        x = 25
        for card_amount in range(1, 8):
            tables.append(Table(x, self.deck, card_amount))
            x += 125
            card_amount += 1
        return tables

    def create_foundations(self):
        foundations = []
        x = 400
        suits = ["hearts", "diamonds", "spades", "clubs"]

        for i in range(len(suits)):
            foundations.append(Foundation(x, suits[i]))
            x += 125
        return foundations

    def message_display(self, text, cords):
        large_text = pygame.font.Font("assets/freesansbold.ttf", 17)
        text_surface = large_text.render(text, True, (255, 255, 255))
        TextSurf, TextRect = text_surface, text_surface.get_rect()
        TextRect.center = cords
        self.screen.blit(TextSurf, TextRect)

    def game_loop(self):
        start_time = time.time()
        while self.game_is_running:
            self.timer = int(time.time() - start_time)
            mouse_x, mouse_y = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicked_new_card(mouse_x, mouse_y)
                    self.check_holding_card(mouse_x, mouse_y)

                if event.type == pygame.MOUSEBUTTONUP:
                    if self.holding_cards != []:
                        self.place_card(mouse_x, mouse_y)
                        self.holding_cards = []
                        self.waste.set_cards()

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.screen.blit(self.backgroundImage, (0, 0))

            for table in self.tables:
                for card in table.get_table():
                    if not card in self.holding_cards:
                        pygame.sprite.GroupSingle(card).draw(self.screen)

            for foundation in self.foundations:
                card = foundation.get_top_card()
                if not card in self.holding_cards:
                    pygame.sprite.GroupSingle(card).draw(self.screen)

            for card in self.waste.get_show_waste_pile():
                if not card in self.holding_cards:
                    pygame.sprite.GroupSingle(card).draw(self.screen)

            self.card_follow_mouse(mouse_x, mouse_y)

            self.message_display(str(self.timer), (352, 39))
            self.message_display(str(self.moves), (561, 39))

            pygame.display.update()

            self.clock.tick(60)
            self.auto_solve()
