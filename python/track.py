﻿# -*- coding: utf-8 -*-
"""
File        :   track.py
Description :   defines the class "Track"
"""

import lib
import roundabout   as __roundabout__
import road         as __road__
from constants      import *
from os             import getcwd

#   Bootstrap
if (__name__ == '__main__'):
    raise Exception("You should run interface.py instead of this file !")

class Track:
    """
    Our city model : a mathematical graph made of roundabouts, linked to each other by roads.
    """
    
    def __init__(self, new_roundabouts = [], new_roads = []):
        """
        Constructor method : creates a track given the roundabouts and roads, if any.
            new_roundabouts   (list)  :   a list of the roundabouts
            new_roads   (list)  :   a list of the roads
        """
        
        self.roundabouts    = new_roundabouts
        self.roads          = new_roads
        self.picture        = None
    
    def add_car(self, road_number, position):
        """
        Adds a car on the track
        """
        new_car = __car__.Car(self.roads[road_number].get_free_lane(), position)

class Track_Parser:
    ROUNDABOUT  = "Roundabout"
    ROAD        = "Road"
    
    def __init__(self, track):
        """
        """
        self.track  = track
    
    def load_from_file(self, file_name, file_picture = ''):
        """
        Loads a track from a textfile, checks its validity, parses it
        and loads it in the simulation.
            file_name    (string)    :   the name of the file to load.
        """
        
        try:
            file_data   = file(file_name)
        except IOError:
            raise Exception("%s cannot be loaded (current directory is : %s)" % (file_name, getcwd())) 
            
#        if len(file_picture) > 0:
#            from pygame import image 
#            try:
#                self.track.picture = image.load(file_picture)
#            except IOError:
#                raise Exception("%s cannot be loaded (current directory is : %s)" % (file_picture, getcwd()))                 
        
        for line in file_data:
            line = line.strip()
            if line.startswith('#') or not line:
                continue
            self.parse_line(line)
    
    def parse_line(self, line):
        """
        Parses a line in a track description file.
            line    (string)    :   the line of text to be parsed
        """
        parse_errors = []
        elements = line.replace(',', ' ').split()
        if elements[0] == self.ROUNDABOUT:
            args = [int(item) for item in elements[1:]]
            self.track.roundabouts.append(__roundabout__.Roundabout(self.track, *args))
        elif elements[0] == self.ROAD:
            args = [int(item) for item in elements[1:]]
            new_road = __road__.Road(self.track.roundabouts[args[0]], self.track.roundabouts[args[1]])
            self.track.roads.append(new_road)
        else:
            raise Exception("ERROR : unknown element type '" + elements[0] + "' !")

def load_demo_track():
    # Temporary testing zone
    track_parser = Track_Parser(track)
    track_parser.load_from_file('demo_track.txt', 'demo_track.png')

track = Track()
load_demo_track()
