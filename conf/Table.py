"""
La clase Table tiene el constructor de la clase que recibe
"""
import time
class Table:

    def __init__(self, x, deck, card_amount):
        
        """"
        Pilas de cartas de la tabla, van a ser finalemnte 7 pilas.
        Las pilas tendrán un *card_mount*, es decir, una acumulación de cartas, que seguiran la siguiente forma:
        1ra Pila, una carta, carta de frente.
        2da Pila, dos cartas, primera carta de reverso, última carta de frente.
        3ra Pila, tres cartas, todas las cartas de reverso, menos la última carta, que estará de frente.
        4ta Pila.. 5ta Pila.. 6ta Pila.. 7ta Pila..
        """
        self.table_cards = []               # Lista vacía que va a almacenar las cartas de la pila.            
        self.x = x                          # Coordenada en el eje x donde se posicionara el primer elemento de cada pila, la cual varía por 25px entre pilas.
        self.y = 236                        # Coordenada en el eje y donde se posicionaran las pilas.
        
        """
        El constructor también recibe:
        *deck*: que es el objeto que contiene las cartas.
        *card_amount* que es el número de cartas que va a tener la pila.
        
        
        El bucle FOR recorre *card_amount* veces, es decir, la cantidad de cartas que tenga la pila instanciada
        para extraer una carta del objeto *deck* y luego añade las coordenadas a la carta y la añade a la lista *table_cards*.
        Luego voltea la carta con la función flip(), y en el caso de ser la útima carta añadida, la voltea de nuevo.
        """
        for number in range(card_amount):
            card = deck.get_deck().pop()
            card.set_coordinates(self.x, self.y+(len(self.table_cards)*40))
            self.table_cards.append(card)
            card.flip()
            if number == card_amount-1:
                card.flip()
                
                
    """
    Recibe como parámetro una carta y la añade a la pila, 
    seteando sus coordenadas visualmente y agregandola a la pila *table_cards*
    """
    def add_new_card(self, card):
        card.set_coordinates(self.x, self.y + (len(self.table_cards) * 40))
        self.table_cards.append(card)

    """
    Recibe como parámetro una lista de cartas y la añade a la pila, 
    seteando sus coordenadas visualmente y agregandola a la pila *table_cards*
    Básicamente, lo mismo que la otra función, pero con un grupo de cartas.
    """
    def add_cards(self, cards):
        for card in cards:
            card.set_coordinates(self.x, self.y + (len(self.table_cards) * 40))
            self.table_cards.append(card)

    def get_table(self):                    # Retorna la pila de cartas de la tabla.
        return self.table_cards

    def bottom_card(self):                  # Verifica si la pila de cartas de la tabla esta vacía, si no lo está, devuelve la última carta de la pila.
        if len(self.table_cards)>0:
            return self.table_cards[len(self.table_cards)-1]
        
    def prev_card(self):                  # Verifica si la pila de cartas de la tabla esta vacía, si no lo está, devuelve la anteúltima carta de la pila.
        if len(self.table_cards) > 0:
            return self.table_cards[len(self.table_cards)-2]
        
    def obtain_next_card(self, card_num):
        try:
            if len(self.table_cards) > 0:
                return self.table_cards[card_num-1]
        except:
            print("list index out of range")

    def get_x(self):                        # Retorna la coordenada en el eje x.
        return self.x

    def get_y(self):                        # Retorna la coordenada en el eje y.
        return self.y

    """
    Elimina y devuelve la última carta de la pila *table_cards*. Si todavía no hay cartas
    en la lista, muestra la carta anterior como cara visible.
    """
    def remove_card(self):
        card = self.table_cards.pop()
        time.sleep(0.5)
        if len(self.table_cards) > 0:
            self.table_cards[len(self.table_cards)-1].set_front_showing()
        return card
    
    """
    Devuelve una lista de cartas que están debajo de la carta pasada como parámetro.
    """
    def get_cards_below(self, card):
        fill = False
        cards_below = []
        for table_card in self.table_cards:
            if table_card == card:
                fill = True
            if fill:
                cards_below.append(table_card)
        return cards_below
    
    def get_showing_cards(self, table_cards):
        cards = []
        for card in table_cards:
            if card.is_front_showing():
                cards.append(card)
        if cards == table_cards: 
            return [cards, True]
        else:
            return [cards, False]

    """
    Establece las coordenadas de todas las cartas de la pila.
    Primero establece la variable posición en 0 y luego establece las coordenadas
    de cada carta en la pila sumando a la coordenada en el eje,e la posición anterior * 40.
    """
    def set_cards(self):
        pos = 0
        for card in self.table_cards:
            card.set_coordinates(self.x, self.y + (pos * 40))
            pos += 1
            
