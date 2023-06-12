import time

class Waste:

    def __init__(self):
        self.waste_pile = []            # Pila de residuo NO visible  (Cartas que no estan en el tablero)
        self.show_pile = []             # Pila de residuo visible
        self.y = 68                     # Coordenadas de la iamgen de las cartas en el eje y.
        self.x = [150, 175, 200]        # Coordenadas de la imagen de las cartas en el eje x, desapiladas del mazo, 1ra, 2da, 3ra

    def get_waste_pile(self):           # Retorna la pila de residuo NO visible.
        return self.waste_pile

    def add_card(self, card):           # agrega una carta a la pila de residuo NO visible.
        card.set_coordinates(150, 68)    # Coordenadas de la pila de residuo NO visible.
        self.waste_pile.append(card)    
        self.set_cards()

    def remove_card(self):              # Remueve la última carta de la pila de residuo NO visible.
        if len(self.waste_pile) > 0:
            card = self.waste_pile.pop()
            time.sleep(0.5)
            return card

    def empty(self):                    # Vacía la pila de residuo NO visible esta vacía.
        self.waste_pile.clear()
        self.set_cards()
        
    def show_is_empty(self):
        return len(self.show_pile) == 0
        
    def get_top_card(self):             # Verifica si la pila de residuo esta vacía, si no lo esta, devuelve la última carta de la pila.
        if len(self.waste_pile) > 0:
            return self.waste_pile[len(self.waste_pile)-1]


    """
    Este método establece las coordenadas de las cartas de la pila de residuo visible.
    Primero verifica si la pila de residuo NO visible tiene más de 3 cartas. Si esta condición se cumple, 
    se le asignan las úiltimas 3 cartas de la pila a la pila de residuo visible. Si la pila de residuo visible tiene 3 cartas o menos, 
    se asigna toda la pila a esta variable. Luego se itera sobre cada carta en *show_pile* y se llama al método *set_coordinates* 
    para establecer las coordenadas de cada carta. Si ya hay 3 cartas mostradas en *show_pile*, 
    la primer carta de la pila se oculta, la segunda pasa a ser la primera, la tercera a ser segunda,
    y la nueva carta mostrada pasa a ser la tercera.
    """
    def set_cards(self):
        if len(self.waste_pile) > 3:
            self.show_pile = self.waste_pile[len(self.waste_pile) - 3 : len(self.waste_pile)]
        else:
            self.show_pile = self.waste_pile
        for card_iterator in range(len(self.show_pile)):
            self.show_pile[card_iterator].set_coordinates(self.x[card_iterator], self.y)

    def get_show_waste_pile(self):      # Retorna la pila de residuo visible.
        return self.show_pile