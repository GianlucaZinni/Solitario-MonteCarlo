import pygame
from Deck import Deck
from Waste import Waste
from Foundation import Foundation
from Table import Table
from pygame.locals import RESIZABLE
import time


# Se inicializa la biblioteca Pygame, permitiendo utilizar sus funciones y métodos.
pygame.init()

# Luego se define el tamaño de la ventana de juego. Primero el eje X y luego el eje Y.
window_size = (900, 885)

"""Se utiliza la función *pygame.display.set_mode()* 
para crear la ventana con el tamaño definido."""
screen = pygame.display.set_mode(window_size, RESIZABLE)

"""Luego se utiliza la función *pygame.display.set_caption()* 
para establecer el título de la ventana."""
pygame.display.set_caption("Solitario")

"""Se instancia la variable booleana *game_is_running* 
que se utilizará para mantener encendido el juego."""
game_is_running = True

"""Finalmente se guarda en la variable backgroundImage se utiliza la función 
*pygame.image.load()* para cargar la imagen del fondo del juego."""
backgroundImage = pygame.image.load("D:/My Drive/Universidad/CUARTO AÑO/Modelos y Simulación/Método de Montecarlo/Montecarlo/Solitario-Montecarlo/assets/backgroundd.jpg")

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

place_sound = pygame.mixer.Sound('D:/My Drive/Universidad/CUARTO AÑO/Modelos y Simulación/Método de Montecarlo/Montecarlo/Solitario-Montecarlo/assets/flip.wav')
shuffle_sound = pygame.mixer.Sound('D:/My Drive/Universidad/CUARTO AÑO/Modelos y Simulación/Método de Montecarlo/Montecarlo/Solitario-Montecarlo/assets/shuffle.wav')
shuffle_sound.play()

"""Función que comprueba si el usuario hizo click en el mazo de residuo no visible.
Si lo ha hecho, se comprueba si el mazo está vacío. Si lo está, las cartas
de la pila de residuo visible se devuelven a la pila de residuo no visible y se barajan. 
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

"""
Comprueba si el usuario esta sosteniendo alguna carta. Si es así, se actualiza
la posición de la carta para que coincida con la posición del cursor.
Si el usuario no está sosteniendo ninguna carta, se comprueba si el cursor está
sobre una carta que se pueda mover. Si es así, se añade esa carta y todas las cartas
debajo de ella a la lista *holding_cards* y se establece *holding_card_group* en el
grupo de cartas correspondiente.
"""
def check_holding_card(mouse_x, mouse_y):
    """Se declaran las variables globales *holding_card_group* *holding_cards* *mouse_cords*
    Se declara la lista vacía *possible_cards*
    Se guardan las coordenadas del cursor en la variable *mouse_cards*"""
    global holding_card_group, holding_cards, mouse_cords
    possible_cards = []
    mouse_cords = (mouse_x, mouse_y)

    """Se itera sobre la lista de objetos *tables*, y por cada objeto se itera sobre las cartas en la
    mesa (almacenadas en *table.get_table()*). Si la carta está en la posición de frente, se agrega
    a la lista possible_cards como una tupla con la carta y la mesa donde se encuentra."""
    for table in tables:
        for table_card in table.get_table():
            if table_card.is_front_showing():
                possible_cards.append((table_card, table))

    """Se itera sobre la lista de objetos *foundations*, y por cada objeto se obtiene la carta en la
    cima de la pila (almacenada en *foundation.get_top_card()*). Si hay una carta en la cima, 
    se agrega a la lista *possible_cards* como una tupla con la carta y la foundation donde se encuentra."""
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
    Si la table/foundation es tables, entonces se obtienen las cartas debajo de la carta seleccionada
    y se almacenan en la variable global *holding_cards*. Si la table/foundation es otra cosa, se establece
    la variable global *holding_cards* como una lista con la carta seleccionada."""
    for card in possible_cards:
        card_x = card[0].get_coordinates()[0]
        card_y = card[0].get_coordinates()[1]
        if mouse_x > card_x and mouse_x < card_x + 100 and mouse_y>card_y and mouse_y < card_y + 145:
            holding_card_group = card[1]
            if holding_card_group in tables:
                holding_cards = holding_card_group.get_cards_below(card[0])
            else:
                holding_cards = [card[0]]

