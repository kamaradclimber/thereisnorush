# -*- coding: utf-8 -*-
"""
File        :   init.py
Description :   defines the classes needed for the simulation
"""

import constants    as __constants__
import track        as __track__
import car          as __car__ 
import road         as __road__
import roundabout   as __roundabout__
from os             import getcwd

def add_demo_car(road_number, position):
    """
    Adds a car on the demo track
    """
    new_car = __car__.Car(track.roads[road_number], position)

def load_demo_track():
    # Temporary testing zone
    track_parser = __track__.Track_Parser(track)
    track_parser.load_from_file("demo_track.txt", "demo_track.png")
    
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

# Bootstrap
if (__name__ == '__main__'):
    raise Exception("You should run interface.py instead of this file !")
else:
    track = __track__.Track()
    load_demo_track()