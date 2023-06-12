import pygame, time

class BasicMoves:
    def __init__(self):
        
        self.mouse_x = 0
        self.mouse_y = 0
        
    def update_mouse_position(self, mouse_x, mouse_y):  # Actualiza la posición del mouse
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        
    """Función que permite que las cartas seleccionadas por el usuario sigan al cursor mientras se arrastran por la pantalla."""
    def card_follow_mouse(self, game): # Función que genera el efecto de arrastrar una carta
        
        mouse_x = self.mouse_x
        mouse_y = self.mouse_y
        """Se verifica si se están sosteniedno cartas, es decir, si la variable global *holding_cards* no está vacía."""
        if game.holding_cards != []:
            """Se define la posición de la carta que sigue al cursor:
            La variable *x* se establece como el valor de la posición horizontal del cursor menos 50 (mitad de la anchura de la carta).
            La variable *y* se establece como el valor de la posición vertical del cursor menos 50 (mitad de la altura de la carta).
            La variable *pos* se establece en 0 y se utiliza para calcular la posición vertical de cada carta que sigue el cursor."""
            x = mouse_x - 50
            y = mouse_y - 50
            pos = 0
            
            """Se itera a través de las cartas en *self.holding_cards*, se les asigna una nueva coordenada vertical que se basa en 
            la posición *y* y se incrementa por 40 veces la variable *pos*."""
            for card in game.holding_cards:
                card.set_coordinates(x, y + (pos * 40))
                """Finalmente, cada carta se dibuja en pantalla usando la función *draw()* de *pygame.sprite.GroupSingle()*"""
                pygame.sprite.GroupSingle(card).draw(game.screen)
                """La variable pos se incrementa en 1 en cada iteración para que las cartas queden apiladas visualmente."""
                pos += 1

    """Función que comprueba si el usuario hizo click en el mazo de residuo no visible.
    Si lo ha hecho, se comprueba si el mazo está vacío. Si lo está, las cartas de la pila de residuo visible se devuelven a la pila de residuo no visible y se barajan. 
    Si no lo está, se añade una carta a la pila de residuo visible."""
    def clicked_new_card(self, game): # Agrega una carta de la pila no visible a la pila visible
        """Verifica SI las coordenadas del cursor están dentro de un rectángulo que se supone
        que contiene la carta del mazo."""
        mouse_x = self.mouse_x
        mouse_y = self.mouse_y
        
        if mouse_x > 25 and mouse_x < 125 and mouse_y > 68 and mouse_y < 210:
            """ (IF)
            Se verifica SI el mazo de cartas está vacío. Sí es así, la función agrega las cartas
            de la pila de residuo no visible (waste) al mazo de cartas y la pila de residuos se vacía.
            
                (ELSE)
            Se ejecuta SI el mazo de cartas NO está vacío,
            Se incrementa la variable *moves* y agrega la carta superior del mazo (Deck) a la
            pila de residuos no visible. Luego se reproduce el sonido de colocación *place_sound*."""
            if len(game.deck.get_deck()) <= 0:
                game.deck.add_cards(list(reversed(game.waste.get_waste_pile().copy())))
                game.waste.empty()
            else:
                game.moves += 1
                game.waste.add_card(game.deck.remove_card())
                game.place_sound.play()

    """Comprueba si el usuario esta sosteniendo alguna carta. Si es así, se actualiza la posición de la carta para que coincida con la posición del cursor.
    Si el usuario no está sosteniendo ninguna carta, se comprueba si el cursor está sobre una carta que se pueda mover. 
    Si es así, se añade esa carta y todas las cartas debajo de ella a la lista *holding_cards* y se establece *holding_card_group* en el grupo de cartas correspondiente."""
    def check_holding_card(self, game): # Verifica si se está sosteniendo una carta

        mouse_x = self.mouse_x
        mouse_y = self.mouse_y
        
        """Se declaran las variables globales *holding_card_group* *holding_cards* *mouse_cords*,
        Se declara la lista vacía *possible_cards*,
        Se guardan las coordenadas del cursor en la variable *mouse_cards*."""
        possible_cards = []
        game.mouse_cords = (mouse_x, mouse_y)
        
        """Se itera sobre la lista de objetos *tables*, y por cada objeto se itera sobre las cartas en la mesa (almacenadas en *table.get_table()*). 
        Si la carta está en la posición de frente, se agrega a la lista possible_cards como una tupla con la carta y la mesa donde se encuentra."""
        for table in game.tables:
            for table_card in table.get_table():
                if table_card.is_front_showing():
                    possible_cards.append((table_card, table))
                    
        """Se itera sobre la lista de objetos *foundations*, y por cada objeto se obtiene la carta en la cima de la pila (almacenada en *foundation.get_top_card()*). 
        Si hay una carta en la cima, se agrega a la lista *possible_cards* como una tupla con la carta y la foundation donde se encuentra."""
        for foundation in game.foundations:
            foundation_card = foundation.get_top_card()
            if foundation_card is not None:
                possible_cards.append((foundation_card, foundation))

        """Se obtiene la carta en la cima de la pila de descarte (almacenada en *waste.get_top_card()*), 
        si hay una carta en la cima, se agrega a la lista *possible_cards* como una tupla con la carta y la pila de descarte."""
        waste_card = game.waste.get_top_card()
        if waste_card is not None:
            possible_cards.append((waste_card, game.waste))

        """Se itera sobre la lista *possible_cards*, y por cada carta se obtienen sus coordenadas con *card_x* y *card_y*. 
        Luego, se verifica si las coordenadas del cursor se encuentran sobre la carta y si es así, 
        se establece la variable global *holding_card_group* a la table/foundtaion/deck de descarte de la carta. 
        Si la table/foundation es tables, entonces se obtienen las cartas debajo de la carta seleccionada y se almacenan en la variable global *holding_cards*. 
        Si la table/foundation es otra cosa, se establece la variable global *holding_cards* como una lista con la carta seleccionada."""
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

    def check_waste_card(self, game, moved):
        """Obtiene la carta visible del mazo VISIBLE."""
        waste_card = game.waste.get_top_card()
        if waste_card is not None:
            """Función que revisa si puede mover la carta seleccionada a algun foundation."""
            moved = self.waste_card_foundation(game, waste_card, moved)
            if not moved:
                """Función que revisa si puede mover la carta seleccionada a alguna table."""
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
                        break
        return moved
        