import pygame
from Card import Card
import random

class Deck:

    def __init__(self):
        self.back_image = pygame.image.load("D:/My Drive/Universidad/CUARTO AÑO/Modelos y Simulación/Método de Montecarlo/Montecarlo/Solitario-Montecarlo/assets/PlayingCards/back.png")
        self.back_image = pygame.transform.scale(self.back_image, (
            int(self.back_image.get_rect().size[0] * .20), int(self.back_image.get_rect().size[1] * .20)))
        self.deck = []
        for suit in ["hearts", "spades", "diamonds", "clubs"]:
            for value in range(1,14):
                image = "D:/My Drive/Universidad/CUARTO AÑO/Modelos y Simulación/Método de Montecarlo/Montecarlo/Solitario-Montecarlo/assets/PlayingCards/"+str(value)+"_of_"+suit+".png"
                self.deck.append(Card(suit,value,image, self.back_image))

    def get_deck(self):
        return self.deck

    def shuffle(self):
        random.shuffle(self.deck)

    def add_cards(self, cards):
        self.deck = cards

    def remove_card(self):
        return self.deck.pop()