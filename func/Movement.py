import pygame, time

class BasicMoves:
    def __init__(self):
        
        self.mouse_x = 0
        self.mouse_y = 0
        
    def update_mouse_position(self, mouse_x, mouse_y):  # Actualiza la posición del mouse
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        
    def card_follow_mouse(self, game): # Función que genera el efecto de arrastrar una carta
        
        mouse_x = self.mouse_x
        mouse_y = self.mouse_y
        
        if game.holding_cards != []:
            
            x = mouse_x - 50
            y = mouse_y - 50
            pos = 0
            
            for card in game.holding_cards:
                card.set_coordinates(x, y + (pos * 40))
                pygame.sprite.GroupSingle(card).draw(game.screen)
                pos += 1

    
    def clicked_new_card(self, game): # Agrega una carta de la pila no visible a la pila visible
        
        mouse_x = self.mouse_x
        mouse_y = self.mouse_y
        
        if mouse_x > 25 and mouse_x < 125 and mouse_y > 68 and mouse_y < 210:
            if len(game.deck.get_deck()) <= 0:
                game.deck.add_cards(list(reversed(game.waste.get_waste_pile().copy())))
                game.waste.empty()
            else:
                game.moves += 1
                game.waste.add_card(game.deck.remove_card())
                game.place_sound.play()

    def check_holding_card(self, game): # Verifica si se está sosteniendo una carta
        
        mouse_x = self.mouse_x
        mouse_y = self.mouse_y
        
        possible_cards = []
        game.mouse_cords = (mouse_x, mouse_y)

        for table in game.tables:
            for table_card in table.get_table():
                if table_card.is_front_showing():
                    possible_cards.append((table_card, table))

        for foundation in game.foundations:
            foundation_card = foundation.get_top_card()
            if foundation_card is not None:
                possible_cards.append((foundation_card, foundation))

        waste_card = game.waste.get_top_card()
        if waste_card is not None:
            possible_cards.append((waste_card, game.waste))

        for card in possible_cards:
            card_x = card[0].get_coordinates()[0]
            card_y = card[0].get_coordinates()[1]
            if (
                mouse_x > card_x
                and mouse_x < card_x + 100
                and mouse_y > card_y
                and mouse_y < card_y + 145
            ):
                game.holding_card_group = card[1]
                if game.holding_card_group in game.tables:
                    game.holding_cards = game.holding_card_group.get_cards_below(
                        card[0]
                    )
                else:
                    game.holding_cards = [card[0]]

    def place_card(self, game): # Función que coloca una carta en una pila automáticamente con un click
        
        mouse_x = self.mouse_x
        mouse_y = self.mouse_y
        
        if game.mouse_cords == (mouse_x, mouse_y):
            if len(game.holding_cards) == 1:
                for foundation in game.foundations:
                    if foundation.get_suit() == game.holding_cards[0].get_suit():
                        foundation_card = foundation.get_top_card()
                        if foundation_card != None:
                            if (
                                foundation_card.get_value() + 1
                                == game.holding_cards[0].get_value()
                            ):
                                foundation.add_card(game.holding_cards[0])
                                game.holding_card_group.remove_card()
                                game.place_sound.play()
                                game.moves += 1
                                return
                        else:
                            if game.holding_cards[0].get_value() == 1:
                                foundation.add_card(game.holding_cards[0])
                                game.holding_card_group.remove_card()
                                game.place_sound.play()
                                game.moves += 1
                                return

            for table in game.tables:
                bottom_card = table.bottom_card()
                if bottom_card != None:
                    value = bottom_card.get_value()
                    if (
                        bottom_card.get_color() != game.holding_cards[0].get_color()
                        and value - 1 == game.holding_cards[0].get_value()
                    ):
                        table.add_cards(game.holding_cards)
                        for _ in game.holding_cards:
                            game.holding_card_group.remove_card()
                            game.place_sound.play()
                            game.moves += 1
                        return
                else:
                    if game.holding_cards[0].get_value() == 13:
                        table.add_cards(game.holding_cards)
                        for _ in game.holding_cards:
                            game.holding_card_group.remove_card()
                        game.place_sound.play()
                        game.moves += 1
                        return

        else:
            positions = [950, 825, 710, 590, 470, 355, 242, 120]
            count = 0

            for pos in positions:
                if mouse_x > pos:
                    break
                count += 1

            if count > 0:
                table = game.tables[7 - count]
                bottom_card = table.bottom_card()

                if bottom_card != None:
                    value = bottom_card.get_value()
                    if (
                        bottom_card.get_color() != game.holding_cards[0].get_color()
                        and value - 1 == game.holding_cards[0].get_value()
                    ):
                        table.add_cards(game.holding_cards)
                        for _ in game.holding_cards:
                            game.holding_card_group.remove_card()
                            game.place_sound.play()
                            game.moves += 1
                        return
                else:
                    if game.holding_cards[0].get_value() == 13:
                        table.add_cards(game.holding_cards)
                        for _ in game.holding_cards:
                            game.holding_card_group.remove_card()
                        game.place_sound.play()
                        game.moves += 1
                        return
            else:
                for foundation in game.foundations:
                    if foundation.get_suit() == game.holding_cards[0].get_suit():
                        foundation_card = foundation.get_top_card()

                        if foundation_card != None:
                            if (
                                foundation_card.get_value() + 1
                                == game.holding_cards[0].get_value()
                            ):
                                foundation.add_card(game.holding_cards[0])
                                game.holding_card_group.remove_card()
                                game.place_sound.play()
                                game.moves += 1
                                return
                        else:
                            if game.holding_cards[0].get_value() == 1:
                                foundation.add_card(game.holding_cards[0])
                                game.holding_card_group.remove_card()
                                game.place_sound.play()
                                game.moves += 1
                                return

        game.holding_card_group.set_cards()

    # Movimientos automáticos

    def check_waste_card(self, game, moved): # Función que comprueba si la carta de descarte se puede colocar en una pila automáticamente
        waste_card = game.waste.get_top_card()
        if waste_card is not None:
            moved = self.waste_card_foundation(game, waste_card, moved)
            if not moved:
                moved = self.waste_card_table(game, waste_card, moved)
                if not moved:
                    moved = self.foundation_to_table_deck_to_table(game, waste_card, moved)
        return moved

    def bottom_card_foundation(self, game, card, table, moved): # Función que comprueba si la carta de la parte inferior de una tabla se puede colocar en un foundation automáticamente
        for foundation in game.foundations:
            if foundation.get_suit() == card.get_suit():
                if card.get_value() == 1:
                    foundation.add_card(card)
                    table.remove_card()
                    moved = True
                    game.moves += 1
                    time.sleep(0.2)
                    break
                else:
                    foundation_card = foundation.get_top_card()
                    if foundation_card is not None:
                        if foundation_card.get_value() + 1 == card.get_value():
                            foundation.add_card(card)
                            table.remove_card()
                            moved = True
                            game.moves += 1
                            time.sleep(0.2)
                            break
        return moved

    def waste_card_foundation(self, game, waste_card, moved): # Función que comprueba si la carta de descarte se puede colocar en una foundation automáticamente
        for foundation in game.foundations:
            if waste_card is not None:
                if foundation.get_suit() == waste_card.get_suit():
                    if waste_card.get_value() == 1:
                        foundation.add_card(waste_card)
                        game.waste.remove_card()
                        moved = True
                        game.moves += 1
                        time.sleep(0.2)
                        break
                    else:
                        foundation_card = foundation.get_top_card()
                        if foundation_card is not None:
                            if foundation_card.get_value() + 1 == waste_card.get_value():
                                foundation.add_card(waste_card)
                                game.waste.remove_card()
                                moved = True
                                game.moves += 1
                                time.sleep(0.2)
                                break
        return moved

    def bottom_card_table(self, game, card, table, moved): # Función que comprueba si la carta de la parte inferior de una tabla se puede colocar en otra tabla automáticamente
        
        prev_card = table.prev_card()
        for dest_table in game.tables:
            if dest_table != table:
                dest_card = dest_table.bottom_card()
                if dest_card is not None and dest_card.get_color() != card.get_color() and dest_card.get_value() - 1 == card.get_value():
                    if prev_card == card or not prev_card.is_front_showing():
                        dest_table.add_new_card(card)
                        table.remove_card()
                        moved = True
                        game.moves += 1
                        time.sleep(0.2)
                        break
                else:
                    if card.get_value() == 13 and prev_card != card and dest_card is None:
                        dest_table.add_new_card(card)
                        table.remove_card()
                        moved = True
                        game.moves += 1
                        time.sleep(0.2)
                        break      
        return moved

    def waste_card_table(self, game, card, moved): # Función que comprueba si la carta de descarte se puede colocar en una tabla automáticamente
        for dest_table in game.tables:
            dest_card = dest_table.bottom_card()
            if dest_card is not None:
                if dest_card.get_color() != card.get_color():
                    if dest_card.get_value() - 1 == card.get_value():
                        dest_table.add_new_card(card)
                        game.waste.remove_card()
                        moved = True
                        game.moves += 1
                        time.sleep(0.2)
                        break
            else:
                if card.get_value() == 13:
                    dest_table.add_new_card(card)
                    game.waste.remove_card()
                    moved = True
                    game.moves += 1
                    time.sleep(0.2)
                    break
        return moved

    def upper_card_table(self, game, cards, table, moved): # Función que comprueba si la carta visible de la parte superior de una tabla se puede colocar en otra tabla automáticamente
        for dest_table in game.tables:
            if dest_table != table:
                dest_card = dest_table.bottom_card()
                if dest_card is None:
                    if cards[0][0].get_value() == 13:
                        if cards[1] == True:
                            return
                        else:
                            dest_table.add_cards(cards[0])
                            for _ in cards[0]:
                                table.remove_card()
                            cards[0].clear()
                            moved = True
                            game.moves += 1
                            time.sleep(0.2)
                            break

                if dest_card is not None:
                    if dest_card.get_color() != cards[0][0].get_color():
                        if dest_card.get_value() - 1 == cards[0][0].get_value():
                            dest_table.add_cards(cards[0])
                            for _ in cards[0]:
                                table.remove_card()
                            moved = True
                            game.moves += 1
                            time.sleep(0.2)
                            break
        return moved
    
    def foundation_to_table_and_table_to_table(self, game, card, table, moved): # Funciona
        
        prev_card = table.prev_card()
        if prev_card == card or not prev_card.is_front_showing():
            for dest_table in game.tables:
                dest_card = dest_table.bottom_card()
                if dest_card is not None and dest_card.get_value() - 2 == card.get_value() and dest_card.get_color() == card.get_color():
                    for foundation in game.foundations:
                        foundation_card = foundation.get_top_card()
                        if foundation_card is not None and foundation_card.get_value() == dest_card.get_value() - 1 and foundation_card.get_color() != dest_card.get_color():
                            foundation.remove_card()
                            table.remove_card()
                            dest_table.add_new_card(foundation_card)
                            dest_table.add_new_card(card)
                            moved = True
                            game.moves += 2
                            time.sleep(0.2)
                            print('foundation to table and table to table')
                            break
        return moved

    def foundation_to_table_x2_and_table_to_table(self, game, card, table, moved):
        
        prev_card = table.prev_card()
        if prev_card == card or not prev_card.is_front_showing():
            for dest_table1 in game.tables:
                dest_card1 = dest_table1.bottom_card()
                if dest_card1 is not None and dest_card1.get_value() - 2 == card.get_value() and dest_card1.get_color() == card.get_color():
                    for foundation in game.foundations:
                        foundation_card1 = foundation.get_top_card()
                        if foundation_card1 is not None and foundation_card1.get_value() == dest_card1.get_value() and foundation_card1.get_color() != dest_card1.get_color() and foundation_card1.get_value() != 1:
                            for dest_table2 in game.tables:
                                dest_card2 = dest_table2.bottom_card()
                                if dest_card2 is not None and dest_card2.get_value() - 1 == foundation_card1.get_value() and dest_card2.get_color() != foundation_card1.get_color():
                                    foundation.remove_card()
                                    table.remove_card()
                                    foundation_card2 = foundation.get_top_card()
                                    dest_table2.add_new_card(foundation_card1)
                                    dest_table1.add_new_card(foundation_card2)
                                    dest_table1.add_new_card(card)
                                    moved = True
                                    game.moves += 3
                                    time.sleep(0.2)
                                    print('foundation to table x2 and table to table')
                                    break
        return moved
    
    def prev_to_foundation(self, game, card, table, moved): # Funciona
        prev_card = table.prev_card()
        for dest_table in game.tables:
            dest_card = dest_table.bottom_card()
            if dest_card is not None and prev_card != card and prev_card.get_color() == dest_card.get_color() and prev_card.get_value() == dest_card.get_value():
                for foundation in game.foundations:
                    foundation_card = foundation.get_top_card()
                    if foundation_card is not None and foundation_card.get_value() + 1 == prev_card.get_value() and foundation_card.get_color() == prev_card.get_color():
                        table.remove_card()
                        dest_table.add_new_card(card)
                        table.remove_card()
                        foundation.add_card(prev_card)
                        moved = True
                        game.moves += 2
                        time.sleep(0.2)
                        print('se ejecuto prev to foundation')
                        break
        return moved
    
    def foundation_to_table_deck_to_table(self, game, waste_card, moved): # Funciona
        
        for foundation in game.foundations:
            foundation_card = foundation.get_top_card()
            
            if foundation_card is not None and foundation_card.get_value() - 1 == waste_card.get_value() and foundation_card.get_color() != waste_card.get_color():
                for dest_table in game.tables:
                    dest_card = dest_table.bottom_card()
                    if dest_card is not None and dest_card.get_value() - 2 == waste_card.get_value() and dest_card.get_color() == waste_card.get_color():
                        foundation.remove_card()
                        dest_table.add_new_card(foundation_card)
                        game.waste.remove_card()
                        dest_table.add_new_card(waste_card)
                        moved = True
                        game.moves += 2
                        time.sleep(0.2)
                        print('se ejecuto foundation to table deck to table')
                        break
        return moved
        