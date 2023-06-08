import pygame
from game_config.Deck import Deck
from game_config.Waste import Waste
from game_config.Foundation import Foundation
from game_config.Table import Table
from pygame.locals import RESIZABLE
from tkinter import messagebox
import time

class Game:
    def __init__(self):

        pygame.init()

        self.window_size = (900, 885)

        self.screen = pygame.display.set_mode(self.window_size, RESIZABLE)

        pygame.display.set_caption("Solitario")

        self.game_is_running = True

        self.backgroundImage = pygame.image.load("static/assets/backgroundd.jpg")


        self.deck = Deck()

        self.deck.shuffle()

        self.waste = Waste()
        self.clock = pygame.time.Clock()

        self.holding_cards = []
        self.holding_card_group = None
        self.mouse_cords = ()
        self.moves = 0
        self.score = 0
        self.frame = 0
        self.timer = 0

        self.place_sound = pygame.mixer.Sound('/static/assets/flip.wav')
        self.shuffle_sound = pygame.mixer.Sound('/static/assets/shuffle.wav')
        self.shuffle_sound.play()

        self.tables = self.create_tables()
        self.foundations = self.create_foundations()
        self.check_if_lock = []

    def clicked_new_card(self, mouse_x, mouse_y):

        if mouse_x > 9 and mouse_x < 106 and mouse_y > 14 and mouse_y < 155:

            if len(self.deck.get_deck()) <= 0:
                self.deck.add_cards(list(reversed(self.waste.get_waste_pile().copy())))
                self.waste.empty()
                self.shuffle_sound.play()
            else:
                self.moves += 1
                self.waste.add_card(self.deck.remove_card())
                self.place_sound.play()

    def check_holding_card(self, mouse_x, mouse_y):

        possible_cards = []
        self.mouse_cords = (mouse_x, mouse_y)

        for table in self.tables:
            for table_card in table.get_table():
                if table_card.is_front_showing():
                    possible_cards.append((table_card, table))

        for foundation in self.foundations:
            foundation_card = foundation.get_top_card()
            if foundation_card!=None:
                possible_cards.append((foundation_card, foundation))

        waste_card = self.waste.get_top_card()
        if waste_card!=None:
            possible_cards.append((waste_card, self.waste))
        

        for card in possible_cards:
            card_x = card[0].get_coordinates()[0]
            card_y = card[0].get_coordinates()[1]
            if mouse_x > card_x and mouse_x < card_x + 100 and mouse_y>card_y and mouse_y < card_y + 145:
                self.holding_card_group = card[1]
                if self.holding_card_group in self.tables:
                    self.holding_cards = self.holding_card_group.get_cards_below(card[0])
                else:
                    self.holding_cards = [card[0]]

    def place_card(self, mouse_x, mouse_y):
        
        if self.mouse_cords == (mouse_x, mouse_y):
            if len(self.holding_cards)==1:
                for foundation in self.foundations:
                    if foundation.get_suit() == self.holding_cards[0].get_suit():
                        foundation_card = foundation.get_top_card()
                        if foundation_card!=None:
                            if foundation_card.get_value()+1 == self.holding_cards[0].get_value():
                                foundation.add_card(self.holding_cards[0])
                                self.holding_card_group.remove_card()
                                self.place_sound.play()
                                self.moves += 1
                                return
                        else:
                            if self.holding_cards[0].get_value() == 1:
                                foundation.add_card(self.holding_cards[0])
                                self.holding_card_group.remove_card()
                                self.place_sound.play()
                                self.moves += 1
                                return

            for table in self.tables:
                bottom_card = table.bottom_card()
                if bottom_card!=None:
                    value = bottom_card.get_value()
                    if bottom_card.get_color()!=self.holding_cards[0].get_color() and value-1==self.holding_cards[0].get_value():
                        table.add_cards(self.holding_cards)
                        for card in self.holding_cards:
                            self.holding_card_group.remove_card()
                            self.place_sound.play()
                            self.moves += 1
                        return
                else:
                    if self.holding_cards[0].get_value() == 13:
                        table.add_cards(self.holding_cards)
                        for card in self.holding_cards:
                            self.holding_card_group.remove_card()
                        self.place_sound.play()
                        self.moves += 1
                        return
                    

        else:
            positions = [950, 825, 710, 590, 470, 355, 242, 120]
            count = 0

            for pos in positions:
                if mouse_x > pos:
                    break
                count += 1
            
            if count > 0:
                table = self.tables[7-count]
                bottom_card = table.bottom_card()
                
                if bottom_card != None:
                    value = bottom_card.get_value()
                    if bottom_card.get_color() != self.holding_cards[0].get_color() and value - 1 == self.holding_cards[0].get_value():
                        table.add_cards(self.holding_cards)
                        for card in self.holding_cards:
                            self.holding_card_group.remove_card()
                            self.place_sound.play()
                            self.moves+=1
                        return
                else: 
                    
                    if self.holding_cards[0].get_value() == 13:
                        table.add_cards(self.holding_cards)
                        for card in self.holding_cards:
                            self.holding_card_group.remove_card()
                        self.place_sound.play()
                        self.moves += 1
                        return
            else:
                
                for foundation in self.foundations:
                    
                    if foundation.get_suit() == self.holding_cards[0].get_suit():
                        
                        foundation_card = foundation.get_top_card()
                        
                        if foundation_card != None:
                            
                            if foundation_card.get_value()+1 == self.holding_cards[0].get_value():
                                foundation.add_card(self.holding_cards[0])
                                self.holding_card_group.remove_card()
                                self.place_sound.play()
                                self.moves += 1
                                return
                        else:
                            
                            if self.holding_cards[0].get_value() == 1:
                                
                                foundation.add_card(self.holding_cards[0])
                                self.holding_card_group.remove_card()
                                self.place_sound.play()
                                self.moves += 1
                                return

        self.holding_card_group.set_cards()

    def card_follow_mouse(self, mouse_x, mouse_y):
        
        if self.holding_cards != []:
            
            x = mouse_x - 50
            y = mouse_y - 50
            pos = 0
            
            for card in self.holding_cards:
                card.set_coordinates(x, y + (pos * 40))
                pygame.sprite.GroupSingle(card).draw(self.screen)
                pos += 1

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
        large_text = pygame.font.Font('/static/assets/Roboto-Bold.ttf',17)
        text_surface = large_text.render(text, True, (255,255,255))
        TextSurf, TextRect = text_surface, text_surface.get_rect()
        TextRect.center = cords
        self.screen.blit(TextSurf, TextRect)

    def check_win(self):
        count = 0
        for foundation in self.foundations:
            complete_pile = foundation.get_Foundation()
            if len(complete_pile) != 13:
                return
            else:
                count += 1
        print("check_win:", count)
        if count == 4:
            
            count += 1
            x = messagebox.askquestion(message="¿Do you want to play again?", title="You win the game!")
            if x == 'yes':
                pygame.quit()
                self.game_loop()
                # Ver como hacer para resetear el juego.
            else:
                pygame.quit()
                quit()

    def auto_solve(self):
        moved = False
        
        check_if_moved = True
        
        for table in self.tables:
            
            card = table.bottom_card()
            if card is not None:
                moved = self.bottom_card_foundation(card, table, moved)
                if not moved:
                    moved = self.bottom_card_table(card, table, moved)
                    if not moved:
                        cards = table.get_showing_cards(table.get_table())
                        if len(cards[0]) > 1:
                            moved = self.upper_card_table(cards, table, moved)
        
        if not moved and len(self.deck.get_deck()) > 0 or len(self.waste.get_waste_pile()) > 0:
            if not self.waste.show_is_empty():
                moved = self.check_waste_card(moved)
        
        if not moved and len(self.deck.get_deck()) <= 0:
            self.deck.add_cards(list(reversed(self.waste.get_waste_pile().copy())))
            self.waste.empty()
            self.moves += 1
            check_if_moved = False
        
        if not moved and len(self.deck.get_deck()) > 0:
            self.waste.add_card(self.deck.remove_card())
            self.moves += 1
            check_if_moved = False
        
        self.check_if_lock.append(check_if_moved)
        last_twentyfour = self.check_if_lock[-24:]
        if True not in last_twentyfour:
            print("Game Over")
            quit()
            
        pygame.display.update()

                
    def check_waste_card(self, moved):
        waste_card = self.waste.get_top_card()
        if waste_card is not None:
            moved = self.waste_card_foundation(waste_card, moved)
            if not moved:
                moved = self.waste_card_table(waste_card, moved)
        return moved

    def bottom_card_foundation(self, card, table, moved):
        for foundation in self.foundations:
            if foundation.get_suit() == card.get_suit():
                if card.get_value() == 1:
                    foundation.add_card(card)
                    table.remove_card()
                    moved = True
                    self.moves += 1
                    time.sleep(0.2)
                    break
                else:
                    foundation_card = foundation.get_top_card()
                    if foundation_card is not None:
                        if foundation_card.get_value() + 1 == card.get_value():
                            foundation.add_card(card)
                            table.remove_card()
                            moved = True
                            self.moves += 1
                            time.sleep(0.2)
                            break
        return moved

    def waste_card_foundation(self, waste_card, moved):
        for foundation in self.foundations:
            if waste_card is not None:
                if foundation.get_suit() == waste_card.get_suit():
                    if waste_card.get_value() == 1:
                        foundation.add_card(waste_card)
                        self.waste.remove_card()
                        moved = True
                        self.moves += 1
                        time.sleep(0.2)
                        break
                    else:
                        foundation_card = foundation.get_top_card()
                        if foundation_card is not None:
                            if foundation_card.get_value() + 1 == waste_card.get_value():
                                foundation.add_card(waste_card)
                                self.waste.remove_card()
                                moved = True
                                self.moves += 1
                                time.sleep(0.2)
                                break
        return moved

    def bottom_card_table(self, card, table, moved):
        for dest_table in self.tables:
            if dest_table != table:
                dest_card = dest_table.bottom_card()
                if dest_card is None:
                    if card.get_value() == 13:
                        prev_card = table.prev_card()
                        if prev_card is not None:
                            if not prev_card.is_front_showing():
                                dest_table.add_new_card(card)
                                table.remove_card()
                                moved = True
                                self.moves += 1
                                time.sleep(0.2)
                        else:
                            dest_table.add_new_card(card)
                            table.remove_card()
                            moved = True
                            self.moves += 1
                            time.sleep(0.2)
                        
                else:
                    if dest_card.get_color() != card.get_color():
                        if dest_card.get_value() - 1 == card.get_value():
                            prev_card = table.prev_card()
                            if prev_card is not None:
                                if not prev_card.is_front_showing():
                                    dest_table.add_new_card(card)
                                    table.remove_card()
                                    moved = True
                                    self.moves += 1
                                    time.sleep(0.2)
                                    break

        return moved

    def waste_card_table(self, card, moved):
        for dest_table in self.tables:
            dest_card = dest_table.bottom_card()
            if dest_card is not None:
                if dest_card.get_color() != card.get_color():
                    if dest_card.get_value() - 1 == card.get_value():
                        dest_table.add_new_card(card)
                        self.waste.remove_card()
                        moved = True
                        self.moves += 1
                        time.sleep(0.2)
                        break
            else:
                if card.get_value() == 13:
                    dest_table.add_new_card(card)
                    # hay un error aca.
                    self.waste.remove_card()
                    moved = True
                    self.moves += 1
                    time.sleep(0.2)
        return moved

    def upper_card_table(self, cards, table, moved):
        for dest_table in self.tables:
            if dest_table != table:
                dest_card = dest_table.bottom_card()
                if dest_card is None:
                    if cards[0][0].get_value() == 13:
                        if cards[1] == True:
                            return
                        else:
                            dest_table.add_cards(cards[0])
                            for card in cards[0]:
                                table.remove_card()
                            cards[0].clear()
                            moved = True
                            self.moves += 1
                            time.sleep(0.2)
                            break

                if dest_card is not None:
                    if dest_card.get_color() != cards[0][0].get_color():
                        if dest_card.get_value() - 1 == cards[0][0].get_value():
                            dest_table.add_cards(cards[0])
                            for card in cards[0]:
                                table.remove_card()
                            moved = True
                            self.moves += 1
                            time.sleep(0.2)
                            break
        return moved

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
                        
                if event.type==pygame.QUIT:
                    pygame.quit()
                    quit()

            self.screen.blit(self.backgroundImage, (0, 0))

            for table in self.tables:
                for card in table.get_table():
                    if not card in self.holding_cards:
                        pygame.sprite.GroupSingle(card).draw( self.screen)

            for foundation in self.foundations:
                card = foundation.get_top_card()
                if not card in self.holding_cards:
                    pygame.sprite.GroupSingle(card).draw( self.screen)

            for card in self.waste.get_show_waste_pile():
                if not card in self.holding_cards:
                    pygame.sprite.GroupSingle(card).draw( self.screen)

            self.card_follow_mouse(mouse_x, mouse_y)

            self.message_display(str(self.timer), (352, 39))
            self.message_display(str(self.moves), (561, 39))

            pygame.display.update()
            
            self.clock.tick(60)
            self.auto_solve()