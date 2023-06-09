class ElMarino:
    
    def __init__(self):
        self.primer_llamado = True
        
    def call(self):
        if self.primer_llamado:
            print("Se ha iniciado El Marino, mi última adquisición.")
            self.primer_llamado = False
        else:
            pass
    
    def UnderTaker(self, game, moves):
        self.call()
        moved = False
        
        check_if_moved = True
        
        for table in game.tables:
            
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
        if True not in last_twentyfour:
            game.result_counter = 5
            return

class LaSocialista:
    
    def __init__(self):
        self.primer_llamado = True

    def call(self):
        if self.primer_llamado:
            print("Se ha iniciado La Socialista y su era dictatorial.")
            self.primer_llamado = False
        else:
            pass

    def Gestionadora(self, game, moves):
        self.call()
        moved = False
        
        check_if_moved = True
        
        for table in game.tables:
            
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
        if True not in last_twentyfour:
            game.result_counter = 5
            return

class ElBombero:

    def __init__(self):
        self.primer_llamado = True

    def call(self):
        if self.primer_llamado:
            print("Se ha iniciado El Bombero, la salvación.")
            self.primer_llamado = False
        else:
            pass

    def ApagaLlamas(self, game, moves):
        self.call()
        moved = False
        
        check_if_moved = True
        
        for table in game.tables:
            
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
        if True not in last_twentyfour:
            game.result_counter = 5
            return