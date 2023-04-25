import pygame
from Deck import Deck
from Waste import Waste
from Foundation import Foundation
from Table import Table
from pygame.locals import RESIZABLE
from tkinter import messagebox
import time


# Se inicializa la biblioteca Pygame, permitiendo utilizar sus funciones y métodos.
pygame.init()

# Luego se define el tamaño de la ventana de juego. Primero el eje X y luego el eje Y.
window_size = (900, 885)

"""Se utiliza la función *pygame.display.set_mode()* para crear la ventana con el tamaño definido."""
screen = pygame.display.set_mode(window_size, RESIZABLE)

"""Luego se utiliza la función *pygame.display.set_caption()* para establecer el título de la ventana."""
pygame.display.set_caption("Solitario")

"""Se instancia la variable booleana *game_is_running* que se utilizará para mantener encendido el juego."""
game_is_running = True

"""Finalmente se guarda en la variable backgroundImage se utiliza la función *pygame.image.load()* para cargar la imagen del fondo del juego."""
backgroundImage = pygame.image.load("assets/backgroundd.jpg")

"""Link de donde obtuvimos los gráficos de las cartas utilizadas.
http://byronknoll.blogspot.com/2011/03/vector-playing-cards.html"""

# Se crea la instancia del objeto *Deck()*
deck = Deck()
# Se utiliza la función que mezcla el mazo.
deck.shuffle()

# Se crea la instancia del objeto *Waste()*
waste = Waste()

clock = pygame.time.Clock()

# Se declaran las variables globales utilizadas por el juego.
holding_cards = []         # Lista vacía que se utilizará para almacenar cartas que el usuario esta sosteniendo.
holding_card_group = None  # Variable establecida en None que luego se actualizará para indicar qué grupo de cartas esta sosteniendo el usuario.
mouse_cords = ()           # Tupla vacía que se actualizará cada vez que el usuario mueva el raton.
moves = 0                  # Contador de movimientos.
score = 0                  # Contador de puntos.
frame = 0                  # Contador de .
timer = 0                  # Contador de tiempo.

"""Definen los efectos de sonido que se reproducen en el juego.
La función *pygame.mixer.sound()* se utiliza para cargar el archivo de sonido en la variable correspondiente.
Luego se reproduce el sonido al barajar als cartas utiliando la función *play()*"""

place_sound = pygame.mixer.Sound('assets/flip.wav')
shuffle_sound = pygame.mixer.Sound('assets/shuffle.wav')
shuffle_sound.play()

"""Función que comprueba si el usuario hizo click en el mazo de residuo no visible.
Si lo ha hecho, se comprueba si el mazo está vacío. Si lo está, las cartas de la pila de residuo visible se devuelven a la pila de residuo no visible y se barajan. 
Si no lo está, se añade una carta a la pila de residuo visible."""
def clicked_new_card(mouse_x, mouse_y):
    
    """Se declara la variable global *moves*."""
    global moves
    
    """Verifica SI las coordenadas del cursor están dentro de un rectángulo que se supone
    que contiene la carta del mazo."""
    if mouse_x > 9 and mouse_x < 106 and mouse_y > 14 and mouse_y < 155:
        """ (IF)
        Se verifica SI el mazo de cartas está vacío. Sí es así, la función agrega las cartas
        de la pila de residuo no visible (waste) al mazo de cartas y la pila de residuos se vacía.
        
            (ELSE)
        Se ejecuta SI el mazo de cartas NO está vacío,
        Se incrementa la variable *moves* y agrega la carta superior del mazo (Deck) a la
        pila de residuos no visible. Luego se reproduce el sonido de colocación *place_sound*."""
        if len(deck.get_deck()) <= 0:
            deck.add_cards(list(reversed(waste.get_waste_pile().copy())))
            waste.empty()
            shuffle_sound.play()
        else:
            moves += 1
            waste.add_card(deck.remove_card())
            place_sound.play()

