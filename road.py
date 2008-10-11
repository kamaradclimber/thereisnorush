# -*- coding: utf-8 -*-

"""
File        :   road.py
Description :   defines the class "Road"
"""

import init
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
        
        # TEMPORARY
        self.vecs = False # indicates whether the vectors have been calculated
    
    def connect(self, starting_node, ending_node):
        """
        Connects the road to 2 nodes.
        """
        
        # TODO :
        #       · (N.AR1) add error handlers in order not to crash on misformed track files
        
        self.begin                  =   starting_node
        self.end                    =   ending_node
        ending_node.incoming_roads  +=  [self]
        starting_node.leaving_roads +=  [self]
    
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
            return(self.cars[0].position > self.cars[0].length/2 + self.cars[0].headway)
    
    def last_gate_update(self, gate):
        """
        Return the time (in milliseconds) since the last update of a gate (0 or 1).
        """
        
        #   Isn't that useless ? Maybe I've not understood the meaning of the following line -- Ch@hine
        # I fixed it, it should now be quite clear! -- Sharayanan
        current_time = get_ticks()
        return (current_time - self.gates_update[gate])
    
    @property
    def length(self):
        """
        Returns the calculated length of the road.
        """
        if (self.begin is not None) and (self.end is not None):
            return sqrt((self.end.x - self.begin.x)**2 + (self.end.y - self.begin.y)**2)
        
        return None
    
    @property
    def get_vectors(self):
        """
        Returns the unit parallel and perpendicular vectors to a the road
        """
        
        # Do not compute unless necessary
        if not self.vecs:
            # Get the begin and endpoints of the road
            x_start, y_start = self.begin.coords
            x_end, y_end     = self.end.coords
            
            # Get the vector parallel to the road
            para_y, para_x = y_end - y_start, x_end - x_start
            para_len = sqrt(para_x**2 + para_y**2)
            
            # Normalize it
            para_x, para_y = para_x / para_len, para_y / para_len
            
            # Get the unit vector perpendicular to the road (CCW)
            perp_x, perp_y = -para_y, para_x
         
            self.perp_x = perp_x
            self.perp_y = perp_y
            self.para_x = para_x
            self.para_y = para_y
            
            self.vecs = True
        
        return self.para_x, self.para_y, self.perp_x, self.perp_y
    
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