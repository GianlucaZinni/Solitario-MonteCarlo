import pygame
from Deck import Deck
from Waste import Waste
from Foundation import Foundation
from Table import Table
import time

pygame.init()
window_size = (900, 885)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Solitario")
game_is_running = True

backgroundImage = pygame.image.load("D:/My Drive/Universidad/CUARTO AÑO/Modelos y Simulación/Método de Montecarlo/Montecarlo/Solitario-Montecarlo/assets/backgroundd.jpg")
# http://byronknoll.blogspot.com/2011/03/vector-playing-cards.html

deck = Deck()
deck.shuffle()

waste = Waste()

clock = pygame.time.Clock()

holding_cards = []
holding_card_group = None
mouse_cords = ()

moves = 0
score = 0
frame = 0
timer = 0

place_sound = pygame.mixer.Sound('D:/My Drive/Universidad/CUARTO AÑO/Modelos y Simulación/Método de Montecarlo/Montecarlo/Solitario-Montecarlo/assets/flip.wav')
shuffle_sound = pygame.mixer.Sound('D:/My Drive/Universidad/CUARTO AÑO/Modelos y Simulación/Método de Montecarlo/Montecarlo/Solitario-Montecarlo/assets/shuffle.wav')
shuffle_sound.play()


def clicked_new_card(mouse_x, mouse_y):
    global moves
    if mouse_x > 9 and mouse_x < 106 and mouse_y > 14 and mouse_y < 155:
        if len(deck.get_deck()) <= 0:
            deck.add_cards(list(reversed(waste.get_waste_pile().copy())))
            waste.empty()
            shuffle_sound.play()
        else:
            moves += 1
            waste.add_card(deck.remove_card())
            place_sound.play()

def check_holding_card(mouse_x, mouse_y):
    global holding_card_group, holding_cards, mouse_cords
    possible_cards = []

    mouse_cords = (mouse_x, mouse_y)

    for table in tables:
        for table_card in table.get_table():
            if table_card.is_front_showing():
                possible_cards.append((table_card, table))

    for foundation in foundations:
        foundation_card = foundation.get_top_card()
        if foundation_card!=None:
            possible_cards.append((foundation_card, foundation))

    waste_card = waste.get_top_card()
    if waste_card!=None:
        possible_cards.append((waste_card, waste))

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

def card_follow_mouse(mouse_x, mouse_y):
    if holding_cards != []:
        #card_cords = holding_card.get_coordinates()
        #dif1 = mouse_x - card_cords[0]
        #dif2 = mouse_y - card_cords[1]
        x=mouse_x - 50
        y=mouse_y - 50
        pos = 0
        for card in holding_cards:
            card.set_coordinates(x, y + (pos * 40))
            pygame.sprite.GroupSingle(card).draw(screen)
            pos += 1

def create_tables():
    tables = []
    x = 25
    card_amount = 1
    for i in range(0, 7):
        tables.append(Table(x, deck, card_amount))
        x += 125
        card_amount += 1
    return tables

def create_foundations():
    foundations = []
    x = 400
    suits = ["hearts", "diamonds", "spades", "clubs"]
    for i in range(0, 4):
        foundations.append(Foundation(x, suits[i]))
        x += 125
    return foundations

tables = create_tables()
foundations = create_foundations()

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