"""Comprueba si el usuario esta sosteniendo alguna carta. Si es así, se actualiza la posición de la carta para que coincida con la posición del cursor.
Si el usuario no está sosteniendo ninguna carta, se comprueba si el cursor está sobre una carta que se pueda mover. 
Si es así, se añade esa carta y todas las cartas debajo de ella a la lista *holding_cards* y se establece *holding_card_group* en el grupo de cartas correspondiente."""
def check_holding_card(mouse_x, mouse_y):
    """Se declaran las variables globales *holding_card_group* *holding_cards* *mouse_cords*,
    Se declara la lista vacía *possible_cards*,
    Se guardan las coordenadas del cursor en la variable *mouse_cards*."""
    global holding_card_group, holding_cards, mouse_cords
    possible_cards = []
    mouse_cords = (mouse_x, mouse_y)

    """Se itera sobre la lista de objetos *tables*, y por cada objeto se itera sobre las cartas en la mesa (almacenadas en *table.get_table()*). 
    Si la carta está en la posición de frente, se agrega a la lista possible_cards como una tupla con la carta y la mesa donde se encuentra."""
    for table in tables:
        for table_card in table.get_table():
            if table_card.is_front_showing():
                possible_cards.append((table_card, table))

    """Se itera sobre la lista de objetos *foundations*, y por cada objeto se obtiene la carta en la cima de la pila (almacenada en *foundation.get_top_card()*). 
    Si hay una carta en la cima, se agrega a la lista *possible_cards* como una tupla con la carta y la foundation donde se encuentra."""
    for foundation in foundations:
        foundation_card = foundation.get_top_card()
        if foundation_card!=None:
            possible_cards.append((foundation_card, foundation))

    """Se obtiene la carta en la cima de la pila de descarte (almacenada en *waste.get_top_card()*), 
    si hay una carta en la cima, se agrega a la lista *possible_cards* como una tupla con la carta y la pila de descarte."""
    waste_card = waste.get_top_card()
    if waste_card!=None:
        possible_cards.append((waste_card, waste))
    
    """Se itera sobre la lista *possible_cards*, y por cada carta se obtienen sus coordenadas con *card_x* y *card_y*. 
    Luego, se verifica si las coordenadas del cursor se encuentran sobre la carta y si es así, 
    se establece la variable global *holding_card_group* a la table/foundtaion/deck de descarte de la carta. 
    Si la table/foundation es tables, entonces se obtienen las cartas debajo de la carta seleccionada y se almacenan en la variable global *holding_cards*. 
    Si la table/foundation es otra cosa, se establece la variable global *holding_cards* como una lista con la carta seleccionada."""
    for card in possible_cards:
        card_x = card[0].get_coordinates()[0]
        card_y = card[0].get_coordinates()[1]
        if mouse_x > card_x and mouse_x < card_x + 100 and mouse_y>card_y and mouse_y < card_y + 145:
            holding_card_group = card[1]
            if holding_card_group in tables:
                holding_cards = holding_card_group.get_cards_below(card[0])
            else:
                holding_cards = [card[0]]

