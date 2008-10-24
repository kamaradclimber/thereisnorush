# -*- coding: utf-8 -*-
"""
File        :   interface.py
Description :   Manages the displays and main loop.
"""

import constants
import init     # ./init.py
import pygame   # http://www.pygame.org
from vector import Vector

screen = pygame.display.set_mode(constants.RESOLUTION)

def draw_roundabout(roundabout):
    """
    Draws a given roundabout on the screen.
        roundabout (Roundabout) : the aforementioned roundabout.
    
    Dessine un carrefour donné à l'écran.
        roundabout (Roundabout) : le carrefour sus-cité.
    """
    # TODO :
    #       · (DN1) draw the cars on the roundabout
    
    pygame.draw.circle(screen, constants.ROUNDABOUT_COLOR, roundabout.position.ceil().get_tuple(), constants.ROUNDABOUT_WIDTH)
    
    # Roundabouts should be drawn as rotating crossroads, in order to draw the cars that rotate in ; the problem is that roads must not be drawn from the center of the roundabout anymore
    #pygame.draw.circle(screen, constants.ROUNDABOUT_COLOR, roundabout.position.ceil().get_tuple(), constants.ROUNDABOUT_WIDTH * 4, 1)
    
    if roundabout.cars:
        # There are cars on the roundabout, we may want to draw them
        # albeit we can't use draw_car here...
        
        #TEMPORARY : the number of cars on the roundabout is written
        position = Vector(roundabout.position.x + 10, roundabout.position.y + 10)
        draw_text(position, str(len(roundabout.cars)))
        pass

def draw_car(car):
    """
    Draws a given car on the screen.
        car (Car) : the aforementioned car.
    
    Dessine une voiture donnée à l'écran.
        car (Car) : la voiture sus-citée.
    """
    d_position = car.location.begin.position
    a_position = car.location.end.position
    direction  = (a_position - d_position)
    
    length_covered = float(int(car.position)) / float(int(car.location.length))
    
    # Get them once
    (r_width, r_length) = (car.width, car.length)

    # Get the appropriate vectors once
    (parallel, orthogonal) = car.location.reference

    # Coordinates for the center
    center_position = d_position + direction * length_covered + orthogonal * car.location.width/2
    
    position1 = center_position - parallel * r_length/2 - orthogonal * r_width/2
    position2 = center_position + parallel * r_length/2 - orthogonal * r_width/2
    position3 = center_position + parallel * r_length/2 + orthogonal * r_width/2
    position4 = center_position - parallel * r_length/2 + orthogonal * r_width/2
    
    # Change the color in case the car is waiting    
    color = car.color
    if car.waiting:
        color = constants.RED

    # EXPERIMENTAL
    if car.sight_distance > 1:
        #pygame.draw.circle(screen, color, center_position.get_list(), car.sight_distance, 1)
        pass
    # Draw the car 
    pygame.draw.polygon(screen, color, (position1.get_tuple(), position2.get_tuple(), position3.get_tuple(), position4.get_tuple()))
    pygame.draw.polygon(screen, constants.BLACK, (position1.get_tuple(), position2.get_tuple(), position3.get_tuple(), position4.get_tuple()), 1)

def draw_text(position = Vector(screen.get_rect().centerx, screen.get_rect().centery), message = '', text_color = constants.WHITE, back_color = constants.BLACK, font = None, anti_aliasing = True):
    """
    Draws text on the screen
        position    (Vector  :   position where the text is to be written
        message (str)        :   the message that is to be written
        text_color (list)    :   the color of the text to be written
        back_color (list)    :   the color on which the text is to be written
        font (pygame.font)   :   the font that will be used for the text to be written
        anti_aliasing (bool) :   whether we should antialias the text to be written
    """
    #   The (optional) pygame.font module is not supported : cannot draw text
    if not pygame.font:
        raise Exception("WARNING (in draw_text()) : the pygame.font module is not supported, cannot draw text.")
    else:
        #   No font is provided : use of a default font
        if not font:
            font = pygame.font.Font(None, 17)
            
        text = font.render(message, anti_aliasing, text_color, back_color)
        textRect = text.get_rect()
        textRect.x, textRect.y = position.x, position.y
        screen.blit(text, textRect)
        
