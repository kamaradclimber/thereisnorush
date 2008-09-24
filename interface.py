import sys, pygame, init

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

node_width  = 4
node_height = 4

# Main loop

while sim_running:
    # Check the users' actions
    event = pygame.event.poll()
   
    if event.type == pygame.QUIT: sim_running = False

    # Clear background  
    screen.fill(black)
    
    # First, draw the nodes
    for node in main.circuit.nodes:
        pt_topleft     = (node.x - node_width/2 , node.y - node_height/2)
        pt_bottomright = (node_width,             node_height)
        rectangle = pygame.Rect(pt_topleft, pt_bottomright)
        
        pygame.draw.rect(screen, red, rectangle, 0)
   
    # Them, draw the roads
    for road in main.circuit.roads:
        pt_topleft     = (road.begin.x, road.begin.y)
        pt_bottomright = (road.end.x,   road.end.y)
        rectangle = pygame.Rect(pt_topleft, pt_bottomright)
        
        pygame.draw.line(screen, white, pt_topleft, pt_bottomright, 1)
   
    # Saves and displays
    pygame.display.flip()