"""
La función *place_card(a, b)* es una función que se llama cuando el jugador intenta colocar una carta arrastrándola con el cursor.
La función comienza por verificar si se está intentando hacer una auto-colocación de una carta sobre la que ya se está sosteniendo. 
Si es así, entonces la función intenta colocar la carta en una pila de la base o en una pila de la foundation, según corresponda.

Si la carta no se está colocando en la misma posición donde se la está sosteniendo, entonces se determina la columna de la tabla donde
se intenta colocar la carta arrastrada, y se verifica si la carta puede ser colocada en esa columna de acuerdo a las reglas del solitario.
Si no puede ser colocada en ninguna columna de la tabla, entonces se intenta colocarla en una de las foundations.
Si la carta no puede ser colocada en ninguna parte, se la deja en su posición original.
En cada caso en que se pueda colocar la carta, se remueve de la mano del jugador y se reproduce un sonido.
Al final, la función ajusta las cartas que quedan en la mano del jugador.
"""
def place_card(mouse_x, mouse_y):
    
    """Se declaran las variables globales que se utilizan en la función. 
    *holding_card_group* es un objeto que representa un grupo de cartas que se están sujetando,
    *holding_cards* es una lista de objetos de carta que se están sujetando, 
    *mouse_cords* es una tupla que representa la ubicación actual del mouse,
    *tables* es una lista de objetos de tabla que representan las siete pilas de cartas en el juego, y 
    *moves* es un contador de movimientos realizados en el juego."""
    global holding_card_group, holding_cards, mouse_cords, tables, moves

    """Este bloque de código se ejecuta si el cursor está en la mismas coordenadas que en la última llamada a la función (es la forma de ejecutar el autoclick).
    El código mueve una carta 'automáticamente' hacia su próxima posición posible, con un click (autofill click).
    Si solo se está sujetando una carta (*holding_cards* tiene una longitud de 1), se verifica si la carta se puede colocar en una foundation. 
    (Las foundations son las cuatro pilas de cartas que se construyen en orden ascendente según su palo).
    Si la carta que se está sujetando es del mismo palo que la cima de una foundation existente y su valor es uno más alto, 
    se coloca la carta en la cima de la foundation y se eliminan las cartas sujetadas. 
    Finalmente se reproduce un sonido de colocación de carta y se aumenta el contador de movimientos."""
    if mouse_cords == (mouse_x, mouse_y):
        if len(holding_cards)==1:
            for foundation in foundations:
                if foundation.get_suit() == holding_cards[0].get_suit():
                    foundation_card = foundation.get_top_card()
                    if foundation_card!=None:
                        if foundation_card.get_value()+1 == holding_cards[0].get_value():
                            foundation.add_card(holding_cards[0])
                            holding_card_group.remove_card()
                            place_sound.play()
                            moves += 1
                            return
                    else:
                        if holding_cards[0].get_value() == 1:
                            foundation.add_card(holding_cards[0])
                            holding_card_group.remove_card()
                            place_sound.play()
                            moves += 1
                            return

        """Esta parte del código itera a través de una lista de objetos *table* y comprueba si el objeto *holding_cards* puede ser colocado en alguna de ellas. 
        Si se encuentra una *table* donde se pueda colocar la carta, se añaden todas las cartas de *holding_cards* a esa *table*
        usando el método *add_cards()* y se eliminan de *holding_card_group* usando el método *remove_card()*.
        También se reproduce un sonido de colocación y se actualiza el contador de movimientos.

        La condición para poder colocar la carta es que la última carta de la mesa tenga el valor de un número menor que la carta que se está intentando colocar y
        que los colores de las cartas sean diferentes. Si la última carta de la mesa no existe, se comprueba si la carta que se está intentando colocar es un Rey (valor 13)
        y se puede colocar en la mesa vacía. Si se encuentra una mesa adecuada para colocar la carta, se usa *return* para salir de la función."""
        for table in tables:
            bottom_card = table.bottom_card()
            if bottom_card!=None:
                value = bottom_card.get_value()
                if bottom_card.get_color()!=holding_cards[0].get_color() and value-1==holding_cards[0].get_value():
                    table.add_cards(holding_cards)
                    for card in holding_cards:
                        holding_card_group.remove_card()
                        place_sound.play()
                        moves += 1
                    return
            else:
                if holding_cards[0].get_value() == 13:
                    table.add_cards(holding_cards)
                    for card in holding_cards:
                        holding_card_group.remove_card()
                    place_sound.play()
                    moves += 1
                    return
                

    else:
        """Si no se cumple la primera condición (la carta se ha soltado en un palo de Foundation), entonces ejecuta el siguiente bloque de código.
        Crea una lista llamada "positions" que contiene las posiciones horizontales de las siete pilas de cartas de juego. 
        La lista está ordenada de derecha a izquierda (del palo de cartas de juego más cercano al borde derecho de la pantalla al palo de cartas de juego más cercano al borde izquierdo de la pantalla).
        Inicializamos una variable *count* con valor 0.
        """
        positions = [950, 825, 710, 590, 470, 355, 242, 120]
        count = 0
        
        """Se itera a través de la lista *positions* 
        Si la posición actual en el bucle (representada por *pos*) es menor que la posición horizontal del mouse (representada por *mouse_x*),
        entonces se rompe el bucle y se actualiza el valor de *count* al número de posiciones en la lista que son menores que la posición horizontal del mouse. """
        for pos in positions:
            if mouse_x > pos:
                break
            count += 1
        
        """ Si *count* es mayor que cero, significa que el cursor está a la derecha de la primera *table*, por lo que se puede soltar la carta en una *table*."""
        if count > 0:
            """Se obtiene la *table* correspondiente al valor de *count*, donde el valor 7 representa la última *table* y el valor 0 la primera """
            table = tables[7-count]
            """Se obtiene la *bottom_card*, que es la carta inferior de la *table* seleccionada."""
            bottom_card = table.bottom_card()
            
            """Si hay una carta en la *table* seleccionada, se compara su color y valor con la carta que se está sosteniendo.
            Si la *bottom_card* tiene un color diferente y su valor es exactamente uno menor que la carta sostenida,
            se colocan las cartas sostenidas en la mesa, se eliminan de la mano, se reproduce un sonido y se incrementa el contador de movimientos."""
            if bottom_card != None:
                value = bottom_card.get_value()
                if bottom_card.get_color() != holding_cards[0].get_color() and value - 1 == holding_cards[0].get_value():
                    table.add_cards(holding_cards)
                    for card in holding_cards:
                        holding_card_group.remove_card()
                        place_sound.play()
                        moves+=1
                    return
            else: # Si no hay una carta en la *table* seleccionada, se comprueba si la carta sostenida es un Rey (valor 13). 
                
                """Si es así, se coloca la carta en la mesa, se elimina de la mano, se reproduce un sonido y se incrementa el contador de movimientos."""
                if holding_cards[0].get_value() == 13:
                    table.add_cards(holding_cards)
                    for card in holding_cards:
                        holding_card_group.remove_card()
                    place_sound.play()
                    moves += 1
                    return
        else: # Si no se cumple la condición anterior (es decir, si no se hizo click en una de las *tables*), el código entra en este bloque de código.
            
            """Se recorren las Foundation."""
            for foundation in foundations:
                
                """Si la Foundation actual es del mismo palo que la carta que se estás sosteniendo en el cursor del mouse, se ejecuta el bloque de código."""
                if foundation.get_suit() == holding_cards[0].get_suit():
                    
                    """Se obtiene la carta superior de la foundation actual."""
                    foundation_card = foundation.get_top_card()
                    
                    """Si hay una carta en la Foundation, se ejecuta el siguiente código."""
                    if foundation_card != None:
                        
                        """Si la carta sostenida en el cursor del mouse tiene un valor que es 1 unidad mayor que el valor de la carta superior de la foundation actual, se ejecuta el siguiente bloque de código.
                        La carta sostenida en el cursor del mouse se agrega a la foundation actual, se elimina de la lista de cartas sostenidas y se reproduce un sonido de "colocación". 
                        Además, se incrementa el número de movimientos realizados y se sale de la función."""
                        if foundation_card.get_value()+1 == holding_cards[0].get_value():
                            foundation.add_card(holding_cards[0])
                            holding_card_group.remove_card()
                            place_sound.play()
                            moves += 1
                            return
                    else: # Si no hay cartas en la foundation actual, se ejecuta el siguiente bloque de código.
                        
                        """SI la carta sostenida en el cursor es un AS (valor igual a 1), se ejecuta el siguiente bloque de código."""
                        if holding_cards[0].get_value() == 1:
                            
                            """La carta sostenida en el cursor se agrega a la foundation actual, se elimina de la lista de cartas sostenidas y se reproduce un sonido de "colocación". 
                            Además, se incrementa el número de movimientos realizados y se sale de la función."""
                            foundation.add_card(holding_cards[0])
                            holding_card_group.remove_card()
                            place_sound.play()
                            moves += 1
                            return

    """Se actualiza la posición de todas las cartas en la lista de cartas sostenidas para que se muestren correctamente en la pantalla."""
    holding_card_group.set_cards()


