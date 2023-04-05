import pygame
from Card import Card
import random

class Deck:

    def __init__(self):
        
        # La función pygame.image.load() establece una imagen en la ventana, en este caso las cartas del mazo tienen todas el mismo revés.
        self.back_image = pygame.image.load("D:/My Drive/Universidad/CUARTO AÑO/Modelos y Simulación/Método de Montecarlo/Montecarlo/Solitario-Montecarlo/assets/PlayingCards/back.png")
        
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
        estas se encuentran en la carpeta assets/PlayingCards y se nombran   value_of_palo.png   Ej: 4_of_hearts.png
        """
        for suit in ["hearts", "spades", "diamonds", "clubs"]:
            for value in range(1,14):
                image = "D:/My Drive/Universidad/CUARTO AÑO/Modelos y Simulación/Método de Montecarlo/Montecarlo/Solitario-Montecarlo/assets/PlayingCards/"+str(value)+"_of_"+suit+".png"
                self.deck.append(Card(suit, value, image, self.back_image))
                
    def get_deck(self):             # función que retorna el mazo.
        return self.deck

    def shuffle(self):              # función que mezcla el mazo
        random.shuffle(self.deck)

    def add_cards(self, cards):     # función que agrega una carta al mazo.     (Sirve a la hora de rellenar de nuevo el mazo, luego de haber sacado todas las cartas)
        self.deck = cards

    def remove_card(self):          # función que elimina una carta del mazo.   (Sirve para ir sacando una carta a la vez del mazo y mostrarla en la pila visible)
        return self.deck.pop()