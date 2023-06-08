import time, pygame

class ElMarino:

    def UnderTaker(self, game, moves):
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
            print("Game Over")
            quit()
            
        pygame.display.update()
        

