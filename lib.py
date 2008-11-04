# -*- coding: utf-8 -*-
"""
File        :   lib.py
Description :   defines the functions needed for the simulation
"""

from random import randint, choice
import constants
import time

#   Bootstrap
if (__name__ == '__main__'):
    raise Exception("You should run interface.py instead of this file !")

Delta_t          = 0.0

def round(number, decimals = 0):
    """
    """
    return int(number * (10**decimals))/float(10**decimals)
    
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

def proba_poll(events):
    """
    Returns an event with a given probability
        events = [value1, proba1, value2, proba2...]
        probas should be integer values
    """
    list_polls  = []
    
    for event in events:
        list_polls += [event[0] for i in range(event[1])]
        
    if len(list_polls) == 0:
        raise Exception('ERROR (in init.proba_poll()): incorrect data format.')
    else:
        return choice(list_polls)

def clock():
    """
    Returns the time multiplied by the simulation speed
    """
    if constants.time_last_counter == 0:
        constants.time_last_counter = time.clock()

    time_interval = time.clock() - constants.time_last_counter
    constants.time_static_counter += time_interval * constants.simulation_speed
            
    constants.time_last_counter = time.clock()
    
    return constants.time_static_counter
    
def set_speed(new_speed):
    """
    Sets the simulation speed
    Please use this instead of directly addressing constants.simulation_speed
    """
    constants.simulation_speed = new_speed
    
def get_speed():
    """
    Returns the simulation speed
    Please use this instead of directly addressing constants.simulation_speed
    """
    return constants.simulation_speed
