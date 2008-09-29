#!/usr/local/bin/python
# -*- coding: utf-8 -*-

################################################################################
#
# File          :   tinr_io.py
# Description   :   Thereisnorush IO Module ; manages file operations
#
# ToDo          :   ·
#              
################################################################################

import string #   standard python library
import init   # ./init.py classes definitions

NODE = "NODE"
ROAD = "ROAD"

def add_track_element(track, elements):
    """
        Adds an element to the track, once it's been checked and validated.
            track       (Track)     :   the track where to put the data.
            elements    (list)      :   a list describing the element [type, arg1, arg2…]
    """
    
    if (elements[0] == NODE):
        track.addNode([elements[1], elements[2]])
    elif (elements[0] == ROAD):
        track.createRoad(track.nodes[elements[1]], track.nodes[elements[2]], elements[3])
    else:
        # Should never be reached: something went wrong
        pass

def getLines(filename):
    """
        Reads a file and returns a list of its lines.
            filename    (string)    :   the complete name of the file to be read
    """
    
    filedata    = open(filename)
    lines       = []

    for line in filedata:
        lines += [line.strip()]

    return lines

def track_line_parse(track, line):
    """
        Parses a line in a track description file.
            track   (Track)     :   the track where to put the data
            line    (string)    :   the line of text to be parsed
    """
    
    elements    = string.replace(string.upper(line), ",", " ").split()
    kind        = ""
    totalArguments     = 0

    # Get element type
    if (not len(elements)):
        # Empty line or incorrect data
        pass
    else:
        kind = elements[0]

    # Define how many arguments are to expect
    if (kind == NODE):
        totalArguments = 2
    elif (kind == ROAD):
        totalArguments = 3
    else:
        # Empty element or incorrect data
        pass

    # Check whether the arguments are corrects
    if (len(elements) == 1 + totalArguments):
        # The line is correct, let's convert them and add the element !
        try:
            # Convert arguments to int and add the element
            for i in range(totalArguments):
                elements[i + 1] = int(elements[i + 1])
            add_track_element(track, elements)
        except:
            # Ill-formed element
            pass
    else:
        # The line is incorrect
        pass

def load_track(track, filename):
    """
        Loads a track from a textfile, checks its validity, parses it
        and loads it in the simulation.
            track       (Track)     :   the track where to put the data.
            filename    (string)    :   the name of the file to load.
    """

    try:
        # Attempts to load & read the file
        lines = getLines(filename)
    except:
        # The file doesn't exists or any other error
        pass
    for line in lines:
        track_line_parse(track, line)
    
################################################################################
#
#   TESTING ZONE

# track = init.Track()
# load_track(track, "track_default.txt")
