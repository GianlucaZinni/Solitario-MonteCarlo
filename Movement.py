import pygame


class Movement:
    def __init__(self, mouse_x, mouse_y):
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y

        self.place_sound = pygame.mixer.Sound("assets/flip.wav")
        self.shuffle_sound = pygame.mixer.Sound("assets/shuffle.wav")
        self.shuffle_sound.play()

    def clicked_new_card(self, deck, waste, moves):
        mouse_x = self.mouse_x
        mouse_y = self.mouse_y

        if mouse_x > 9 and mouse_x < 106 and mouse_y > 14 and mouse_y < 155:
            if len(deck.get_deck()) <= 0:
                deck.add_cards(list(reversed(waste.get_waste_pile().copy())))
                waste.empty()
                self.shuffle_sound.play()

            else:
                moves += 1
                waste.add_card(deck.remove_card())
                self.place_sound.play()

        return waste, deck, moves

    def check_holding_card(
        self, mouse_cords, tables, foundations, waste, holding_cards, holding_card_group
    ):
        mouse_x = self.mouse_x
        mouse_y = self.mouse_y

        possible_cards = []
        mouse_cords = (mouse_x, mouse_y)

        for table in tables:
            for table_card in table.get_table():
                if table_card.is_front_showing():
                    possible_cards.append((table_card, table))

        for foundation in foundations:
            foundation_card = foundation.get_top_card()
            if foundation_card != None:
                possible_cards.append((foundation_card, foundation))

        waste_card = waste.get_top_card()
        if waste_card != None:
            possible_cards.append((waste_card, waste))

        for card in possible_cards:
            card_x = card[0].get_coordinates()[0]
            card_y = card[0].get_coordinates()[1]
            if (
                mouse_x > card_x
                and mouse_x < card_x + 100
                and mouse_y > card_y
                and mouse_y < card_y + 145
            ):
                holding_card_group = card[1]
                if holding_card_group in tables:
                    holding_cards = holding_card_group.get_cards_below(card[0])
                else:
                    holding_cards = [card[0]]

        return (
            tables,
            foundations,
            waste,
            holding_cards,
            holding_card_group,
            mouse_cords,
        )

    def place_card(
        self, mouse_cords, foundations, tables, moves, holding_cards, holding_card_group
    ):
        mouse_x = self.mouse_x
        mouse_y = self.mouse_y

        if mouse_cords == (mouse_x, mouse_y):
            if len(holding_cards) == 1:
                for foundation in foundations:
                    if foundation.get_suit() == holding_cards[0].get_suit():
                        foundation_card = foundation.get_top_card()
                        if foundation_card != None:
                            if (
                                foundation_card.get_value() + 1
                                == holding_cards[0].get_value()
                            ):
                                foundation.add_card(holding_cards[0])
                                holding_card_group.remove_card()
                                self.place_sound.play()
                                moves += 1
                                return foundations, moves, holding_card_group
                        else:
                            if holding_cards[0].get_value() == 1:
                                foundation.add_card(holding_cards[0])
                                holding_card_group.remove_card()
                                self.place_sound.play()
                                moves += 1
                                return foundations, moves, holding_card_group

            for table in tables:
                bottom_card = table.bottom_card()
                if bottom_card != None:
                    value = bottom_card.get_value()
                    if (
                        bottom_card.get_color() != holding_cards[0].get_color()
                        and value - 1 == holding_cards[0].get_value()
                    ):
                        table.add_cards(holding_cards)
                        for card in holding_cards:
                            holding_card_group.remove_card()
                            self.place_sound.play()
                            moves += 1
                        return table, moves, holding_card_group
                else:
                    if holding_cards[0].get_value() == 13:
                        table.add_cards(holding_cards)
                        for card in holding_cards:
                            holding_card_group.remove_card()
                        self.place_sound.play()
                        moves += 1
                        return tables, moves, holding_card_group

        else:
            positions = [950, 825, 710, 590, 470, 355, 242, 120]
            count = 0

            for pos in positions:
                if mouse_x > pos:
                    break
                count += 1

            if count > 0:
                table = tables[7 - count]
                bottom_card = table.bottom_card()

                if bottom_card != None:
                    value = bottom_card.get_value()
                    if (
                        bottom_card.get_color() != holding_cards[0].get_color()
                        and value - 1 == holding_cards[0].get_value()
                    ):
                        table.add_cards(holding_cards)
                        for card in holding_cards:
                            holding_card_group.remove_card()
                            self.place_sound.play()
                            moves += 1
                        return tables, moves, holding_card_group
                else:
                    if holding_cards[0].get_value() == 13:
                        table.add_cards(holding_cards)
                        for card in holding_cards:
                            holding_card_group.remove_card()
                        self.place_sound.play()
                        moves += 1
                        return tables, moves, holding_card_group
            else:
                for foundation in foundations:
                    if foundation.get_suit() == holding_cards[0].get_suit():
                        foundation_card = foundation.get_top_card()

                        if foundation_card != None:
                            if (
                                foundation_card.get_value() + 1
                                == holding_cards[0].get_value()
                            ):
                                foundation.add_card(holding_cards[0])
                                holding_card_group.remove_card()
                                self.place_sound.play()
                                moves += 1
                                return foundations, moves, holding_card_group
                        else:
                            if holding_cards[0].get_value() == 1:
                                foundation.add_card(holding_cards[0])
                                holding_card_group.remove_card()
                                self.place_sound.play()
                                moves += 1
                                return foundations, moves, holding_card_group

        holding_card_group.set_cards()
        return holding_card_group

    def card_follow_mouse(self, mouse_x, mouse_y):
        if self.holding_cards != []:
            x = mouse_x - 50
            y = mouse_y - 50
            pos = 0

            for card in self.holding_cards:
                card.set_coordinates(x, y + (pos * 40))
                pygame.sprite.GroupSingle(card).draw(self.screen)
                pos += 1