def draw_traffic_light(position, road, gate):
    """
    Draws a traffic light...
        x, y : coordinates
        road : the road
        gate : 1 or 0, the gate
    """
    
    TF_RADIUS = 3
    width     = 0
    state     = road.gates[gate]

    (parallel, orthogonal) = road.reference   
    start_position  = position + orthogonal * 6 - parallel * 12
    d_position      = Vector(0, -1) * TF_RADIUS * 2
    
    for i in range(3):
        if (state) and (i == 0):
            color = constants.LIGHT_GREEN
            width = 0
        elif (not state) and (i == 2):
            color = constants.LIGHT_RED
            width = 0
        else:
            color = constants.GRAY
            width = 1
        
        position = start_position + d_position * i
        pygame.draw.circle(screen, color, position.get_list(), TF_RADIUS, width)

def draw_road(road):
    """
    Draws a given road on the screen and all the cars on it.
        road (Road) : the aforementioned road.
            
    Dessine une route donnée à l'écran et toutes les voitures dessus.
        road (Road) : la route sus-citée.
    """
    
    (start_position, end_position) = (road.begin.position.ceil(), road.end.position.ceil())
   
    # This is not perfect... but it's ok for now I guess -- Sharayanan
    draw_traffic_light(end_position, road, constants.LEAVING_GATE)
     
    color = constants.GREEN
    key = 0
    if road.cars and constants.DISPLAY_DENSITY:
        occupation = 0
        for car in road.cars:
            occupation += car.length
            
        key = 2 * (float(occupation)/float(road.length)) * 255
        if key > 255: key = 255
        color = [key, 255 - key, 0]
    
    pygame.draw.aaline(screen, color, start_position.get_tuple(), end_position.get_tuple()) # EXPERIMENTAL
    
    # Draw an arrow pointing at where we go
    #draw_arrow(road)
    
    if road.cars and key < 200:
        # Do not draw cars when density exceeds ~80%
        for car in road.cars:
            draw_car(car)

def draw_info(): 
    cars_on_road        = 0
    cars_on_roundabout  = 0
    cars_waiting        = 0
    text                = []
    
    for road in init.track.roads:
        cars_on_road += len(road.cars)
        cars_waiting += road.total_waiting_cars
    for roundabout in init.track.roundabouts:
        cars_on_roundabout += len(roundabout.cars)
    
    text.append(str(len(init.track.roads)) + " roads")
    text.append(str(len(init.track.roundabouts)) + " roundabouts")
    text.append('')
    
    text.append(str(cars_on_road + cars_on_roundabout) + " cars")
    text.append("  > on roads : " + str(cars_on_road))
    text.append("  > on roundabouts : " + str(cars_on_roundabout))
    text.append("  > waiting : " + str(cars_waiting))
    #text.append("  > stress moyen: " + str(constants.angriness_mean / constants.nb_died))
    
    position = Vector()
    for i in range(len(text)):
        position.x = 640
        position.y = 4 + 16 * i
        draw_text(position, text[i])
            
def draw_scene():
    """
    Draws the complete scene on the screen.
    Dessine la scène entière à l'écran.
    """  
    try:
        screen.fill(constants.BLACK)
    except pygame.error, exc:
        # Avoid errors during unloading
        exit()
        
    # EXPERIMENTAL
    if init.track.picture:
        screen.blit(init.track.picture, (0,0))
    
    for road in init.track.roads:
        draw_road(road)
    for roundabout in init.track.roundabouts:
        draw_roundabout(roundabout)
        
    draw_info()
    
    pygame.display.flip()
    pygame.display.update()
    
def halt():
    """
    Closes properly the simulation.
    Quitte correctement la simulation.
    """
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
    for roundabout in init.track.roundabouts:
        roundabout.update()

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
    
    #   please do not shout everywhere, i agree on your point, but this particular function may remain, i think -kamaradclimber
    # Please don't *shout*, this is not a function, and this is required here -- Sharayanan
    pygame.init()
    pygame.display.set_caption("Thereisnorush (testing) - r" + str(constants.REVISION_NUMBER))
    
    # Main loop
    main_loop()

# Don't write anything after that !
