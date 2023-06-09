import time
class Foundation:

    def __init__(self, x, suit):
        
        self.Foundation_pile = []   # Lista con las cartas que se almacenan en la Foundation
        self.x = x                  # Coordenada x del Foundation
        self.y = 68                 # Coordenada y del Foundation
        self.suit = suit            # Palo del Foundation

    def get_Foundation(self):       # Retorna la lista que almacena el Foundation
        return self.Foundation_pile

    def add_card(self, card):       # Agrega una carta a la lista y transporta la carta a la posición de dicho Foundation.
        self.Foundation_pile.append(card)
        card.set_coordinates(self.x, self.y)

    def remove_card(self):          # Elimina una carta de la lista
        if len(self.Foundation_pile) > 0:
            card = self.Foundation_pile.pop()
            time.sleep(0.5)
            return card

    """
    Este método devuelve la carta superior de la pila *Foundation_pile*.
    Primero verifica si la pila tiene al menos una carta. Si esta condición se cumple,
    devuelve la última carta de la pila. Si la pila esta vacía, el método no devuelve nada.   
    """
    def get_top_card(self):
        if len(self.Foundation_pile) > 0:
            return self.Foundation_pile[len(self.Foundation_pile)-1]

    def get_suit(self):             # Retorna el palo del Foundation
        return self.suit

    """
    Este método establece las coordenadas de la carta superior de la pila *Foundation_pile*
    Primero accede a la última carta de la pila, luego utiliza el método *set_coordinates(x, y)*,
    con lo que establece la posición de la carta en la pantalla.    
    """
    def set_cards(self):
        self.Foundation_pile[len(self.Foundation_pile)-1].set_coordinates(self.x, self.y)
        
        
    def is_complete(self):
        if len(self.Foundation_pile) == 13:
            return all(card.rank == str(i) for i, card in enumerate(self.Foundation_pile, start=1))
        else:
            return False