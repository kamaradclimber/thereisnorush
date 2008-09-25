#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import pygame   # http://www.pygame.org
import init     # ./init.py

# Pygame initialization 
pygame.init()

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

size        = width, height = (320, 240)     # Screen resolution
screen      = pygame.display.set_mode(size)  # Screen object
sim_running = True                           # Indicates whether the simulation is running

node_width  = 4
node_height = 4
node_color = red

road_color = white


def draw_node(node):
    """
    Draws a given node on the screen.
        node (node) : the aforementioned node.
    """
    pt_topleft     = (node.x - node_width / 2 , node.y - node_height / 2 )
    pt_bottomright = (node_width, node_height)
    rectangle      = pygame.Rect(pt_topleft, pt_bottomright)
    pygame.draw.rect(screen, node_color, rectangle, 0)

def draw_road(road):
    """
    Draws a given road on the screen.
        road (road) : the aforementioned road.
    """
    pt_topleft     = (road.begin.x, road.begin.y)
    pt_bottomright = (road.end.x,   road.end.y)
    rectangle      = pygame.Rect(pt_topleft, pt_bottomright)
    pygame.draw.line(screen, road_color, pt_topleft, pt_bottomright, 1)
    
def draw_scene():
    """
    Draws the complete scene on the screen
    """
    # Clear background  
    screen.fill(black)

    # First, draw the nodes, then draw the roads
    for node in init.circuit.nodes: draw_node(node)
    for road in init.circuit.roads: draw_road(road)
    
    # Saves and displays
    pygame.display.flip()

def main_loop():
    """
    Main loop : keeps updating and displaying the scene forever,
                unless somebody hits Esc.
    """
    # Main loop

    global sim_running
    while sim_running:
        # Check the users' actions
        event = pygame.event.poll()
   
        if event.type == pygame.QUIT: sim_running = False
        
        # Draw the scene
        draw_scene()
        
    # End of simulation instructions
    pass
    
# Bootstrap

if (__name__ == "__main__"):
    # Before simulation instructions
    pass
    # Main loop
    main_loop()

# Don't write anything after that !