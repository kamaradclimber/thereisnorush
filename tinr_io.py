#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# Thereisnorush IO Module (tinr_io.py)
# 
# Manages file operations

import string #               standard python library
import init   # ./init.py     classes definitions

node_code = "NODE"
road_code = "ROAD"

def add_track_element(circuit, elements):
    """
    Adds an element to the track, once it's been checked and validated.
        circuit  (track)  : the track where to put the data.
        elements (list) : a list describing the element [type, arg1, arg3…]
    """

    if (elements[0] == node_code):
        # The element is a node
        circuit.addNode([elements[1], elements[2]])
    elif (elements[1] == road_code):
        # The element is a road
        circuit.addRoad(circuit.nodes[elements[1]], circuit.nodes[elements[2]], elements[3])
    else:
        # Should never be reached: something went wrong
        pass
    
    pass

def get_lines(filename):
    """
    Reads a file and returns a list of its lines.
        filename (string) : the complete name of the file to be read.
    """
    filedata = open(filename)
    lines = []
    
    for line in filedata: lines += [line.strip()]

    return lines
    
def track_line_parse(circuit, line):
    """
    Parses a line in a track description file.
        circuit  (track)  : the track where to put the data.
        line (string) : a line of text to be parsed.
    """
    elements = string.replace(string.upper(line), ",", " ").split()
    el_type = ""
    el_args = 0

    # Get element type
    if (len(elements) == 0):
        # Empty line or incorrect data
        pass
    else:
        # Get the track element's type
        el_type = elements[0]

    # Define how many arguments are to expect
    if (el_type == node_code):
        # The element is a node : 2 arguments expected
        el_args = 2
    elif (el_type == road_code):
        # The element is a road : 3 arguments expected
        el_args = 3
    else:
        # Empty element or incorrect data
        pass

    # Check whether the arguments are corrects
    if (len(elements) == 1 + el_args):
        # The line is correct, let's convert them and add the element !
        try:
            # Convert arguments to int and add the element
            for i in range(el_args): elements[i+1] = int(elements[i+1])
            add_track_element(circuit, elements)
        except:
            # Ill-formed element
            pass
    else:
        # The line is incorrect
        pass

def load_track(circuit, filename):
    """
    Loads a track from a textfile, checks its validity, parses it
    and loads it in the simulation.
        circuit  (track)  : the track where to put the data.
        filename (string) : the name of the file to load.
    """
    try:
        # Attempts to load & read the file
        lines = get_lines(filename)
    except:
        # The file doesn't exists or any other error
        pass
    for line in lines: track_line_parse(circuit, line)

##############################################################################
#
#   TESTING ZONE

circuit = init.Track()
load_track(circuit, "track_default.txt")
