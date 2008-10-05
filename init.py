# -*- coding: utf-8 -*-

"""
File        :   init.py
Description :   defines the classes and constants needed for the simulation
"""

#   To avoid multiple inclusions
try:
    INIT_FILE
except NameError:
    INIT_FILE = True
    
    import string               # standard python library
    from os   import getcwd     # standard python library, ne pas tout prendre, c'est plus propre :-)
    from math import pi         # standard python library, ne pas tout prendre, c'est plus propre :-)
    import track
    
    #   Useful constants
    
    delta_t = 0.01  # TEMPORARY
    
    BLACK       = (  0,   0,   0)
    RED         = (255,   0,   0)
    GREEN       = (  0, 255,   0)
    BLUE        = (  0,   0, 255)
    WHITE       = (255, 255, 255)
    
    LIGHT_RED   = (255,  64,  64)
    LIGHT_GREEN = ( 64, 255,  64)
    LIGHT_BLUE  = ( 64,  64, 255)
    
    RESOLUTION  = (WINDOW_WIDTH, WINDOW_HEIGHT) = (512, 384)
    
    NODE_WIDTH  = 3
    NODE_HEIGHT = 3
    NODE_COLOR  = RED
    NODE_RADIUS_DEFAULT = 10
    LEAVING_GATE  = 0
    INCOMING_GATE = 1
    
    CAR_WIDTH   = 4
    CAR_HEIGHT  = 4
    CAR_COLOR   = LIGHT_BLUE
    
    ROAD_COLOR  = WHITE
    
    NODE        = "Node"
    ROAD        = "Road"

    #   TESTING ZONE
    
    def load_demo_track():
        # Temporary testing zone
        track.load_from_file("track_default.txt")
        # Attention à l'ordre dans lequel on place les voitures ! si ce n'est pas dans lordre décroissant par position, tout le reste du programme est gêné !
        # (un tri, tout au début devrait résoudre ce bug issue2)
        # Évitez les doublons aussi, tant que possible ! -- Sharayanan
        track.roads[3].add_car(Car([], track.roads[3]), 5)
        track.roads[6].add_car(Car([], track.roads[6]), 500)
        track.roads[6].add_car(Car([], track.roads[6]), 30)
        track.roads[6].add_car(Car([], track.roads[6]), 10)
        track.roads[7].add_car(Car([], track.roads[7]), 40)
        track.roads[7].add_car(Car([], track.roads[7]), 10)
        track.roads[8].add_car(Car([], track.roads[8]), 40)
        track.roads[9].add_car(Car([], track.roads[9]), 10)
        track.roads[10].add_car(Car([], track.roads[10]), 40)
        track.roads[10].add_car(Car([], track.roads[10]), 10)
    
    if (__name__ == '__main__'):
        print "You should run interface.py instead of this file !"
    else:
        track = Track()
        load_demo_track()
