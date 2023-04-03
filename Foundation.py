import pygame

# 
class Foundation:

    def __init__(self,x, suit):
        self.Foundation_pile = []
        self.x = x
        self.y = 68
        self.suit = suit

    def get_Foundation(self):
        return self.Foundation_pile

    def add_card(self, card):
        self.Foundation_pile.append(card)
        card.set_coordinates(self.x, self.y)

    def remove_card(self):
        self.Foundation_pile.pop()

    def get_top_card(self):
        if len(self.Foundation_pile)>0:
            return self.Foundation_pile[len(self.Foundation_pile)-1]

    def get_suit(self):
        return self.suit

    def set_cards(self):
        self.Foundation_pile[len(self.Foundation_pile)-1].set_coordinates(self.x, self.y)