"""Función que permite que las cartas seleccionadas por el usuario sigan al cursor mientras se arrastran por la pantalla."""
def card_follow_mouse(mouse_x, mouse_y):
    
    """Se verifica si se están sosteniedno cartas, es decir, si la variable global *holding_cards* no está vacía."""
    if holding_cards != []:
        
        """Se define la posición de la carta que sigue al cursor:
        La variable *x* se establece como el valor de la posición horizontal del cursor menos 50 (mitad de la anchura de la carta).
        La variable *y* se establece como el valor de la posición vertical del cursor menos 50 (mitad de la altura de la carta).
        La variable *pos* se establece en 0 y se utiliza para calcular la posición vertical de cada carta que sigue el cursor."""
        x = mouse_x - 50
        y = mouse_y - 50
        pos = 0
        
        """Se itera a través de las cartas en *holding_cards*, se les asigna una nueva coordenada vertical que se basa en 
        la posición *y* y se incrementa por 40 veces la variable *pos*."""
        for card in holding_cards:
            card.set_coordinates(x, y + (pos * 40))
            """Finalmente, cada carta se dibuja en pantalla usando la función *draw()* de *pygame.sprite.GroupSingle()*"""
            pygame.sprite.GroupSingle(card).draw(screen)
            """La variable pos se incrementa en 1 en cada iteración para que las cartas queden apiladas visualmente."""
            pos += 1

"""Función crea una lista de objetos Table (Las 7 pilas de la mesa) y luego devuelve la lista completa de tablas.
Se crea una lista *tables*, y se define la variable *x* inicializada en 25 para separar las tablas en 25px sobre el eje x.
Luego se  realiza un bucle FOR que itera sobre un rango de 1 a 7 para construir cada tabla.
En cada iteración se agrega una nueva tabla a la lista *tables*, construyendo un nuevo objeto *Table*.
Al objeto se le pasa una posición horizontal *x*, el objeto *deck* y la cantidad de cartas a mostrar en
la tabla, que comienza en *card_amount* = 1 (una carta) y aumenta +1 en cada iteración, haciendo que vaya de 1 a 7 cartas,
luego se actualiza la posición *x* para la siguiente tabla, que se posicióna 125 píxeles a la derecha de la tabla anterior.
Finalmente retorna la lista de tables."""
def create_tables():
    tables = []
    x = 25
    for card_amount in range(1, 8):
        tables.append(Table(x, deck, card_amount))
        x += 125
        card_amount += 1
    return tables

