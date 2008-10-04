# -*- coding: utf-8 -*-

"""
File        :   interface.py
Description :   Manages the displays and main loop.
"""

import pygame   # http://www.pygame.org
import init     # ./init.py
import sys      # standard python library
import math     # standard python library

#   Settings

global screen       # Screen object - Objet écran
global is_running   # Indicates whether the simulation is running - Indique si la simulation tourne
global debug        # Indicates whether debugging messages are displayed - Indique si les messages de débogage sont affichés

screen = pygame.display.set_mode(init.RESOLUTION)   # Sets drawing surface - Met en place la surface de dessin
debug  = True

def init_display():
    pygame.init()
    pygame.display.set_caption("Thereisnorush (unstable)")

def draw_node(node):
    """
    Draws a given node on the screen.
        node (Node) : the aforementioned node.
    
    Dessine un carrefour donné à l'écran.
        node (Node) : le carrefour sus-cité.
    """
    
    # TODO :
    #       · (DN1) draw the cars on the node, or alter the node drawing procedure to show there are cars, whatever
   
    pygame.draw.circle(screen, init.NODE_COLOR, (int(node.x), int(node.y)), init.NODE_WIDTH)
    
    if node.cars:
        # There are cars on the node, we may want to draw them
        # albeit we can't use draw_car here…
        pass 
    
def draw_car(car):
    """
    Draws a given car on the screen.
        car (Car) : the aforementioned car.
    
    Dessine une voiture donnée à l'écran.
        car (Car) : la voiture sus-citée.
    """
    
    xd, yd = car.road.begin.coords
    xa, ya = car.road.end.coords

    length_covered = int(car.position) * 100 / int(car.road.length)
    
    x_position = int(xd) + (int(xa) - int(xd) ) * length_covered / 100
    y_position = int(yd) + (int(ya) - int(yd) ) * length_covered / 100
    
    pt_topleft     = (x_position - init.CAR_WIDTH / 2 , y_position - init.CAR_HEIGHT / 2 )
    pt_bottomright = (init.CAR_WIDTH, init.CAR_HEIGHT)
    
    rectangle      = pygame.Rect(pt_topleft, pt_bottomright)
    pygame.draw.rect(screen, init.CAR_COLOR, rectangle, 0)

def draw_arrow(x_start, y_start, x_end, y_end):
    """
    Draws lil' cuty arrows along the roads to know where they're going
    """
    
    # Get the vector parallel to the road
    para_y = y_end - y_start
    para_x = x_end - x_start
    para_len = math.sqrt(para_x**2 + para_y**2)
    
    # Normalize it
    para_x = para_x / para_len
    para_y = para_y / para_len
    
    # Get the vector perpendicular to the road (CCW)
    perp_x = -para_y
    perp_y = para_x
    
    # Get the midpoint of the road
    mid_x = (x_start + x_end)/2
    mid_y = (y_start + y_end)/2
    
    # Draw an arrow on the left side!
    x_arrow_start = mid_x - perp_x * 4 - para_x * 4
    y_arrow_start = mid_y - perp_y * 4 - para_y * 4
    
    x_arrow_end = mid_x - perp_x * 4 + para_x * 4 
    y_arrow_end = mid_y - perp_y * 4 + para_y * 4
    
    pygame.draw.line(screen, init.ROAD_COLOR, (x_arrow_start, y_arrow_start), (x_arrow_end, y_arrow_end), 1)
    pygame.draw.line(screen, init.ROAD_COLOR, (x_arrow_end - perp_x - para_x, y_arrow_end - perp_y - para_y), (x_arrow_end + perp_x - para_x, y_arrow_end + perp_y - para_y), 1)
    
def draw_road(road):
    """
    Draws a given road on the screen and all the cars on it.
        road (Road) : the aforementioned road.
            
    Dessine une route donnée à l'écran et toutes les voitures dessus.
        road (Road) : la route sus-citée.
    """
    
    x_start = int(road.begin.x)
    y_start = int(road.begin.y)
    x_end = int(road.end.x)
    y_end = int(road.end.y)
    
    pygame.draw.line(screen, init.ROAD_COLOR, (x_start, y_start), (x_end, y_end), 1)
    
    # Draw an arrow pointing at where we go
    draw_arrow(x_start, y_start, x_end, y_end)
    
    for car in road.cars:
        draw_car(car)
    
def draw_scene():
    """
    Draws the complete scene on the screen.
    Dessine la scène entière à l'écran.
    """
    
    screen.fill(init.BLACK)
    
    for road in init.track.roads:
        draw_road(road)
    for node in init.track.nodes:
        draw_node(node)
    
    pygame.display.flip()
    pygame.display.update()
    
    
def halt():
    """
    Closes properly the simulation.
    Quitte correctement la simulation.
    """
    
    # TODO :
    #       · (H1) try to avoid "pygame.error: display Surface quit" on exit, by exiting the main loop first
    
    is_running = False
    pygame.quit()
  
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
        elif (event.type == pygame.MOUSEBUTTONUP):
            left_button, right_button, middle_button = pygame.mouse.get_pressed()
            x, y = pygame.mouse.get_pos()
        
        #   Keyboard button
        elif (event.type == pygame.KEYDOWN):
            keyb_state = pygame.key.get_pressed()
            
            if keyb_state[pygame.K_ESCAPE]:
                halt()
        else:
            pass

def update_scene():
    for road in init.track.roads:
        road.update()
    for node in init.track.nodes:
        node.update()

def main_loop():
    """
    Main loop : keeps updating and displaying the scene forever,
                unless somebody hits Esc.
    
    Boucle principale : met à jour et affiche la scène pour toujours,
                        jusqu'à ce que quelqu'un appuye sur Esc.
    """
    
    is_running = True

    while is_running:
        # Check the users' actions | Vérifie les actions de l'utilisateur
        event_manager()
        
        # Updates the scene | Met à jour la scène
        update_scene()
        
        # Draw the scene | Dessine la scène
        draw_scene()

    # End of simulation instructions
    # Instructions de fin de simulation
    halt()
    
# Bootstrap

if __name__ == "__main__":
    # Before simulation instructions
    init_display()
    # Main loop
    main_loop()

# Don't write anything after that !
