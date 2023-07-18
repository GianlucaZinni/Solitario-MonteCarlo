import pygame, time, sys
from conf.Waste import Waste
from conf.Foundation import Foundation
from conf.Table import Table
from pygame.locals import RESIZABLE
from func.Movement import BasicMoves
from func.Strategies import ElMarino, LaSocialista, ElBombero, ElGobernador

class Game:
    def __init__(self, ejecucion, idEstrategia, deck):
        pygame.init()
        """Se utiliza la función *pygame.display.set_caption()* para establecer el título de la ventana."""
        pygame.display.set_caption("Partida: " + str(ejecucion) + " / Estrategia: " + str(idEstrategia) + " / Solitario")

        # Identificador de la estrategia del juego
        self.idEstrategia = idEstrategia

        """Configuración de la pantalla
        Se utiliza la función *pygame.display.set_mode()* para crear la ventana con el tamaño definido."""
        self.window_size = (900, 885)

        """Se utiliza la función *pygame.display.set_mode()* para crear la ventana con el tamaño definido."""
        self.screen = pygame.display.set_mode(self.window_size, RESIZABLE)
        
        """Finalmente se guarda en la variable backgroundImage se utiliza la función *pygame.image.load()* para cargar la imagen del fondo del juego."""
        self.backgroundImage = pygame.image.load("static/assets/layout/backgroundd.jpg")

        """Definen los efectos de sonido que se reproducen en el juego.
        La función *pygame.mixer.sound()* se utiliza para cargar el archivo de sonido en la variable correspondiente.
        Luego se reproduce el sonido al barajar las cartas utiliando la función *play()*"""
        # self.place_sound = pygame.mixer.Sound('static/assets/sounds/flip.wav')

        """Se instancia la variable booleana *game_is_running* que se utilizará para mantener encendido el juego."""
        self.game_is_running = True

        self.deck = deck

        # Se crea la instancia del objeto *Waste()*
        self.waste = Waste()
        self.clock = pygame.time.Clock()
        
        # Variable que almacena el mazo utilizado en la partida
        self.full_deck = self.deck.insert_all_cards()

        # Se declaran las variables globales utilizadas por el juego.
        # self.holding_cards = []         # Lista vacía que se utilizará para almacenar cartas que el usuario esta sosteniendo.
        # self.holding_card_group = None  # Variable establecida en None que luego se actualizará para indicar qué grupo de cartas esta sosteniendo el usuario.
        # self.mouse_cords = ()           # Tupla vacía que se actualizará cada vez que el usuario mueva el raton.
        self.moves = 0                  # Contador de movimientos.
        self.timer = 0                  # Contador de tiempo.

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
        self.tables = self.create_tables()
        self.foundations = self.create_foundations()

        # Variables para finalizar la partida
        self.check_if_lock = []
        self.result_counter = 0
        self.results = None

    """Función crea una lista de objetos Table (Las 7 pilas de la mesa) y luego devuelve la lista completa de tablas.
    Se crea una lista *tables*, y se define la variable *x* inicializada en 25 para separar las tablas en 25px sobre el eje x.
    Luego se  realiza un bucle FOR que itera sobre un rango de 1 a 7 para construir cada tabla.
    En cada iteración se agrega una nueva tabla a la lista *tables*, construyendo un nuevo objeto *Table*.
    Al objeto se le pasa una posición horizontal *x*, el objeto *deck* y la cantidad de cartas a mostrar en
    la tabla, que comienza en *card_amount* = 1 (una carta) y aumenta +1 en cada iteración, haciendo que vaya de 1 a 7 cartas,
    luego se actualiza la posición *x* para la siguiente tabla, que se posicióna 125 píxeles a la derecha de la tabla anterior.
    Finalmente retorna la lista de tables."""
    def create_tables(self):
        tables = []
        x = 25
        for card_amount in range(1, 8):
            tables.append(Table(x, self.deck, card_amount))
            x += 125
            card_amount += 1
        return tables
    
    """Función crea y devuelve una lista de objetos *Foundation*
    La Foundation son las áreas del juego donde se construyen las cartas de cada palo en orden ascendente.
    """
    def create_foundations(self):
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

    """Esta función muestra un mensaje de texto en la pantalla del juego. 
    Toma dos parámetros: el primer parámetro es el texto que se mostrará en la pantalla
    y el segundo parámetro es la posición en la que se mostrará el texto.

    Se utiliza para mostrar en pantalla el puntaje, movimientos y tiempo.

    La función primero carga la fuente de texto desde un archivo ttf y luego crea una superficie
    de texto con el tamaño y color de fuente deseado. A continuación, se establece la posición del
    rectángulo que contiene el texto y se centra en la posición proporcionada como parámetro. 
    Finalmente, el texto se dibuja en la pantalla en la posición del rectángulo."""
    def message_display(self, text, cords):
        large_text = pygame.font.Font("static/assets/fonts/Roboto-Bold.ttf", 17)
        text_surface = large_text.render(text, True, (255,255,255))
        TextSurf, TextRect = text_surface, text_surface.get_rect()
        TextRect.center = cords
        self.screen.blit(TextSurf, TextRect)

    """Esta función es el núcleo del juego, en el que se ejecuta todo el código principal."""
    def game_loop(self):
        start_time = time.time()
        moves = BasicMoves()
        
        elmarino = ElMarino()
        lasocialista = LaSocialista()
        elbombero = ElBombero()
        elgobernador = ElGobernador()

        """Se declara la variable global *self.holding_cards* (puede ser accedida y modificada desde cualquier lugar del programa). 
        *self.holding_cards* es una lista de objetos de carta que se están sujetando.
        Se establece un bucle *while* que se ejecutará mientras la variable *game_is_running* = True, esta variable controla si el jeugo está en ejecución o no, y es declarada por defecto como True."""
        while self.game_is_running:
            self.timer = "{:.5f}".format(time.time() - start_time)
            
            mouse_x, mouse_y = pygame.mouse.get_pos()
            moves.update_mouse_position(mouse_x, mouse_y)


            """En este bucle se recorren todos los eventos de la cola de eventos de Pygame. 
            Esto permite manejar eventos de teclado, mouse y otros eventos relacionados con la ventana del juego."""
            for event in pygame.event.get():
                
                """En este bloque de código se verifica si el evento actual es el cierre de la ventana del juego. 
                Si es así, se llama a la función pygame.quit() para salir de Pygame y se llama a quit() para salir del programa por completo.
                """
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
                # """En este bloque de código se verifica si el evento actual es un click del botón del mouse. 
                # Si es así, se llaman a dos funciones: clicked_new_card(x, y) y check_holding_card(x, y)."""
                # if event.type == pygame.MOUSEBUTTONDOWN:
                #     moves.clicked_new_card(self)
                #     moves.check_holding_card(self)

                # """En este bloque de código se verifica si el evento actual es la desclick del botón del mouse. 
                # Si *self.holding_cards* no está vacía, se llama a la función place_card(x, y), se establece *self.holding_cards* como una lista vacía y se llama a la función waste.set_cards()."""
                # if event.type == pygame.MOUSEBUTTONUP:
                #     if self.holding_cards != []:
                #         moves.place_card(self)
                #         self.holding_cards = []
                #         self.waste.set_cards()

            """En esta línea se dibuja la imagen de fondo en la ventana del juego. self.self.backgroundImage es una imagen cargada anteriormente. (detrás de todo)"""
            self.screen.blit(self.backgroundImage, (0, 0))
            
            """En este bloque de código se dibujan todas las cartas en las *tables* del juego. 
            Se recorre cada *table* en la lista *tables*, y para cada *table* se recorre su lista de cartas y se dibujan todas las cartas que no están en *self.holding_cards*.
            
            El bucle FOR recorre cada pila de mesas (table) y llama al método get_table() para obtener la lista de cartas de cada pila.
            Luego, se verifica si la carta no se está sosteniendo con el cursor (not card in self.holding_cards).
            Si es así, la carta se dibuja en la pantalla usando el método draw() de pygame.sprite.GroupSingle."""
            for table in self.tables:
                for card in table.get_table():
                    if not card in self.holding_cards:
                        pygame.sprite.GroupSingle(card).draw(self.screen)

            """El bucle FOR recorre cada pila de base (foundation) y llama al método get_top_card() para obtener la carta en la cima de cada pila. 
            Luego, se verifica si la carta no se está sosteniendo con el cursor (not card in self.holding_cards). 
            Si es así, la carta se dibuja en la pantalla usando el método draw() de pygame.sprite.GroupSingle."""
            for foundation in self.foundations:
                card = foundation.get_top_card()
                if not card in self.holding_cards:
                    pygame.sprite.GroupSingle(card).draw(self.screen)

            """El bucle FOR recorre cada carta en la pila de descarte (waste) llamando al método get_show_waste_pile(). 
            Luego, se verifica si la carta no se está sosteniendo con el mouse (not card in holding_cards). 
            Si es así, la carta se dibuja en la pantalla usando el método draw() de pygame.sprite.GroupSingle."""
            for card in self.waste.get_show_waste_pile():
                if not card in self.holding_cards:
                    pygame.sprite.GroupSingle(card).draw(self.screen)

            # """Función que dibuja cualquier carta que se esté sosteniendo con el ratón en la posición actual del ratón."""
            # moves.card_follow_mouse(self)

            """Se llama a la función message_display() tres veces para mostrar el temporizador, la puntuación y el número de movimientos en la parte superior de la pantalla."""
            self.message_display(str(self.timer), (639, 39))
            self.message_display(str(self.moves), (853, 39))
            
            """Función que limita la velocidad del juego a 60 fotogramas por segundo."""
            self.clock.tick(120)
            
            Strategies = {
                1 : (elmarino.UnderTaker, "El Marino"),
                2 : (lasocialista.Gestionadora, "La Socialista"),
                3 : (elbombero.ApagaLlamas, "El Bombero"),
                4 : (elgobernador.Progresismo, "El Gobernador")
            }
            
            """Bucle que se ejecuta según la estratégia."""
            for key, value in Strategies.items():
                if self.idEstrategia == key:
                    value[0](self, moves)
                    self.message_display(value[1], (490, 14))
                    break

            self.results = self.game_result()
            """Función que actualiza la pantalla con los cambios realizados."""
            pygame.display.update()

    """Función que devuelve los resultados al terminar el juego."""
    def game_result(self):
        if self.check_all_cards_face_up():
            results = {
                "idGames": None,
                "victoria": True,
                "duracion": self.timer,
                "movimientos": self.moves,
                "mazo" : self.full_deck,
                "idEstrategia": self.idEstrategia
            }
            self.game_is_running = False

            return results
        
        
        elif self.result_counter == 5:
            """Condición de juego perdido (que se haya buscado 24 veces en el mazo de manera seguida sin hacer otro movimiento)."""
            results = {
                "idGames": None,
                "victoria": False,
                "duracion": self.timer,
                "movimientos": self.moves,
                "mazo" : self.full_deck,
                "idEstrategia": self.idEstrategia
            }
            self.game_is_running = False
            return results
    
    """Funcion que verifica que todas las cartas del juego esten dadas vueltas, condición de juego ganado."""
    def check_all_cards_face_up(self):
        for table in self.tables:
            table_cards = table.get_table()
            for card in table_cards:
                if not card.is_front_showing():
                    return False
        self.count_remaining_moves()
        return True
    
    """Función que cuenta los movimientos restantes al ganar la partida."""
    def count_remaining_moves(self):

        for _ in self.waste.get_waste_pile():
            self.moves += 1
            
        for _ in self.deck.get_deck():
            self.moves += 1
            
        for table in self.tables:
            for _ in table.get_table():
                self.moves += 1

        return self.moves