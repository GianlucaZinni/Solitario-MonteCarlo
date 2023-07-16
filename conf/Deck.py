import pygame, time, random
from conf.Card import Card

class Deck:

    def __init__(self):
        
        # La función pygame.image.load() establece una imagen en la ventana, en este caso las cartas del mazo tienen todas el mismo revés.
        self.back_image = pygame.image.load("static/assets/layout/templates/back.png")
        
        """
        La función pygame.transform.scale toma la imagen y una tupla que representa el 
        nuevo tamaño en pixeles y devuelve una imagen con el tamaño especificado.
        En este caso modifica el tamaño de la imagen original un 20% en ancho y alto. 
        """
        self.back_image = pygame.transform.scale(self.back_image, (int(self.back_image.get_rect().size[0] * .20), int(self.back_image.get_rect().size[1] * .20)))
        
        self.deck = []              # Creamos la lista que contendrá el mazo de cartas.
        
        """
        Bucle FOR que agrega 13 cartas del 1 al 13 para cada uno de los 4 palos, 
        luego con ayuda de una concatenación, agregamos la imagen correspondiente a cada valor de la carta,
        estas se encuentran en la carpeta static/assets/layout/templates/ y se nombran   value_of_palo.png   Ej: 4_of_hearts.png
        """
        for suit in ["hearts", "spades", "diamonds", "clubs"]:
            for value in range(1,14):
                image = "static/assets/layout/templates/"+str(value)+"_of_"+suit+".png"
                self.deck.append(Card(suit, value, image, self.back_image))
                
    def get_deck(self):             # función que retorna el mazo.
        return self.deck
    
    def set_deck(self, deck):
        self.deck = deck
        return self.deck

    def shuffle(self):              # función que mezcla el mazo
        random.shuffle(self.deck)
        return self.deck

    def add_cards(self, cards):     # función que agrega una carta al mazo.     (Sirve a la hora de rellenar de nuevo el mazo, luego de haber sacado todas las cartas)
        self.deck = cards

        # función que elimina una carta del mazo.   (Sirve para ir sacando una carta a la vez del mazo y mostrarla en la pila visible)
    def remove_card(self):
        if len(self.deck) <= 0:
            print("The deck is empty")
        else:
            card = self.deck.pop()
            return card
    
    def reset_deck(self):
        self.deck = self.insert_all_cards[:]
        
    def insert_all_cards(self):
        all_cards = []
        for card in self.deck:
            all_cards.append((card.get_suit(), card.get_value()))
        return all_cards