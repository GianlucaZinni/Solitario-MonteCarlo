from abc import ABC, abstractmethod

class Strategy(ABC):
    def __init__(self):
        self.primer_llamado = True
        self.primer_movimiento = True

    @abstractmethod
    def call(self):
        pass

class ElMarino(Strategy):
    
    def call(self):
        if self.primer_llamado:
            print("Se ha iniciado El Marino, mi última adquisición.")
            self.primer_llamado = False
            
    def UnderTaker(self, game, moves):
        self.call()
        moved = False
        
        check_if_moved = True
        
        for table in reversed(game.tables):
            
            card = table.bottom_card()
            if card is not None:
                moved = moves.bottom_card_foundation(game, card, table, moved)
                if not moved:
                    moved = moves.bottom_card_table(game, card, table, moved)
                    if not moved:
                        moved = moves.prev_to_foundation(game, card, table, moved)
                        if not moved:
                            moved = moves.foundation_to_table_and_table_to_table(game, card, table, moved)
                            if not moved:
                                moved = moves.foundation_to_table_x2_and_table_to_table(game, card, table, moved)
                                if not moved:
                                    cards = table.get_showing_cards(table.get_table())
                                    if len(cards[0]) > 1:
                                        moved = moves.upper_card_table(game, cards, table, moved)
                            
        if not moved and len(game.deck.get_deck()) > 0 or len(game.waste.get_waste_pile()) > 0:
            if not game.waste.show_is_empty():
                moved = moves.check_waste_card(game, moved)
        
        if not moved and len(game.deck.get_deck()) <= 0:
            game.deck.add_cards(list(reversed(game.waste.get_waste_pile().copy())))
            game.waste.empty()
            game.moves += 1
            check_if_moved = False
        
        if not moved and len(game.deck.get_deck()) > 0:
            game.waste.add_card(game.deck.remove_card())
            game.moves += 1
            check_if_moved = False
        
        game.check_if_lock.append(check_if_moved)
        last_twentyfour = game.check_if_lock[-24:]
        if not self.primer_movimiento and True not in last_twentyfour:
            game.result_counter = 5
            return
        else:
            self.primer_movimiento = False

class LaSocialista(Strategy): # Primero intenta entre mismas tables y despues foundation
    
    def call(self):
        if self.primer_llamado:
            print("Se ha iniciado La Socialista y su era dictatorial.")
            self.primer_llamado = False

    def Gestionadora(self, game, moves):
        self.call()
        moved = False
        
        check_if_moved = True
        
        for table in game.tables:
            card = table.bottom_card()
            if card is not None:
                moved = moves.bottom_card_table(game, card, table, moved)
                if not moved:
                    moved = moves.bottom_card_foundation(game, card, table, moved)
                    if not moved:
                        cards = table.get_showing_cards(table.get_table())
                        if len(cards[0]) > 1:
                            moved = moves.upper_card_table(game, cards, table, moved)
        
        if not moved and len(game.deck.get_deck()) > 0 or len(game.waste.get_waste_pile()) > 0:
            if not game.waste.show_is_empty():
                moved = moves.check_waste_card(game, moved)
        
        if not moved and len(game.deck.get_deck()) <= 0:
            game.deck.add_cards(list(reversed(game.waste.get_waste_pile().copy())))
            game.waste.empty()
            game.moves += 1
            check_if_moved = False
        
        if not moved and len(game.deck.get_deck()) > 0:
            game.waste.add_card(game.deck.remove_card())
            game.moves += 1
            check_if_moved = False
        
        game.check_if_lock.append(check_if_moved)
        last_twentyfour = game.check_if_lock[-24:]
        if not self.primer_movimiento and True not in last_twentyfour:
            game.result_counter = 5
            return
        else:
            self.primer_movimiento = False

class ElBombero(Strategy): # Primero intenta al foundation y después entre las tables

    def call(self):
        if self.primer_llamado:
            print("Se ha iniciado El Bombero, la salvación.")
            self.primer_llamado = False

    def ApagaLlamas(self, game, moves):
        self.call()
        moved = False
        
        check_if_moved = True
        
        for table in reversed(game.tables):
            card = table.bottom_card()
            if card is not None:
                moved = moves.bottom_card_foundation(game, card, table, moved)
                if not moved:
                    moved = moves.bottom_card_table(game, card, table, moved)
                    if not moved:
                        cards = table.get_showing_cards(table.get_table())
                        if len(cards[0]) > 1:
                            moved = moves.upper_card_table(game, cards, table, moved)
    
        if not moved and len(game.deck.get_deck()) > 0 or len(game.waste.get_waste_pile()) > 0:
            if not game.waste.show_is_empty():
                moved = moves.check_waste_card(game, moved)
        
        if not moved and len(game.deck.get_deck()) <= 0:
            game.deck.add_cards(list(reversed(game.waste.get_waste_pile().copy())))
            game.waste.empty()
            game.moves += 1
            check_if_moved = False
        
        if not moved and len(game.deck.get_deck()) > 0:
            game.waste.add_card(game.deck.remove_card())
            game.moves += 1
            check_if_moved = False
        
        game.check_if_lock.append(check_if_moved)
        last_twentyfour = game.check_if_lock[-24:]
        if not self.primer_movimiento and True not in last_twentyfour:
            game.result_counter = 5
            return
        else:
            self.primer_movimiento = False
