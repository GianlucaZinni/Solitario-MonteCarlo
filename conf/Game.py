import pygame, time, sys
from conf.Waste import Waste
from conf.Foundation import Foundation
from conf.Table import Table
from pygame.locals import RESIZABLE
from func.Movement import BasicMoves
from func.Strategies import ElMarino, LaSocialista, ElBombero

class Game:
    def __init__(self, ejecucion, idEstrategia, deck):
        pygame.init()
        pygame.display.set_caption("Partida: " + str(ejecucion) + " / Estrategia: " + str(idEstrategia) + " / Solitario")

        # Identificador de la estrategia del juego
        self.idEstrategia = idEstrategia

        # Configuración de la pantalla
        self.window_size = (900, 885)
        self.screen = pygame.display.set_mode(self.window_size, RESIZABLE)
        self.backgroundImage = pygame.image.load("static/assets/layout/backgroundd.jpg")

        # Booleano para controlar el loop principal
        self.game_is_running = True

        # Variables para generar el mazo y el reloj
        self.deck = deck

        self.waste = Waste()
        self.clock = pygame.time.Clock()
        
        # Variable que almacena el mazo utilizado en la partida
        self.full_deck = self.deck.insert_all_cards()

        # Variables para el movimiento de las cartas
        self.holding_cards = []
        self.holding_card_group = None
        self.mouse_cords = ()

        # Variables contabilizadoras
        self.moves = 0
        self.timer = 0

        # Variables para generar el tablero
        self.tables = self.create_tables()
        self.foundations = self.create_foundations()

        # Variables para finalizar la partida
        self.check_if_lock = []
        self.result_counter = 0
        self.results = None

    def create_tables(self):
        tables = []
        x = 25
        for card_amount in range(1, 8):
            tables.append(Table(x, self.deck, card_amount))
            x += 125
            card_amount += 1
        return tables

    def create_foundations(self):
        foundations = []
        x = 400
        suits = ["hearts", "diamonds", "spades", "clubs"]

        for i in range(len(suits)):
            foundations.append(Foundation(x, suits[i]))
            x += 125
        return foundations

    def message_display(self, text, cords):
        large_text = pygame.font.Font("static/assets/fonts/Roboto-Bold.ttf", 17)
        text_surface = large_text.render(text, True, (255, 255, 255))
        TextSurf, TextRect = text_surface, text_surface.get_rect()
        TextRect.center = cords
        self.screen.blit(TextSurf, TextRect)

    def game_loop(self):
        start_time = time.time()
        moves = BasicMoves()
        
        elmarino = ElMarino()
        lasocialista = LaSocialista()
        elbombero = ElBombero()

        while self.game_is_running:
            self.timer = int(time.time() - start_time)
            mouse_x, mouse_y = pygame.mouse.get_pos()
            moves.update_mouse_position(mouse_x, mouse_y)

            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    moves.clicked_new_card(self)
                    moves.check_holding_card(self)

                if event.type == pygame.MOUSEBUTTONUP:
                    if self.holding_cards != []:
                        moves.place_card(self)
                        self.holding_cards = []
                        self.waste.set_cards()

            self.screen.blit(self.backgroundImage, (0, 0))

            for table in self.tables:
                for card in table.get_table():
                    if not card in self.holding_cards:
                        pygame.sprite.GroupSingle(card).draw(self.screen)

            for foundation in self.foundations:
                card = foundation.get_top_card()
                if not card in self.holding_cards:
                    pygame.sprite.GroupSingle(card).draw(self.screen)

            for card in self.waste.get_show_waste_pile():
                if not card in self.holding_cards:
                    pygame.sprite.GroupSingle(card).draw(self.screen)

            moves.card_follow_mouse(self)

            self.message_display(str(self.timer), (639, 39))
            self.message_display(str(self.moves), (853, 39))
            
            self.clock.tick(120)
            
            Strategies = {
                1 : (elmarino.UnderTaker, "El Marino"),
                2 : (lasocialista.Gestionadora, "La Socialista"),
                3 : (elbombero.ApagaLlamas, "El Bombero" )
            }
            
            for key, value in Strategies.items():
                if self.idEstrategia == key:
                    value[0](self, moves)
                    self.message_display(value[1], (490, 14))
                    break

            pygame.display.update()
            self.results = self.game_result()

    def game_result(self):
        if self.check_all_cards_face_up():
            results = {
                "idGames": None,
                "victoria": True,
                "duracion": f"{self.timer} segundos",
                "movimientos": self.moves,
                "mazo" : self.full_deck,
                "idEstrategia": self.idEstrategia
            }
            self.game_is_running = False

            return results
        
        elif self.result_counter == 5:
            results = {
                "idGames": None,
                "victoria": False,
                "duracion": f"{self.timer} segundos",
                "movimientos": self.moves,
                "mazo" : self.full_deck,
                "idEstrategia": self.idEstrategia
            }
            self.game_is_running = False
            return results
        
    def check_all_cards_face_up(self):
        for table in self.tables:
            table_cards = table.get_table()
            for card in table_cards:
                if not card.is_front_showing():
                    return False
        self.count_remaining_moves()
        return True
    
    def count_remaining_moves(self):

        for _ in self.waste.get_waste_pile():
            self.moves += 1
            
        for _ in self.deck.get_deck():
            self.moves += 1
            
        for table in self.tables:
            for _ in table.get_table():
                self.moves += 1
                
        print(self.moves)
        return self.moves