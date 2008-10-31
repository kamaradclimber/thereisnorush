# -*- coding: utf-8 -*-
"""
File        :   road.py
Description :   defines the class "Road"
"""

import lib
import time

import constants    as __constants__
from math           import sqrt

class Road:
    """
    Connection between 2 nodes ; one-way only.
    """
    def __init__(   self,
                    new_begin       = None,
                    new_end         = None,
                    new_max_speed   = __constants__.ROAD_DEFAULT_MAX_SPEED):
        """
        Constructor method : creates a new road.
            new_begin  (Node)    : starting point for the road
            new_end    (Node)    : ending point for the road
            new_length (int)     : road length
        """
        self.begin          = new_begin
        self.end            = new_end
        self.cars           = []
        self.max_speed      = new_max_speed
        self.gates_update   = [time.clock(), time.clock()]
        self.gates          = [True, False]    # [gate at the beginning, gate at the end]
        self.parallel       = None
        self.orthogonal     = None
        self.width          = __constants__.ROAD_DEFAULT_WIDTH
        
        self.end.incoming_roads.append(self)
        self.begin.leaving_roads.append(self)
        
        self.end.host_road(self)
        self.begin.host_road(self)

    def update(self):
        """
        Updates the road (will update the cars on the road).
        """
        # CONVENTION SENSITIVE
        if self.cars:
            queue_length = len(self.cars)
            
            for i in range(queue_length):
                self.cars[queue_length - 1 - i].act()
        
    def last_gate_update(self, gate):
        """
        Return the time (in milliseconds) since the last update of a gate (0 or 1).
        """
        current_time = time.clock()
        return (current_time - self.gates_update[gate])
    
    @property
    def is_free(self):
        """
        Returns whether there is still room on the road.
        """
        # I guess there is still room as long as the last car engaged on the road if far enough from the start of the road
        if not self.cars:
            return True
        else:
            # CONVENTION SENSITIVE
            return(self.cars[0].position > self.cars[0].length + self.cars[0].headway)
    
    @property
    def length(self):
        """
        Returns the calculated length of the road.
        """
        if (self.begin is not None) and (self.end is not None):
            return abs(self.end.position - self.begin.position)
        
        return None
    
    @property
    def unit_vectors(self):
        """
        Returns the unit parallel and perpendicular vectors to a the road
        """
        
        # Avoid recomputing them each time
        if self.parallel and self.orthogonal:
            parallel = self.parallel
            orthogonal = self.orthogonal
        else:
            #   Normalized parallel and orthogonal vectors
            parallel = self.end.position - self.begin.position
            parallel.normalize()
            orthogonal = parallel.get_orthogonal()
            
            self.parallel = parallel
            self.orthogonal = orthogonal

        return (parallel, orthogonal)
    
    @property
    def total_waiting_cars(self):
        """
        Returns the number of waiting cars on the road.
        """
        if not self.cars:
            return 0
        return len([0 for car in self.cars if car.is_waiting])    
