# -*- coding: utf-8 -*-
"""
File        :   init.py
Description :   defines the classes needed for the simulation
"""

try:
    INIT_FILE
except NameError:
    INIT_FILE = True
    
    #try:
    import constants
    from os             import getcwd
    from track          import Track
    from track          import Track_Parser
    from car            import Car 
    from road           import Road
    from roundabout     import Roundabout 
    #except:
        #pass
        
    #   TESTING ZONE
    
    def add_demo_car(road_number, position):
        """
        Adds a car on the demo track
        """
        new_car = Car(track.roads[road_number], position)
    
    def load_demo_track():
        # Temporary testing zone
        track_parser = Track_Parser(track)
        track_parser.load_from_file("demo_track.txt")
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
        
    def new_roundabout(new_coordinates, spawning = False, radius = constants.ROUNDABOUT_RADIUS_DEFAULT):
        """
        Returns a new Roundabout instance (avoid cross-referencing)
        """
        return Roundabout(new_coordinates, spawning, radius)
    
    def find_key(dictionnary, value):
        """
        Finds the key associated to a value in a dictionnary.
        """
        #   Note : if several keys are candidates, the "first" encountered is returned
        candidates = [k for k, v in dictionnary.iteritems() if v == value]
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