"""Función crea y devuelve una lista de objetos *Foundation*
La Foundation son las áreas del juego donde se construyen las cartas de cada palo en orden ascendente.
"""
def create_foundations():
    """Se define una lista vacía de foundations para almacenar los Objetos Foundation.
    Se establece la coordenada x para situar las cartas de la primera Foundation.
    Se define una lista con los cuatro palos de la baraja para establecer el palo de la Foundation."""
    foundations = []
    x = 400
    suits = ["hearts", "diamonds", "spades", "clubs"]
    
    """Se itera 4 veces, se agrega a la lista *foundations* un nuevo objeto Foundation, con su respectivo palo y coordenada horizontal."""
    for i in range(len(suits)):
        foundations.append(Foundation(x, suits[i]))
        x += 125
    """Se retornan todas las *foundations*"""
    return foundations

"""Función que verifica constantemente que cada Foundation tenga 13 cartas, si se cumple la condición, se ganó el juego.
(La idea es que te permita decidir si jugar de nuevo o no)."""
def check_win():
    count = 0
    for foundation in foundations:
        complete_pile = foundation.get_Foundation()
        if len(complete_pile) != 13:
            return
        else:
            count += 1
    print("check_win:", count)
    if count == 4:
        
        count += 1
        x = messagebox.askquestion(message="¿Do you want to play again?", title="You win the game!")
        if x == 'yes':
            pygame.quit()
            game_loop()
            # Ver como hacer para resetear el juego.
    
        else:
            pygame.quit()
            quit()
            
def check_autowin():
    count = 0
    global moves, tables
    for table in tables:
        card = table.bottom_card()
        all_cards = len(table.get_table())
        card_count = 0
        for card in table.get_table():
            if card.is_front_showing():
                card_count += 1
        if all_cards == card_count:
            count += 1
    if count == 7:
        for table in tables:
            card = table.bottom_card()
            if card is not None:
                print(card.get_value(), card.get_suit())
                coords = card.get_coordinates()
                for foundation in foundations:
                    time.sleep(0.05)
                    if foundation.get_suit() == card.get_suit():
                        foundation_card = foundation.get_top_card()
                        if foundation_card != None:
                            if foundation_card.get_value() + 1 == card.get_value():
                                card_follow_mouse(coords[0], coords[1])
                                foundation.add_card(card)
                                table.remove_card()
                                place_sound.play()
                                moves += 1
                                continue
                        else:
                            if card.get_value() == 1:
                                card_follow_mouse(coords[0], coords[1])
                                foundation.add_card(card)
                                table.remove_card()
                                place_sound.play()
                                moves += 1
                                continue

"""
Se crean las dos listas del juego, *tables* y *foundations*

La lista *tables* se crea llamando a la función *create_tables()*, la cual crea siete objetos 
de la clase *Table* con diferentes cantidades de cartas en cada mesa y los agrega a la lista *tables*. 
Cada mesa está separada por un espacio horizontal de 125 píxeles.

La lista *foundations* se crea llamando a la función *create_foundations()*, 
la cual crea cuatro objetos de la clase *Foundation* para cada uno de los palos de la baraja
(corazones, diamantes, picas y tréboles) y los agrega a la lista *foundations*. 
Cada foundation está separada por unespacio horizontal de 125 píxeles.
"""
tables = create_tables()
foundations = create_foundations()


"""Esta función muestra un mensaje de texto en la pantalla del juego. 
Toma dos parámetros: el primer parámetro es el texto que se mostrará en la pantalla
y el segundo parámetro es la posición en la que se mostrará el texto.

Se utiliza para mostrar en pantalla el puntaje, movimientos y tiempo.

La función primero carga la fuente de texto desde un archivo ttf y luego crea una superficie
de texto con el tamaño y color de fuente deseado. A continuación, se establece la posición del
rectángulo que contiene el texto y se centra en la posición proporcionada como parámetro. 
Finalmente, el texto se dibuja en la pantalla en la posición del rectángulo."""
def message_display(text, cords):
    large_text = pygame.font.Font('assets/freesansbold.ttf',17)
    text_surface = large_text.render(text, True, (255,255,255))
    TextSurf, TextRect = text_surface, text_surface.get_rect()
    TextRect.center = cords
    screen.blit(TextSurf, TextRect)


"""Función que verifica constantemente que cada Foundation tenga 13 cartas, si se cumple la condición, se ganó el juego.
(La idea es que te permita decidir si jugar de nuevo o no)."""
def check_win():
    count = 0
    for foundation in foundations:
        complete_pile = foundation.get_Foundation()
        if len(complete_pile) != 13:
            return
        else:
            count += 1
    print("check_win:", count)
    if count == 4:
        
        count += 1
        x = messagebox.askquestion(message="¿Do you want to play again?", title="You win the game!")
        if x == 'yes':
            pygame.quit()
            game_loop()
            # Ver como concha hacer para resetear el juego.
    
        else:
            pygame.quit()
            quit()


