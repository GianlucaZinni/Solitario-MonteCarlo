from abc import ABC, abstractmethod
import random

class Strategy(ABC):
    def __init__(self):
        self.primer_llamado = True

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
        if True in game.check_if_lock:
            game.check_if_lock.clear()
            return
        if True not in game.check_if_lock and len(game.check_if_lock) >= 24:
            game.result_counter = 5
            return

class LaSocialista(Strategy):
    
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
        if True in game.check_if_lock:
            game.check_if_lock.clear()
            return
        if True not in game.check_if_lock and len(game.check_if_lock) >= 24:
            game.result_counter = 5
            return

class ElBombero(Strategy):

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
    
        if (not moved and len(game.deck.get_deck()) > 0 
            or len(game.waste.get_waste_pile()) > 0):
            if not game.waste.show_is_empty():
                moved = moves.check_waste_card(game, moved)
        
        if not moved and len(game.deck.get_deck()) <= 0:
            game.deck.add_cards(list(
                reversed(game.waste.get_waste_pile().copy())
                ))
            game.waste.empty()
            game.moves += 1
            check_if_moved = False
        
        if not moved and len(game.deck.get_deck()) > 0:
            game.waste.add_card(game.deck.remove_card())
            game.moves += 1
            check_if_moved = False
        
        game.check_if_lock.append(check_if_moved)
        if True in game.check_if_lock:
            game.check_if_lock.clear()
            return
        if (True not in game.check_if_lock 
            and len(game.check_if_lock) >= 24):
            game.result_counter = 5
            return

class ElGobernador(Strategy):
    
    def call(self):
        if self.primer_llamado:
            print("Se ha iniciado El Gobernador, el generador de infortunios.")
            self.primer_llamado = False
            
    def Progresismo(self, game, moves):
        self.call()
        moved = False
        
        check_if_moved = True
        
        functions = {
            1: moves.bottom_card_foundation,
            2: moves.bottom_card_table,
            3: moves.prev_to_foundation,
            4: moves.foundation_to_table_and_table_to_table,
            5: moves.foundation_to_table_x2_and_table_to_table,
        }
        
        for table in game.tables:
            
            card = table.bottom_card()
            if card is not None:
                selected_function = functions.get(random.randint(1, len(functions)))
                moved = selected_function(game, card, table, moved)
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
        if True in game.check_if_lock:
            game.check_if_lock.clear()
            return
        if True not in game.check_if_lock and len(game.check_if_lock) >= 24:
            game.result_counter = 5
            return