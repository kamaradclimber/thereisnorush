# -*- coding: utf-8 -*-
"""
File        :   init.py
Description :   defines the classes needed for the simulation
"""

import constants    as __constants__
from os             import getcwd
import track        as __track__
import car          as __car__ 
import road         as __road__
import roundabout   as __roundabout__
    
#   TESTING ZONE

def add_demo_car(road_number, position):
    """
    Adds a car on the demo track
    """
    new_car = __car__.Car(track.roads[road_number], position)

def load_demo_track():
    # Temporary testing zone
    track_parser = __track__.Track_Parser(track)
    track_parser.load_from_file("demo_track.txt", "demo_track.png")
    # CONVENTION SENSITIVE
    #add_demo_car(3,5)
    #add_demo_car(6,50)
    #add_demo_car(6,30)
    #add_demo_car(6,10)
    #add_demo_car(7,40)
    #add_demo_car(7,10)
    #add_demo_car(8,40)
    #add_demo_car(9,10)
    #add_demo_car(10,40)
    #add_demo_car(10,10)
    #add_demo_car(11,40)
    #add_demo_car(11,10)
    #add_demo_car(12,40)
    #add_demo_car(13,20)
    #add_demo_car(13,10)
    #add_demo_car(14,50)
    #add_demo_car(14,40)
    #add_demo_car(14,30)
    #add_demo_car(14,20)
    #add_demo_car(14,10)
    
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
    track = __track__.Track()
    load_demo_track()