def check_autowin():
    count = 0
    global moves, tables
    for table in tables:
        card = table.bottom_card()
        all_cards = len(table.get_table())
        card_count = 0
        for card in table.get_table():
            if card.is_front_showing():
                card_count += 1
        if all_cards == card_count:
            count += 1
    if count == 7:
        for table in tables:
            card = table.bottom_card()
            if card is not None:
                coords = card.get_coordinates()
                for foundation in foundations:
                    if foundation.get_suit() == card.get_suit():
                        foundation_card = foundation.get_top_card()
                        if foundation_card != None:
                            if foundation_card.get_value() + 1 == card.get_value():
                                card_follow_mouse(coords[0], coords[1])
                                foundation.add_card(card)
                                table.remove_card()
                                place_sound.play()
                                moves += 1
                                continue
                        else:
                            if card.get_value() == 1:
                                card_follow_mouse(coords[0], coords[1])
                                foundation.add_card(card)
                                table.remove_card()
                                place_sound.play()
                                moves += 1
                                continue
                            

"""Algoritmo: El marino

El marino es un señor algoritmo que se encarga de tocar todo lo que puede hasta fenecer o ganar.

Funcionamiento:

    Para cada table de entre todas las tables:
        Agarra la última carta de la table
            Si la carta existe:
                Intenta colocarla en algún foundation.
                    Si no se pudo: 
                        Intenta colocarla en una table distinta.
                        Si no pudo:
                            Intenta colocar la carta más alta visible de la table actual en una table distinta.
        Si no se movió:
            Agarra una carta del mazo VISIBLE.
            Si la carta existe:
                Intenta colocarla en algún foundation.
                    Si no se pudo: 
                        Intenta colocarla en una table distinta.
                        
        Si no se movió y el mazo NO VISIBLE esta vacío:
            rellena el mazo NO VISIBLE con TODAS las cartas del mazo VISIBLE.
            vacía el mazo VISIBLE.
        
        Si no se movió y el mazo VISIBLE no esta vacío:
            Saca una carta del mazo
    
    Mientras tanto rellena una lista *check_if_lock = []*
    
    Si pudo colocar una carta al foundation o a la table: 
        agrega un True a la lista
        
    Si no pudo mover ninguna carta y agarró una carta del mazo NO VISIBLE o se quedo sin cartas en el mazo NO VISIBLE y lo relleno de nuevo:
        agrega un False a la lista
        
    En el caso de que los últimos 24 elementos de la lista *check_if_lock = []* sean FALSE:
        Perdiste el juego.

            (Esto significa que intento todos los movimientos antes mencionados y no logró ningun cambio, por ende,
            no es capaz de mover cartas de la table o del mazo a ningún foundation o table, lo que significa que se perdió el juego).
        
"""

check_if_lock = []

def auto_solve():
    
    global moves, game_is_running, check_if_lock
    
    """Se declara la variable *moved* que determinará si el algoritmo movió una carta, si moved = True, la función se reinicia."""
    moved = False
    
    """Se declara la variable *check_if_moved* que se almacenará en la lista *check_if_lock = []*"""
    check_if_moved = True
    
    """Bucle que revisa todas las table entre las 7 tables"""
    for table in tables:
        
        """Obtiene la última carta de la table seleccionada."""
        card = table.bottom_card()
        if card is not None:
            """Función que revisa si puede mover la carta seleccionada a algun foundation."""
            moved = bottom_card_foundation(card, table, moved)
            if not moved:
                """Función que revisa si puede mover la carta seleccionada a otra table."""
                moved = bottom_card_table(card, table, moved)
                if not moved:
                    """Función que obtiene una lista de todas las cartas visibles de la table."""
                    cards = table.get_showing_cards(table.get_table())
                    if len(cards[0]) > 1:
                        """Función que revisa si puede mover la carta más alta visible de la table seleccionada, a otra table."""
                        moved = upper_card_table(cards, table, moved)
    
    """Si aún no se movió ninguna carta y alguno de los mazos de residuos aún tienen cartas."""
    if not moved and len(deck.get_deck()) > 0 or len(waste.get_waste_pile()) > 0:
        """Si el mazo VISIBLE tiene cartas."""
        if not waste.show_is_empty():
            """Función que ingresa a las condiciones para mover una carta del mazo."""
            moved = check_waste_card(moved)
    
    """Si aún no se movió ninguna carta y el mazo NO VISIBLE esta vacío, rellenar el mazo NO VISIBLE con las cartas del mazo VISIBLE"""
    if not moved and len(deck.get_deck()) <= 0:
        deck.add_cards(list(reversed(waste.get_waste_pile().copy())))
        waste.empty()
        moves += 1
        check_if_moved = False
    
    """Si aún no se movió ninguna carta y el mazo VISIBLE tiene cartas, sacar una carta del mazo NO VISIBLE."""
    if not moved and len(deck.get_deck()) > 0:
        waste.add_card(deck.remove_card())
        moves += 1
        check_if_moved = False
    
    """En este bloque de código se observan los últimos 24 movimientos de la partida (las mismas cartas que hay default en el mazo), si el algoritmo
    solo intentó sacar cartas del mazo NO VISIBLE en los últimos 24 movimientos, significa que no puede mover ninguna carta más y perdió la partida."""
    check_if_lock.append(check_if_moved)
    last_twentyfour = check_if_lock[-24:]
    if True not in last_twentyfour:
        x = messagebox.askquestion(message="¿Do you want to play again?", title="You lose >:(")
        if x == 'yes':
            pygame.quit()
            game_loop()
            # Ver como concha hacer para resetear el juego.
        else:
            pygame.quit()
            quit()
        
    """Refresca la pantalla."""
    pygame.display.update()

            
