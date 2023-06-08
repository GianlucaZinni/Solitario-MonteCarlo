import pygame

class Card(pygame.sprite.Sprite):
    def __init__(self, suit, value, image, back_image):
        pygame.sprite.Sprite.__init__(self)
        
        self.suit = suit # Se determina el palo de la carta.
        self.value = value # Se determina el valor de la carta.
        self.back_image = back_image # Se determina la imagen del revés de la carta.
        
        """
        Primero se carga la imagen en la variable *front_image* con la función pygame.image.load()
        Luego se cambvia el tamaño de la imagen con la función pygame.transform.scale(), que toma la imagen y 
        una tupla que representa el nuevo tamaño en pixeles y  devuelve una imagen con el tamaño especificado.
        Después se le asigna la imagen escalada a la variable *image* y se obtiene su rectangulo delimitador utilizando el método get_rect()
        Este rectangulo se utiliza para determinar la posición y el tamaño de la imagen en pantalla.
        """
        self.front_image = pygame.image.load(image)
        self.front_image = pygame.transform.scale(self.front_image, (int(self.front_image.get_rect().size[0] * .20), int(self.front_image.get_rect().size[1] * .20)))
        self.image = self.front_image
        self.rect = self.image.get_rect()

    def get_suit(self):                 # Retorna el palo de la carta.
        return self.suit

    def get_value(self):                # Retorna el valor de la carta.
        return self.value

    def set_coordinates(self, x, y):    # Setea las coordenadas de la carta.
        self.rect = (x,y)
        
    def get_coordinates(self):          # Retorna las coordenadas de la carta.
        return self.rect

    def flip(self):                     # Da vuelta la carta (Cambia visualmente, la imagen del revés por la imagen del frente)
        if self.image == self.front_image:
            self.image = self.back_image
        else:
            self.image = self.front_image

    def set_front_showing(self):        # Muestra el frente de una carta.
        self.image = self.front_image

    def is_front_showing(self):         # Retorna true si la carta esta de frente, o false si esta del revés.
        if self.image == self.front_image:
            return True
        return False
    
    def is_last_showing(self, cards):
        new_cards = []
        for card in cards:
            if not card.is_front_showing():
                continue
            else:
                new_cards.append(card)
        return new_cards

    def get_color(self):                # Retorna el color del palo. (Para averiguar si es posible su colocación por debajo de otra carta que tenga distinto color)
        if self.suit=="spades" or self.suit=="clubs":
            return "black"
        else:
            return "red"