def place_card(mouse_x, mouse_y):
    global holding_card_group, holding_cards, mouse_cords, tables, moves

    #auto fill with click
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
        positions = [950, 825, 710, 590, 470, 355, 242, 120]
        count = 0
        for pos in positions:
            if mouse_x>pos:
                break
            count+=1
        if count>0:
            table = tables[7-count]
            bottom_card = table.bottom_card()
            if bottom_card != None:
                value = bottom_card.get_value()
                if bottom_card.get_color() != holding_cards[0].get_color() and value - 1 == holding_cards[
                    0].get_value():
                    table.add_cards(holding_cards)
                    for card in holding_cards:
                        holding_card_group.remove_card()
                        place_sound.play()
                        moves+=1
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

    holding_card_group.set_cards()

"""Función que permite que las cartas seleccionadas por el usuario sigan
al cursor mientras se arrastran por la pantalla."""
def card_follow_mouse(mouse_x, mouse_y):
    """se verifica si se están sosteniedno cartas, es decir, si la variable global *holding_cards* no está vacía."""
    if holding_cards != []:
        
        """Se define la posición de la carta que sigue al cursor:
        La variable *x* se establece como el valor de la posición horizontal del cursor menos 50 (mitad de la anchura de la carta).
        La variable *y* se establece como el valor de la posición vertical del cursor menos 50 (mitad de la altura de la carta).
        La variable *pos* se establece en 0 y se utiliza para calcular la posición vertical de cada carta que sigue el cursor."""
        x = mouse_x - 50
        y = mouse_y - 50
        pos = 0
        
        """Se itera a través de las cartas en *holding_cards*, se les asigna una nueva coordenada vertical que se basa en
        la posición *y* y se incrementa por 40 veces la variable *pos*"""
        for card in holding_cards:
            card.set_coordinates(x, y + (pos * 40))
            """Finalmente, cada carta se dibuja en pantalla usando la función *draw()* de *pygame.sprite.GroupSingle()*"""
            pygame.sprite.GroupSingle(card).draw(screen)
            """La variable pos se incrementa en 1 en cada iteración para que las cartas queden apiladas visualmente."""
            pos += 1

"""Función crea una lista de objetos Table (Las 7 pilas de la mesa) y luego devuelve la lista completa de tablas.
Se crea una lista *tables*, y se define la variable *x* inicializada en 25 para separar las tablas
en 25px sobre el eje x.
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
    
    """Se itera 4 veces,
    se agrega a la lista *foundations* un nuevo objeto Foundation, con su respectivo palo y coordenada horizontal.
    """
    for i in range(len(suits)):
        foundations.append(Foundation(x, suits[i]))
        x += 125
    """Se retornan todas las *foundations*"""
    return foundations


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
    large_text = pygame.font.Font('D:/My Drive/Universidad/CUARTO AÑO/Modelos y Simulación/Método de Montecarlo/Montecarlo/Solitario-Montecarlo/assets/freesansbold.ttf',17)
    text_surface = large_text.render(text, True, (255,255,255))
    TextSurf, TextRect = text_surface, text_surface.get_rect()
    TextRect.center = cords
    screen.blit(TextSurf, TextRect)

def game_loop():
    global holding_cards
    while game_is_running:

        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked_new_card(mouse_x, mouse_y)
                check_holding_card(mouse_x, mouse_y)
            if event.type == pygame.MOUSEBUTTONUP:
                if holding_cards != []:
                    place_card(mouse_x, mouse_y)
                    holding_cards = []
                    #set because if card is placed the new ones need to pop out
                    waste.set_cards()
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()

        #Draw background image to screen (behind everything)
        screen.blit(backgroundImage, (0, 0))

        #Draw all cards in tables to the screen
        for table in tables:
            for card in table.get_table():
                if not card in holding_cards:
                    pygame.sprite.GroupSingle(card).draw(screen)

        for foundation in foundations:
            card = foundation.get_top_card()
            if not card in holding_cards:
                pygame.sprite.GroupSingle(card).draw(screen)

        #Draw all cards in waste bin to the screen
        for card in waste.get_show_waste_pile():
            if not card in holding_cards:
                pygame.sprite.GroupSingle(card).draw(screen)

        #Draw cards picked up by mouse
        card_follow_mouse(mouse_x, mouse_y)

        message_display(str(timer), (352, 39))
        message_display(str(score), (454, 39))
        message_display(str(moves), (561, 39))

        pygame.display.update()
        clock.tick(60)

game_loop()