def check_waste_card(moved):
    global moves
    
    """Obtiene la carta visible del mazo VISIBLE."""
    waste_card = waste.get_top_card()
    if waste_card is not None:
        """Función que revisa si puede mover la carta seleccionada a algun foundation."""
        moved = waste_card_foundation(waste_card, moved)
        if not moved:
            """Función que revisa si puede mover la carta seleccionada a alguna table."""
            moved = waste_card_table(waste_card, moved)
    return moved

def bottom_card_foundation(card, table, moved):
    global moves
    for foundation in foundations:
        if foundation.get_suit() == card.get_suit():
            if card.get_value() == 1:
                foundation.add_card(card)
                table.remove_card()
                moved = True
                moves += 1
                time.sleep(0.2)
                break
            else:
                foundation_card = foundation.get_top_card()
                if foundation_card is not None:
                    if foundation_card.get_value() + 1 == card.get_value():
                        foundation.add_card(card)
                        table.remove_card()
                        moved = True
                        moves += 1
                        time.sleep(0.2)
                        break
    return moved

def waste_card_foundation(waste_card, moved):
    global moves
    for foundation in foundations:
        if waste_card is not None:
            if foundation.get_suit() == waste_card.get_suit():
                if waste_card.get_value() == 1:
                    foundation.add_card(waste_card)
                    waste.remove_card()
                    moved = True
                    moves += 1
                    time.sleep(0.2)
                    break
                else:
                    foundation_card = foundation.get_top_card()
                    if foundation_card is not None:
                        if foundation_card.get_value() + 1 == waste_card.get_value():
                            foundation.add_card(waste_card)
                            waste.remove_card()
                            moved = True
                            moves += 1
                            time.sleep(0.2)
                            break
    return moved

def bottom_card_table(card, table, moved):
    global moves
    for dest_table in tables:
        if dest_table != table:
            dest_card = dest_table.bottom_card()
            if dest_card is None:
                if card.get_value() == 13:
                    prev_card = table.prev_card()
                    if prev_card is not None:
                        if not prev_card.is_front_showing():
                            dest_table.add_new_card(card)
                            table.remove_card()
                            moved = True
                            moves += 1
                            time.sleep(0.2)
                    else:
                        dest_table.add_new_card(card)
                        table.remove_card()
                        moved = True
                        moves += 1
                        time.sleep(0.2)
                    
            else:
                if dest_card.get_color() != card.get_color():
                    if dest_card.get_value() - 1 == card.get_value():
                        prev_card = table.prev_card()
                        if prev_card is not None:
                            if not prev_card.is_front_showing():
                                dest_table.add_new_card(card)
                                table.remove_card()
                                moved = True
                                moves += 1
                                time.sleep(0.2)
                                break

    return moved

def waste_card_table(card, moved):
    global moves
    
    for dest_table in tables:
        dest_card = dest_table.bottom_card()
        if dest_card is not None:
            if dest_card.get_color() != card.get_color():
                if dest_card.get_value() - 1 == card.get_value():
                    dest_table.add_new_card(card)
                    waste.remove_card()
                    moved = True
                    moves += 1
                    time.sleep(0.2)
                    break
        else:
            if card.get_value() == 13:
                dest_table.add_new_card(card)
                waste.remove_card()
                moved = True
                moves += 1
                time.sleep(0.2)
    return moved

def upper_card_table(cards, table, moved):
    global moves
    for dest_table in tables:
        if dest_table != table:
            dest_card = dest_table.bottom_card()
            if dest_card is None:
                if cards[0][0].get_value() == 13:
                    if cards[1] == True:
                        return
                    else:
                        dest_table.add_cards(cards[0])
                        for card in cards[0]:
                            table.remove_card()
                        cards[0].clear()
                        moved = True
                        moves += 1
                        time.sleep(0.2)
                        break

            if dest_card is not None:
                if dest_card.get_color() != cards[0][0].get_color():
                    if dest_card.get_value() - 1 == cards[0][0].get_value():
                        dest_table.add_cards(cards[0])
                        for card in cards[0]:
                            table.remove_card()
                        moved = True
                        moves += 1
                        time.sleep(0.2)
                        break
    return moved

