# -*- coding: utf-8 -*-

"""
File        :   track.py
Description :   defines the class "Track"
"""

import init

class Track:
    """
    Our city model : a mathematical graph made of nodes, linked to each other by roads.
    """
    
    def __init__(self, new_nodes = [], new_roads = []):
        """
        Constructor method : creates a track given the nodes and roads, if any.
            new_nodes   (list)  :   a list of the nodes
            new_roads   (list)  :   a list of the roads
        """
        
        if not isinstance(new_nodes, list):
            self.nodes = []
        else:
            self.nodes = new_nodes
        
        if not isinstance(new_roads, list):
            self.roads = []
        else:
            self.roads = new_roads
   
        # EXPERIMENTAL
        self.picture = None 

class Track_Parser:

    NODE        = "Node"
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
        if elements[0] == self.NODE:
            args = [int(item) for item in elements[1:]]
            node = init.new_node(*args)
            self.track.nodes.append(node)
        elif elements[0] == self.ROAD:
            args = [int(item) for item in elements[1:]]
            new_road = init.new_road(self.track.nodes[args[0]], self.track.nodes[args[1]])
            self.track.roads.append(new_road)
        else:
            raise Exception("ERROR : unknown element type '" + kind + "' !")