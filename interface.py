#!/usr/local/bin/python
# -*- coding: utf-8 -*-

################################################################################
#
# File          :   interface.py
# Description   :   
#
# ToDo          :   ·
#              
################################################################################

import pygame   # http://www.pygame.org
import init     # ./init.py
import sys      # standard python library

#   Settings

global screen                                # Screen object - Objet écran
global isRunning                           # Indicates whether the simulation is running - Indique si la simulation tourne
global debug                                 # Indicates whether debugging messages are displayed - Indique si les messages de débogage sont affichés

clock  = pygame.time.Clock()                 # Clock object to control fps - Objet horloge pour controler les fps
screen = pygame.display.set_mode((320, 240))       # Sets drawing surface - Met en place la surface de dessin
debug  = True

def init_display():
    pygame.init()                                             # Pygame initialization - Initialisation de pygame
    pygame.display.set_caption("Thereisnorush (unstable)")    # Sets window caption - Définit le titre de la fenêtre

def drawNode(node):
    """
        Draws a given node on the screen.
            node (Node) : the aforementioned node.
    
        Dessine un carrefour donné à l'écran.
            node (Node) : le carrefour sus-cité.
    """
    
    rectangle = pygame.Rect(node.x - init.NODE_WIDTH/2, node.y - init.NODE_HEIGHT/2, init.NODE_WIDTH, init.NODE_HEIGHT)
    pygame.draw.rect(screen, init.NODE_COLOR, rectangle, 0)

def drawCar(car):
    """
        Draws a given car on the screen.
            car (Car) : the aforementioned car.
    
        Dessine une voiture donnée à l'écran.
            car (Car) : la voiture sus-citée.
    """
    
    xd, yd = car.road.begin.getCoordinates() # i like this OO call !
    xa, ya = car.road.end.getCoordinates()

    length_covered = car.position * 100 / car.road.length
    
    x_position = xd + (xa - xd ) * length_covered / 100
    y_position = yd + (ya - yd ) * length_covered / 100
    
    pt_topleft     = (x_position - init.CAR_WIDTH / 2 , y_position - init.CAR_HEIGHT / 2 )
    pt_bottomright = (init.CAR_WIDTH, init.CAR_HEIGHT)
    
    rectangle      = pygame.Rect(pt_topleft, pt_bottomright)
    pygame.draw.rect(screen, init.CAR_COLOR, rectangle, 0)

def drawRoad(road):
    """
        Draws a given road on the screen and all the cars on it.
            road (Road) : the aforementioned road.
            
        Dessine une route donnée à l'écran et toutes les voitures dessus.
            road (Road) : la route sus-citée.
    """
    
    pygame.draw.line(screen, init.ROAD_COLOR, (road.begin.x, road.begin.y), (road.end.x, road.end.y), 1)
    
    for car in road.cars:
        drawCar(car)
    
def draw_scene():
    """
        Draws the complete scene on the screen.
        Dessine la scène entière à l'écran.
    """
    
    screen.fill(init.BLACK)
    
    for node in init.track.nodes:
        drawNode(node)
    for road in init.track.roads:
        drawRoad(road)
    
    pygame.display.flip()
    pygame.display.update()
    
def halt():
    """
        Closes properly the simulation.
        Quitte correctement la simulation.
    """
    
    isRunning = False
    pygame.quit()
    #sys.exit()  
  
def event_manager():
    """
        Checks for users' actions and call appropriate methods.
        Vérifie les actions de l'utilisateur et réagit en conséquence.
    """
    
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            halt()
    
#   Mouse button
    
        elif (event.type == pygame.MOUSEBUTTONDOWN):
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
    
#   Keyboard button
    
        elif (event.type == pygame.KEYDOWN):
            keyb_state = pygame.key.get_pressed()
            
            #debugging code
            print "KEY", keyb_state
            
            if keyb_state[pygame.K_ESCAPE]:
                halt()
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

    isRunning = True

    while isRunning:
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
        except Exception, exc:
            # There some error: stop everything
            # Il y a une erreur quelconque : on arrête tout
            print exc
            isRunning = False
            
        pass

    # End of simulation instructions
    # Instructions de fin de simulation
    pass
    halt()
    
# Bootstrap

if (__name__ == "__main__"):
    # Before simulation instructions
    pass
    init_display()
    # Main loop
    main_loop()

# Don't write anything after that !
