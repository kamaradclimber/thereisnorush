import sys, pygame, main

# Pygame initialization 
pygame.init()

#  Colors   ####################################################################

black = (0, 0, 0)
white = (255, 255, 255)
red   = (255, 0, 0)

#  Settings ####################################################################

size        = width, height = (320, 240)     # Screen resolution
screen      = pygame.display.set_mode(size)  # Screen object
sim_running = True                           # Indicates whether the simulation is running

# Main loop

while sim_running:
    # Check the users' actions
    event = pygame.event.poll()
   
    if event.type == pygame.QUIT: sim_running = False

    # Clear background  
    screen.fill(black)
    
    # First, draw the nodes
    for node in main.circuit.nodes:
        position1 = (node.x - 2, node.y - 2)
        position2 = (4, 4)
        rectangle = pygame.Rect(position1, position2)
        pygame.draw.rect(screen, red, rectangle, 0)
   
    # Them, draw the roads
    for road in main.circuit.roads:
        position1 = (road.begin.x, road.begin.y)
        position2 = (road.end.x, road.end.y)
        rectangle = pygame.Rect(position1, position2)
        pygame.draw.line(screen, white, position1, position2, 1)
   
    # Saves and displays
    pygame.display.flip()