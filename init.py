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
    
    #   Useful constants
    
    delta_t = 0.01  # TEMPORARY
    
    BLACK       = (  0,   0,   0)
    RED         = (255,   0,   0)
    GREEN       = (  0, 255,   0)
    BLUE        = (  0,   0, 255)
    WHITE       = (255, 255, 255)
    GRAY        = (190, 190, 190)
    
    LIGHT_RED   = (255,  64,  64)
    LIGHT_GREEN = ( 64, 255,  64)
    LIGHT_BLUE  = ( 64,  64, 255)
    
    RESOLUTION  = (WINDOW_WIDTH, WINDOW_HEIGHT) = (800, 600)
    
    NODE_WIDTH          = 3
    NODE_HEIGHT         = 3
    NODE_COLOR          = RED
    NODE_RADIUS_DEFAULT = 10

    ROAD_COLOR  = WHITE
   
    
    DISPLAY_DENSITY = False # You may de-activate per-density coloring (+ fps)

    from os     import getcwd   # standard python library, ne pas tout prendre, c'est plus propre :-)
    from track  import Track
    from track  import Track_Parser
    from car    import Car 
    from road   import Road
    from node   import Node
    
    #   TESTING ZONE
    
    def add_demo_car(road_number, position):
        """
        Adds a car on the demo track
        """

        new_car = Car(track.roads[road_number], position)
        #new_car.join(track.roads[road_number], position)
    
    def load_demo_track():
        # Temporary testing zone
        track_parser = Track_Parser(track)
        track_parser.load_from_file("track_default.txt")
        # Attention à l'ordre dans lequel on place les voitures ! si ce n'est pas dans lordre décroissant par position, tout le reste du programme est gêné !
        # (un tri, tout au début devrait résoudre ce bug issue2)
        # Évitez les doublons aussi, tant que possible ! -- Sharayanan
        # CONVENTION SENSITIVE
        add_demo_car(3,5)
        add_demo_car(6,50)
        add_demo_car(6,30)
        add_demo_car(6,10)
        add_demo_car(7,40)
        add_demo_car(7,10)
        add_demo_car(8,40)
        add_demo_car(9,10)
        add_demo_car(10,40)
        add_demo_car(10,10)
        add_demo_car(11,40)
        add_demo_car(11,10)
        add_demo_car(12,40)
        add_demo_car(13,20)
        add_demo_car(13,10)
        add_demo_car(14,50)
        add_demo_car(14,40)
        add_demo_car(14,30)
        add_demo_car(14,20)
        add_demo_car(14,10)
    
    def new_car(road):
        """
        Returns a new Car instance (avoid cross-referencing)
        """
        
        return Car(road)
        
    def new_road(new_begin = None, new_end = None, length = 100):
        """
        Returns a new Road instance (avoid cross-referencing)
        """
        
        return Road(new_begin, new_end, length)
        
    def new_node(new_coordinates, spawning = False, radius = NODE_RADIUS_DEFAULT):
        """
        Returns a new Node instance (avoid cross-referencing)
        """
        
        return Node(new_coordinates, spawning, radius)
    
    if (__name__ == '__main__'):
        print "You should run interface.py instead of this file !"
    else:
        track = Track()
        load_demo_track()