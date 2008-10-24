# -*- coding: utf-8 -*-

"""
File        :   track.py
Description :   defines the class "Track"
"""

import init
import constants
from roundabout import Roundabout

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
        
        if not isinstance(new_roundabouts, list):
            self.roundabouts = []
        else:
            self.roundabouts = new_roundabouts
        
        if not isinstance(new_roads, list):
            self.roads = []
        else:
            self.roads = new_roads
  
        self.picture = None
        

class Track_Parser:

    ROUNDABOUT  = "Roundabout"
    ROAD        = "Road"

    def __init__(self, track):
        """
        """
        self.track = track

    def load_from_file(self, file_name, file_picture = ''):
        """
        Loads a track from a textfile, checks its validity, parses it
        and loads it in the simulation.
            file_name    (string)    :   the name of the file to load.
        """
        
        # TODO :
        #       · (T.LFF1) try to figure out a way to force the current directory to be the correct one (especially on Windows), since it raises an error when cwd isn't init.py's directory.
        
        try:
            file_data   = file(file_name)
        except IOError:
            raise Exception("%s cannot be loaded (current directory is : %s)" % (file_name, getcwd())) 
            
        if len(file_picture) > 0:
            from pygame import image 
            try:
                self.track.picture = image.load(file_picture)
            except IOError:
                raise Exception("%s cannot be loaded (current directory is : %s)" % (file_picture, getcwd()))                 
        
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
            roundabout = Roundabout(*args)
            self.track.roundabouts.append(roundabout)
        elif elements[0] == self.ROAD:
            args = [int(item) for item in elements[1:]]
            new_road = init.new_road(self.track.roundabouts[args[0]], self.track.roundabouts[args[1]])
            self.track.roads.append(new_road)
        else:
            raise Exception("ERROR : unknown element type '" + elements[0] + "' !")
