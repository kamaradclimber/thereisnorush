# -*- coding: utf-8 -*-
"""
File        :   lib.py
Description :   defines the functions needed for the simulation
"""

from random     import randint, choice
from constants  import *
import time

#   Bootstrap
if (__name__ == '__main__'):
    raise Exception("You should run interface.py instead of this file !")

delta_t = 0.0

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
    global time_last_counter
    global time_static_counter
    
    if time_last_counter == 0:
        time_last_counter = time.clock()

    time_interval = time.clock() - time_last_counter
    time_static_counter += time_interval * simulation_speed
            
    time_last_counter = time.clock()
    
    return time_static_counter
    
def set_speed(new_speed):
    """
    Sets the simulation speed
    Please use this instead of directly addressing simulation_speed
    """
    
    simulation_speed = new_speed
    
def get_speed():
    """
    Returns the simulation speed
    Please use this instead of directly addressing simulation_speed
    """
    return simulation_speed

def get_simulation_time():
    """
    Returns the simulation time (h, m, s)
    """
    
    timer = time_static_counter
    
    hours   = int(timer / 3600.0) % 24
    minutes = int(timer / 60.0)   % 60
    seconds = int(timer)          % 60
    
    return hours, minutes, seconds
