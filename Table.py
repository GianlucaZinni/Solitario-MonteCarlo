import pygame

class Table:

    def __init__(self, x, deck, card_amount):
        self.table_cards = []
        self.x = x
        self.y = 236
        for number in range(card_amount):
            card = deck.get_deck().pop()
            card.set_coordinates(self.x, self.y+(len(self.table_cards)*40))
            self.table_cards.append(card)
            card.flip()
            if number == card_amount-1:
                card.flip()

    def add_new_card(self, card):
        card.set_coordinates(self.x, self.y + (len(self.table_cards) * 40))
        self.table_cards.append(card)

    def add_cards(self, cards):
        for card in cards:
            card.set_coordinates(self.x, self.y + (len(self.table_cards) * 40))
            self.table_cards.append(card)

    def get_table(self):
        return self.table_cards

    def bottom_card(self):
        if len(self.table_cards)>0:
            return self.table_cards[len(self.table_cards)-1]

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def remove_card(self):
        card = self.table_cards.pop()
        if len(self.table_cards)>0:
            self.table_cards[len(self.table_cards)-1].set_front_showing()
        return card

    def get_cards_below(self,card):
        fill = False
        cards_below = []
        for table_card in self.table_cards:
            if table_card == card:
                fill = True
            if fill:
                cards_below.append(table_card)
        return cards_below

    def set_cards(self):
        pos = 0
        for card in self.table_cards:
            card.set_coordinates(self.x, self.y + (pos * 40))
            pos += 1