"""Esta función es el núcleo del juego, en el que se ejecuta todo el código principal."""
def game_loop():
    start_time = time.time()
    """Se declara la variable global *holding_cards* (puede ser accedida y modificada desde cualquier lugar del programa). 
    *holding_cards* es una lista de objetos de carta que se están sujetando"""
    global holding_cards
    
    """Se establece un bucle *while* que se ejecutará mientras la variable *game_is_running* = True, esta variable controla si el jeugo está en ejecución o no, y es declarada por defecto como True."""
    while game_is_running:
        timer = int(time.time() - start_time)
        """En esta línea se obtiene la posición del cursor en la ventana del juego y se guarda en dos variables, *mouse_x* y *mouse_y*."""
        mouse_x, mouse_y = pygame.mouse.get_pos()

        """En este bucle se recorren todos los eventos de la cola de eventos de Pygame. 
        Esto permite manejar eventos de teclado, mouse y otros eventos relacionados con la ventana del juego."""
        for event in pygame.event.get():
            
            """En este bloque de código se verifica si el evento actual es un click del botón del mouse. 
            Si es así, se llaman a dos funciones: clicked_new_card(x, y) y check_holding_card(x, y)."""
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked_new_card(mouse_x, mouse_y)
                check_holding_card(mouse_x, mouse_y)
            
            """En este bloque de código se verifica si el evento actual es la desclick del botón del mouse. 
            Si *holding_cards* no está vacía, se llama a la función place_card(x, y), se establece *holding_cards* como una lista vacía y se llama a la función waste.set_cards()."""
            if event.type == pygame.MOUSEBUTTONUP:
                if holding_cards != []:
                    place_card(mouse_x, mouse_y)
                    holding_cards = []
                    waste.set_cards()
                    
            """En este bloque de código se verifica si el evento actual es el cierre de la ventana del juego. 
            Si es así, se llama a la función pygame.quit() para salir de Pygame y se llama a quit() para salir del programa por completo.
            """
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()

        """En esta línea se dibuja la imagen de fondo en la ventana del juego. backgroundImage es una imagen cargada anteriormente. (detrás de todo)"""
        screen.blit(backgroundImage, (0, 0))

        """En este bloque de código se dibujan todas las cartas en las *tables* del juego. 
        Se recorre cada *table* en la lista *tables*, y para cada *table* se recorre su lista de cartas y se dibujan todas las cartas que no están en *holding_cards*.
        
        El bucle FOR recorre cada pila de mesas (table) y llama al método get_table() para obtener la lista de cartas de cada pila.
        Luego, se verifica si la carta no se está sosteniendo con el cursor (not card in holding_cards).
        Si es así, la carta se dibuja en la pantalla usando el método draw() de pygame.sprite.GroupSingle."""
        for table in tables:
            for card in table.get_table():
                if not card in holding_cards:
                    pygame.sprite.GroupSingle(card).draw(screen)

        """El bucle FOR recorre cada pila de base (foundation) y llama al método get_top_card() para obtener la carta en la cima de cada pila. 
        Luego, se verifica si la carta no se está sosteniendo con el cursor (not card in holding_cards). 
        Si es así, la carta se dibuja en la pantalla usando el método draw() de pygame.sprite.GroupSingle."""
        for foundation in foundations:
            card = foundation.get_top_card()
            if not card in holding_cards:
                pygame.sprite.GroupSingle(card).draw(screen)

        """El bucle FOR recorre cada carta en la pila de descarte (waste) llamando al método get_show_waste_pile(). 
        Luego, se verifica si la carta no se está sosteniendo con el ratón (not card in holding_cards). 
        Si es así, la carta se dibuja en la pantalla usando el método draw() de pygame.sprite.GroupSingle."""
        for card in waste.get_show_waste_pile():
            if not card in holding_cards:
                pygame.sprite.GroupSingle(card).draw(screen)

        """Función que dibuja cualquier carta que se esté sosteniendo con el ratón en la posición actual del ratón."""
        card_follow_mouse(mouse_x, mouse_y)

        """Se llama a la función message_display() tres veces para mostrar el temporizador, la puntuación y el número de movimientos en la parte superior de la pantalla."""
        message_display(str(timer), (352, 39))
        message_display(str(score), (454, 39))
        message_display(str(moves), (561, 39))

        """Función que actualiza la pantalla con los cambios realizados."""
        pygame.display.update()
        
        """FUnción que limita la velocidad del juego a 60 fotogramas por segundo."""
        clock.tick(60)
        
        auto_solve()

game_loop()