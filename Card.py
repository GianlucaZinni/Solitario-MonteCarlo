import pygame

class Card(pygame.sprite.Sprite):
    def __init__(self, suit, value, image, back_image):
        pygame.sprite.Sprite.__init__(self)
        self.suit = suit
        self.value = value
        self.back_image = back_image
        self.front_image = pygame.image.load(image)
        self.front_image = pygame.transform.scale(self.front_image, (
        int(self.front_image.get_rect().size[0] * .20), int(self.front_image.get_rect().size[1] * .20)))
        self.image = self.front_image
        self.rect = self.image.get_rect()

    def get_suit(self):
        return self.suit

    def get_value(self):
        return self.value

    def set_coordinates(self, x, y):
        self.rect = (x,y)

    def get_coordinates(self):
        return self.rect

    def flip(self):
        if self.image == self.front_image:
            self.image = self.back_image
        else:
            self.image = self.front_image

    def set_front_showing(self):
        self.image = self.front_image

    def is_front_showing(self):
        if self.image == self.front_image:
            return True
        return False

    def get_color(self):
        if self.suit=="spades" or self.suit=="clubs":
            return "black"
        else:
            return "red"