# -*- coding: utf-8 -*-

"""
File        :   interface.py
Description :   Manages the displays and main loop.
"""

import init     # ./init.py
import pygame   # http://www.pygame.org

screen = pygame.display.set_mode(init.RESOLUTION)
debug  = True

def draw_node(node):
    """
    Draws a given node on the screen.
        node (Node) : the aforementioned node.
    
    Dessine un carrefour donné à l'écran.
        node (Node) : le carrefour sus-cité.
    """
    # TODO :
    #       · (DN1) draw the cars on the node
    
    pygame.draw.circle(screen, init.NODE_COLOR, node.position.ceil().get_tuple(), init.NODE_WIDTH)
    
    # Nodes should be drawn as rotating crossroads, in order to draw the cars that rotate in ; the problem is that roads must not be drawn from the center of the node anymore
    pygame.draw.circle(screen, init.NODE_COLOR, node.position.ceil().get_tuple(), init.NODE_WIDTH * 4, 1)
    
    if node.cars:
        # There are cars on the node, we may want to draw them
        # albeit we can't use draw_car here...
        
        #TEMPORARY : the number of cars on the node is written
        draw_text(node.position.x + 10, node.position.y + 10, str(len(node.cars)))
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

    # Coordinates for the center
    center_position = d_position + direction * length_covered
    
    # Get the appropriate vectors once
    parallel   = car.location.parallel
    orthogonal = car.location.orthogonal
    
    position1 = center_position - parallel * r_length/2 - orthogonal * r_width/2
    position2 = center_position + parallel * r_length/2 - orthogonal * r_width/2
    position3 = center_position + parallel * r_length/2 + orthogonal * r_width/2
    position4 = center_position - parallel * r_length/2 + orthogonal * r_width/2
    
    # Change the color in case the car is waiting    
    color = car.color
    if car.waiting:
        color = init.GRAY

    # Draw the car 
    pygame.draw.polygon(screen, color, (position1.get_tuple(), position2.get_tuple(), position3.get_tuple(), position4.get_tuple()), 0)

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
        raise Exception("ERROR : the pygame.font module is not supported, cannot draw text.")
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
    (start_position, end_position) = (road.begin.position, road.end.position)

    # Get the midpoint of the road
    mid_position = (start_position + end_position)/2
    
    # Draw an arrow on the left side
    arrow_start_position        = mid_position - road.orthogonal * 4 - road.parallel * 4
    arrow_end_position          = mid_position - road.orthogonal * 4 + road.parallel * 4
    
    arrow_head_start_position   = arrow_end_position - road.orthogonal - road.parallel
    arrow_head_end_position     = arrow_end_position + road.orthogonal - road.parallel
    
    pygame.draw.aaline(screen, init.BLUE, arrow_start_position.get_tuple(), arrow_end_position.get_tuple())
    pygame.draw.aaline(screen, init.BLUE, arrow_head_start_position.get_tuple(), arrow_head_end_position.get_tuple())

def draw_traffic_light(position, road, gate):
    """
    Draws a traffic light…
        x, y : coordinates
        road : the road
        gate : 1 or 0, the gate
    """
    
    TF_RADIUS = 2
    width     = 0
    state     = road.gates[gate]
    
    start_position  = position + road.orthogonal * 4 - road.parallel * 8
    d_position      = -road.parallel * TF_RADIUS * 2
    
    for i in range(3):
        if (state) and (i == 0):
            color = init.LIGHT_GREEN
            width = 0
        elif (not state) and (i == 2):
            color = init.LIGHT_RED
            width = 0
        else:
            color = init.GRAY
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
   
    # This is not perfect… but it's ok for now I guess -- Sharayanan
    draw_traffic_light(end_position, road, 1)
   
    color = init.GREEN
    key = 0
    if road.cars and init.DISPLAY_DENSITY:
        occupation = 0
        for car in road.cars:
            occupation += car.length
            
        key = 2 * (float(occupation)/float(road.length)) * 255
        if key > 255: key = 255
        color = [key, 255 - key, 0]
    
    pygame.draw.aaline(screen, color, start_position.get_tuple(), end_position.get_tuple()) # EXPERIMENTAL
    
    # Draw an arrow pointing at where we go
    draw_arrow(road)
    if road.cars and key < 200:
        # Do not draw cars when density exceeds ~80%
        for car in road.cars:
            draw_car(car)
    
def draw_scene():
    """
    Draws the complete scene on the screen.
    Dessine la scène entière à l'écran.
    """  
    try:
        screen.fill(init.BLACK)
    except pygame.error, exc:
        # Avoid errors during unloading
        exit()
        
    # EXPERIMENTAL
    if init.track.picture:
        screen.blit(init.track.picture, (0,0))
    
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
    
    #   please do not shout everywhere, i agree on your point, but this particular function may remain, i think -kamaradclimber
    # Please don't *shout*, this is not a function, and this is required here -- Sharayanan
    pygame.init()
    pygame.display.set_caption("Thereisnorush (unstable) - r" + str(init.REVISION_NUMBER))
    
    # Main loop
    main_loop()

# Don't write anything after that !