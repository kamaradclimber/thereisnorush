# -*- coding: utf-8 -*-
"""
File        :   init.py
Description :   defines the classes and constants needed for the simulation
"""

try:
    INIT_FILE
except NameError:
    INIT_FILE = True
    
    #   Useful constants
    delta_t = 0.1
    
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

    ROAD_COLOR      = WHITE 
    
    DISPLAY_DENSITY = False # You may de-activate per-density coloring (+ fps)
    
    REVISION_NUMBER = 97

    try:
        from os     import getcwd
        from track  import Track
        from track  import Track_Parser
        from car    import Car 
        from road   import Road
        from node   import Node
    except:
        pass
        
    #   TESTING ZONE
    
    def add_demo_car(road_number, position):
        """
        Adds a car on the demo track
        """
        new_car = Car(track.roads[road_number], position)
    
    def load_demo_track():
        # Temporary testing zone
        track_parser = Track_Parser(track)
        track_parser.load_from_file("demo_track.txt", "demo_track.png")
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
    
    def find_key(dic, val):
        """
        Finds the key associated to a value in a dictionnary
        """
        candidates = [k for k, v in dic.iteritems() if v == val]
        if len(candidates) > 0:
            return candidates[0]
        else:
            return None 
            
    def shift_list(list):
        """
        Effects a shift on a list 
        """
        return [list[-1]] + list[0:len(list)-1]
    
    if (__name__ == '__main__'):
        raise Exception("You should run interface.py instead of this file !")
    else:
        track = Track()
        load_demo_track()
