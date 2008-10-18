# -*- coding: utf-8 -*-

"""
File        :   road.py
Description :   defines the class "Road"
"""

from pygame import time
from math   import sqrt

ROAD_DEFAULT_MAX_SPEED  = 50
ROAD_DEFAULT_LENGTH     = 100

class Road:
    """
    Connection between 2 nodes ; one-way only.
    """
    
    def __init__(   self,
                    new_begin       = None,
                    new_end         = None,
                    new_max_speed   = ROAD_DEFAULT_MAX_SPEED):
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
        self.gates_update   = [time.get_ticks(), time.get_ticks()]
        self.gates          = [True, False]    # [gate at the beginning, gate at the end]
        self.parallel       = None
        self.orthogonal     = None
        
        self._set_vectors()
        
        self.end.incoming_roads.append(self)
        self.begin.leaving_roads.append(self)
        
        self.end.add_me(self)
        self.begin.add_me(self)

    def update(self):
        """
        Updates the road (will update the cars on the road).
        """
        
        # CONVENTION SENSITIVE
        if self.cars:
            queue_length = len(self.cars)
            
            for i in range(queue_length):
                self.cars[queue_length -1-i].update(queue_length - 1-i)
        

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
            return(self.cars[0].position > self.cars[0].length / 2 + self.cars[0].headway)
    
    def last_gate_update(self, gate):
        """
        Return the time (in milliseconds) since the last update of a gate (0 or 1).
        """

        current_time = time.get_ticks()
        return (current_time - self.gates_update[gate])
    
    @property
    def length(self):
        """
        Returns the calculated length of the road.
        """
        if (self.begin is not None) and (self.end is not None):
            return abs(self.end.position - self.begin.position)
        
        return None
    
    def _set_vectors(self):
        """
        Returns the unit parallel and perpendicular vectors to a the road
        """
        # Do not compute unless necessary
        if self.parallel is None or self.orthogonal is None:
            # Get the normalized parallel vector to the road
            self.parallel = self.end.position - self.begin.position
            self.parallel.normalize()
            
            # Get the normalized orthogonal vector to the road
            self.orthogonal = self.parallel.get_orthogonal()
    
    @property
    def total_waiting_cars(self):
        """
        Returns the number of waiting cars on the road.
        """
        
        total = 0
        if self.cars:
            for car in self.cars:
                if car.waiting:
                    total += 1
        return total