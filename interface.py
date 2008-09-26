#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import pygame   # http://www.pygame.org
import init     # ./init.py
import sys      # standard python library

# Colors

black = (  0,   0,   0)
red   = (255,   0,   0)
green = (  0, 255,   0)
blue  = (  0,   0, 255)
white = (255, 255, 255)

light_red   = (255,  64,  64)
light_green = ( 64, 255,  64)
light_blue  = ( 64,  64, 255)

# Settings

size = width, height = (320, 240)            # Screen resolution - Résolution de l'affichage

global screen                                # Screen object - Objet écran
global sim_running                           # Indicates whether the simulation is running - Indique si la simulation tourne
global debug                                 # Indicates whether debugging messages are displayed - Indique si les messages de débogage sont affichés

clock  = pygame.time.Clock()                 # Clock object to control fps - Objet horloge pour controler les fps
screen = pygame.display.set_mode(size)       # Sets drawing surface - Met en place la surface de dessin
debug  = True

# Node general properties
# Propriétés générales d'un carrefour
node_width  = 4
node_height = 4
node_color = red

# Car general properties
# Propriétés générales d'une voiture
car_width  = 4
car_height = 4
car_color = green

# Road general properties
# Propriétés générales d'une route
road_color = white

def init_display():
    pygame.init()                                             # Pygame initialization - Initialisation de pygame
    pygame.display.set_caption("Thereisnorush (unstable)")    # Sets window caption - Définit le titre de la fenêtre

def draw_node(node):
    """
    Draws a given node on the screen.
        node (node) : the aforementioned node.

    Dessine un carrefour donné à l'écran.
        node (node) : le carrefour sus-cité.
    """
    pt_topleft     = (node.x - node_width / 2 , node.y - node_height / 2 )
    pt_bottomright = (node_width, node_height)
    rectangle      = pygame.Rect(pt_topleft, pt_bottomright)
    pygame.draw.rect(screen, node_color, rectangle, 0)

def draw_car(car):
    """
    Draws a given car on the screen.
        car (car) : the aforementioned car.

    Dessine une voiture donnée à l'écran.
        car (car) : la voiture sus-citée.
    """
    
    xd, yd = car.road.begin.coords() # i like this OO call !
    xa, ya = car.road.end.coords()

    length_covered = car.pos * 100 / car.road.length
    x_position = xd + (xa - xd ) * length_covered / 100
    y_position = yd + (ya - yd ) * length_covered / 100
    pt_topleft     = (x_position - car_width / 2 , y_position - car_height / 2 )
    pt_bottomright = (car_width, car_height)
    rectangle      = pygame.Rect(pt_topleft, pt_bottomright)
    pygame.draw.rect(screen, car_color, rectangle, 0)

def draw_road(road):
    """
    Draws a given road on the screen and all the cars on it.
        road (road) : the aforementioned road.

    Dessine une route donnée à l'écran et toutes les voitures dessus.
        road (road) : la route sus-citée.
    """
    pt_topleft     = (road.begin.x, road.begin.y)
    pt_bottomright = (road.end.x,   road.end.y)
    rectangle      = pygame.Rect(pt_topleft, pt_bottomright)
    pygame.draw.line(screen, road_color, pt_topleft, pt_bottomright, 1)
    
    for car in road.cars: draw_car(car)
    
def draw_scene():
    """
    Draws the complete scene on the screen.
    Dessine la scène entière à l'écran.
    """
    # Clear background - Nettoie l'arrière-plan
    screen.fill(black)

    # First, draw the nodes, then draw the roads, with the cars on them
    # D'abord, dessine les carrefours, puis les routes avec les voitures dessus
    for node in init.circuit.nodes: draw_node(node)
    for road in init.circuit.roads: draw_road(road)
    # Saves and displays
    # Valide et affiche
    pygame.display.flip()
    pygame.display.update()
    
def exit_program():
    """
    Closes properly the simulation.
    Quitte correctement la simulation.
    """
    sim_running = False
    pygame.quit()
    #sys.exit()  
  
def event_manager():
    """
    Checks for users' actions and call appropriate methods.
    Vérifie les actions de l'utilisateur et réagit en conséquence.
    """
    
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            # The user wants to leave
            # L'utilisateur veut quitter
            exit_program()
        elif (event.type == pygame.MOUSEBUTTONDOWN):
            # The user is clicking somewhere or using the mousewheel
            # L'utilisateur clique ou utilise la molette
            left_button, right_button, middle_button = pygame.mouse.get_pressed()
            x, y = pygame.mouse.get_pos()
            
            #debugging code
            print "MD", x, y, left_button, right_button, middle_button
            
            # The next line will be implemented when the GUI code is written : do not delete please
            # call tinr_gui.mouse_down(x, y, [left_button, right_button, middle_button]
        elif (event.type == pygame.MOUSEBUTTONUP):
            # The user is releasing the buttons
            left_button, right_button, middle_button = pygame.mouse.get_pressed()
            x, y = pygame.mouse.get_pos()
            
            #debugging code
            print "MU", x, y, left_button, right_button, middle_button
            
            # The next line will be implemented when the GUI code is written : do not delete please
            # call tinr_gui.mouse_up(x, y, [left_button, right_button, middle_button]
        elif (event.type == pygame.KEYDOWN):
            # The user pressed a key
            # L'utilisateur a appuyé sur une touche
            keyb_state = pygame.key.get_pressed()

            #debugging code
            print "KEY", keyb_state

            if keyb_state[pygame.K_ESCAPE]:
                # The user wants to escape!
                # L'utilisateur veut s'échapper !
                exit_program()
        else:
            pass

def main_loop():
    """
    Main loop : keeps updating and displaying the scene forever,
                unless somebody hits Esc.

    Boucle principale : met à jour et affiche la scène pour toujours,
                        jusqu'à ce que quelqu'un appuye sur Esc.
    """
    # Main loop

    sim_running = True

    while sim_running:
        # Ensure that we won't update more often than 60 times per second
        # S'assure qu'on ne dépassera pas 60 images par secondes
        clock.tick(60)
        
        # Check the users' actions
        # Vérifie les actions de l'utilisateur
        event_manager()

        pass
        
        # Draw the scene
        # Dessine la scène
        try:
            # Snafu
            # Situation normale
            draw_scene()
        except:
            # There some error: stop everything
            # Il y a une erreur quelconque : on arrête tout
            sim_running = False

        pass

    # End of simulation instructions
    # Instructions de fin de simulation
    pass
    exit_program()
    
# Bootstrap

if (__name__ == "__main__"):
    # Before simulation instructions
    pass
    init_display()
    # Main loop
    main_loop()

# Don't write anything after that !
