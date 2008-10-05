# -*- coding: utf-8 -*-

"""
File        :   track.py
Description :   defines the class "Track"
"""

try:
    TRACK_FILE
except NameError:
    TRACK_FILE = True
    
    import string
    import init 
    import road
    import car 
    import node
    
    class Track:
        """
        Our city model : a mathematical graph made of nodes, linked to each other by roads.
        """
        
        def __init__(self, new_nodes = None, new_roads = None):
            """
            Constructor method : creates a track given the nodes and roads, if any.
                new_nodes   (list)  :   a list of the nodes
                new_roads   (list)  :   a list of the roads
            """
            
            if (new_nodes is None) or (not isinstance(new_nodes, list)):
                self.nodes = []
            else:
                self.nodes = new_nodes
            
            if (new_roads is None) or (not isinstance(new_nodes, list)):
                self.roads = []
            else:
                self.roads = new_roads
        
        def add_element(self, elements):
            """
            Adds an element to the track, once it's been checked and validated.
                elements    (list)      :   a list describing the element [type, arg1, arg2…]
            """
            if (elements[0] == init.NODE):
                self.nodes.append(node.Node([elements[1], elements[2]]))
            elif (elements[0] == init.ROAD):
                new_road = road.Road(self.nodes[elements[1]], self.nodes[elements[2]], elements[3])
                self.roads += [new_road]
                new_road.connect(self.nodes[elements[1]], self.nodes[elements[2]])
            else:
                print "ERROR : unknown element type '" + elements[0] + "'."
                pass
        
        def parse_line(self, line):
            """
            Parses a line in a track description file.
                line    (string)    :   the line of text to be parsed
            """
            
            elements        = string.replace(line, ",", " ").split()
            kind            = ""
            total_arguments = 0
            
            #   Get element type
            if len(elements) != 0:
                kind = elements[0]
            
            #   Define how many arguments are expected
            if (kind == init.NODE):
                total_arguments = 2 #   abscissa and ordinate
            elif (kind == init.ROAD):
                total_arguments = 3 #   starting node, ending node and length
            else:
                print "ERROR : unknown element type '" + kind + "' !"
                pass
            
            #   Add the specified element to the track, if everything is OK
            if (len(elements) == 1 + total_arguments):
                try:
                    for i in range(1, total_arguments):
                        elements[i] = int(elements[i])
                    self.add_element(elements)
                except Exception, exc:
                    print "ERROR : in parsing the following line : "
                    print elements
                    print exc 
                    pass
            else:
                print "ERROR : wrong parameters given for the element '" + kind + "'."
                print elements
        
        def load_from_file(self, file_name):
            """
            Loads a track from a textfile, checks its validity, parses it
            and loads it in the simulation.
                file_name    (string)    :   the name of the file to load.
            """
            
            # TODO :
            #       · (T.LFF1) try to figure out a way to force the current directory to be the correct one (especially on Windows), since it raises an error when cwd isn't init.py's directory.
            
            try:
                # Attempts to load & read the file
                file_data   = open(file_name)
                lines       = []
                
                for line in file_data:
                    lines += [line.strip()]
                
            except Exception, exc:
                # The file doesn't exists or any other error
                print "ERROR : the file " + file_name + " cannot be loaded."
                print "Current directory is : " + getcwd() 
                print exc 
                pass
                exit()
            
            for line in lines:
                self.parse_line(line)