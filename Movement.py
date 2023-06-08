class Moves:
    def __init__(self):
        
        self.mouse_x = 0
        self.mouse_y = 0
        
    def update_mouse_position(self, mouse_x, mouse_y):
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
    
    def clicked_new_card(self, game):
        
        mouse_x = self.mouse_x
        mouse_y = self.mouse_y
        
        if mouse_x > 9 and mouse_x < 106 and mouse_y > 14 and mouse_y < 155:
            if len(game.deck.get_deck()) <= 0:
                game.deck.add_cards(list(reversed(game.waste.get_waste_pile().copy())))
                game.waste.empty()
                game.shuffle_sound.play()
            else:
                game.moves += 1
                game.waste.add_card(game.deck.remove_card())
                game.place_sound.play()

    def check_holding_card(self, game):
        
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

    def place_card(self, game):
        
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
                        for card in game.holding_cards:
                            game.holding_card_group.remove_card()
                            game.place_sound.play()
                            game.moves += 1
                        return
                else:
                    if game.holding_cards[0].get_value() == 13:
                        table.add_cards(game.holding_cards)
                        for card in game.holding_cards:
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
                        for card in game.holding_cards:
                            game.holding_card_group.remove_card()
                            game.place_sound.play()
                            game.moves += 1
                        return
                else:
                    if game.holding_cards[0].get_value() == 13:
                        table.add_cards(game.holding_cards)
                        for card in game.holding_cards:
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
