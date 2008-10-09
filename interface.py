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
    
    xd, yd = car.location.begin.coords
    xa, ya = car.location.end.coords
    
    para_x, para_y, perp_x, perp_y = car.location.get_vectors
    length_covered = float(int(car.position)) / float(int(car.location.length))
    
    # EXPERIMENTAL: draw the cars at a scale consistent with the road
    #scale_factor = car.location.length / math.sqrt((xa-xd)**2 + (ya-yd)**2)
    scale_factor = 1
    
    # Coordinates for the center
    cx, cy = xd + length_covered * (xa - xd), yd + length_covered * (ya - yd)
    
    # Relative size of the car
    r_width = car.width * scale_factor
    r_length = car.length * scale_factor
    
    # Get the coordinates for the endpoints
    # ToDo : use relative sizes to respect the roads' scales
    x1, y1 = cx - para_x * r_length/2 - perp_x * r_width/2, cy - para_y * r_length/2 - perp_y * r_width/2
    x2, y2 = cx + para_x * r_length/2 - perp_x * r_width/2, cy + para_y * r_length/2 - perp_y * r_width/2
    x3, y3 = cx + para_x * r_length/2 + perp_x * r_width/2, cy + para_y * r_length/2 + perp_y * r_width/2
    x4, y4 = cx - para_x * r_length/2 + perp_x * r_width/2, cy - para_y * r_length/2 + perp_y * r_width/2
    
    # Change the color in case the car is waiting    
    color = car.color
    if car.waiting:
        color = init.GRAY

    # Draw the car 
    pygame.draw.polygon(screen, color, ((x1, y1), (x2, y2), (x3, y3), (x4, y4)), 0)

def draw_text(x = screen.get_rect().centerx, y = screen.get_rect().centery, message = "", text_color = init.WHITE, back_color = init.BLACK, font = None, anti_aliasing = True):
    """
    Draws text on the screen
        x, y    (int)        :   position where the text is to be written
        message (str)        :   the message that is to be written
        text_color (list)    :   the color of the text to be written
        back_color (list)    :   the color on which the text is to be written
        font (pygame.font)   :   the font that will be used for the text to be written
        anti_aliasing (bool) :   whether we should antialias the text to be written
    """
    if not pygame.font:
        # The (optional) pygame.font module is not supported, we cannot draw text
        print "ERROR : the pygame.font module is not supported, cannot draw text."
    else:
        if not font:
            # We use a default font if none is provided
            font = pygame.font.Font(None, 17)
            
        text = font.render(message, anti_aliasing, text_color, back_color)
        textRect = text.get_rect()
        textRect.x, textRect.y = x, y
        screen.blit(text, textRect)
        
def draw_arrow(road):
    """
    Draws lil' cuty arrows along the roads to know where they're going
    """
    
    para_x, para_y, perp_x, perp_y = road.get_vectors
    
    x_start, y_start = road.begin.coords
    x_end, y_end     = road.end.coords

    # Get the midpoint of the road
    mid_x, mid_y = (x_start + x_end)/2, (y_start + y_end)/2
    
    # Draw an arrow on the left side!
    x_arrow_start, y_arrow_start = mid_x - perp_x * 4 - para_x * 4, mid_y - perp_y * 4 - para_y * 4
    x_arrow_end, y_arrow_end     = mid_x - perp_x * 4 + para_x * 4, mid_y - perp_y * 4 + para_y * 4
    
    pygame.draw.line(screen, init.ROAD_COLOR, (x_arrow_start, y_arrow_start), (x_arrow_end, y_arrow_end), 1)
    pygame.draw.line(screen, init.ROAD_COLOR, (x_arrow_end - perp_x - para_x, y_arrow_end - perp_y - para_y), (x_arrow_end + perp_x - para_x, y_arrow_end + perp_y - para_y), 1)

def draw_traffic_light(x, y, state):
    """
    Draws a traffic light…
        x, y : coordinates
        state : (True, False)
    """
    
    TF_RADIUS = 2
    
    for i in range(3):
        if (state) and (i == 2):
            pygame.draw.circle(screen, init.LIGHT_GREEN, [x, y + TF_RADIUS * i * 2], TF_RADIUS, 0)
        elif (not state) and (i == 0):
            pygame.draw.circle(screen, init.LIGHT_RED, [x, y + TF_RADIUS * i * 2], TF_RADIUS, 0)
        pygame.draw.circle(screen, init.GRAY, [x, y + TF_RADIUS * i * 2], TF_RADIUS, 1)

def draw_road(road):
    """
    Draws a given road on the screen and all the cars on it.
        road (Road) : the aforementioned road.
            
    Dessine une route donnée à l'écran et toutes les voitures dessus.
        road (Road) : la route sus-citée.
    """
    
    x_start, y_start = int(road.begin.x), int(road.begin.y)
    x_end, y_end     = int(road.end.x), int(road.end.y)
   
    # This is not perfect… but it's ok for now I guess -- Sharayanan
    #draw_traffic_light(x_start + 4, y_start + 4, road.gates[0])
    draw_traffic_light(x_end - 4, y_end + 4, road.gates[1])
   
    # EXPERIMENTAL: color the road from green (empty) to red (full)
    # Model : color key proportional to traffic density (N_cars/L_road)
    if road.cars:
        occupation = 0
        for car in road.cars:
            occupation += car.length
            
        key = 2 * (float(occupation)/float(road.length)) * 255
        if key > 255: key = 255
        color = [key, 255 - key, 0]
    else:
        #color = init.ROAD_COLOR
        color = init.GREEN
    
    #pygame.draw.line(screen, init.ROAD_COLOR, (x_start, y_start), (x_end, y_end), 1)
    
    pygame.draw.line(screen, color, (x_start, y_start), (x_end, y_end), 1) # EXPERIMENTAL
    
    # Draw an arrow pointing at where we go
    draw_arrow(road)
    
    if road.cars:
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
    
    #   PLEASE STOP MAKING FUNCTIONS THAT DO ONLY 2 INSTRUCTIONS -- Ch@hine
    # Please don't *shout*, this is not a function, and this is required here -- Sharayanan
    pygame.init()
    pygame.display.set_caption("Thereisnorush (unstable)")
    
    # Main loop
    main_loop()

# Don't write anything after that !