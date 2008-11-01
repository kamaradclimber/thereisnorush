# -*- coding: utf-8 -*-
"""
File        :   lib.py
Description :   defines the functions needed for the simulation
"""

import constants    as __constants__
from random         import randint

#   Bootstrap
if (__name__ == '__main__'):
    raise Exception("You should run interface.py instead of this file !")

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
        return list_polls[randint(0, len(list_polls) - 1)
]
