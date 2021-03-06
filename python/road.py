﻿# -*- coding: utf-8 -*-
"""
File        :   road.py
Description :   defines the class "Road"
"""

import lib


from constants  import *
from math       import sqrt

class Road:
    """
    A road acts as a container for several lanes and connects two roundabouts
    """
    def __init__(   self,
                    new_start       = None,
                    new_end         = None,
                    new_max_speed   = ROAD_DEFAULT_MAX_SPEED):
        """
        Constructor method : creates a new road.
        """

        self.start      = new_start
        self.end        = new_end
        self.max_speed  = new_max_speed
        
        self.lanes      = [Lane(self, i) for i in range(ROAD_DEFAULT_LANES)]
        
        self.traffic_lights_update   = [lib.clock(), lib.clock()]
        self.traffic_lights          = [True, False]    # [at the beginning, at the end]
       
        #   In order not to compute the unit vectors of the road several times, they are stored once they are computed
        self.parallel   = None
        self.orthogonal = None
        
        self.start.host_road(self)
        self.end.host_road(self)
        
        width = 0
        for lane in self.lanes:
            width += lane.width
        self.width = width

    def update(self):
        """
        Updates the road (will update the lanes on the road).
        """

        for lane in self.lanes:
            lane.update()
        
    def last_gate_update(self, gate):
        """
        Return the time (in milliseconds) since the last update of a gate (0 or 1).
        """

        current_time = lib.clock()
        return (current_time - self.traffic_lights_update[gate])

    def get_free_lane(self):
        """
        Returns a free lane on the road, if any.
        """
        free_lanes = [lane for lane in self.lanes if lane.is_free]
        
        if not len(free_lanes):
            return None
            
        return free_lanes[0]
        
    @property
    def is_free(self):
        """
        Returns whether there is still room on the road.
        The road is free if at least one of its lane is free.
        """
        
        for lane in self.lanes:
            if lane.is_free:
                return True
    
        return False

    @property
    def length(self):
        """
        Returns the calculated length of the road.
        """

        if (self.start is not None) and (self.end is not None):
            return abs(self.end.position - self.start.position)
        
        return None
    
    @property
    def unit_vectors(self):
        """
        Returns the unit parallel and perpendicular vectors to a the road
        """
        
        #   Avoid recomputing them each time
        if (self.parallel is not None) and (self.orthogonal is not None):
            parallel = self.parallel
            orthogonal = self.orthogonal
        else:
            #   Normalized parallel and orthogonal vectors
            parallel = (self.end.position - self.start.position).normalize()
            orthogonal = parallel.get_orthogonal()
            
            self.parallel = parallel
            self.orthogonal = orthogonal

        return (parallel, orthogonal)
    
    @property
    def total_waiting_cars(self):
        """
        Returns the total number of waiting cars on the road.
        """

        result = 0
        for lane in self.lanes:
            result += lane.total_waiting_cars
        
        return result
    
    @property
    def total_cars(self):
        """
        Returns the total number of cars on the road
        """

        result = 0
        for lane in self.lanes:
            result += len(lane.cars)
            
        return result
    
    @property
    def weight(self):
        """
        Returns the weight associated to the road, for pathfinding computations.
        Here, the weight is the time needed to walk the road.
        """

        return self.length/self.max_speed
    
    @property
    def track(self):
        """
        Returns the track to which the road belongs.
        """

        return self.start.track

class Lane():
    """
    A lane is a one-way piece of road
    """
    
    def __init__(self, new_road, new_index):
        """
        Creates a Lane on the parent new_road.
        The higher the index, the farther the lane.
        """

        self.cars   = []
        self.width  = LANE_DEFAULT_WIDTH
        self.index  = new_index
        self.road   = new_road
        
    def update(self):
        """
        Updates the lane, and all the cars on it
        """

        if not len(self.cars):
            return None
            
        queue_length = len(self.cars)
        
        for i in range(queue_length):
            self.cars[queue_length - 1 - i].act()
    
    @property
    def total_waiting_cars(self):
        """
        Returns the number of waiting cars on the lane.
        """

        if not self.cars:
            return 0
        return len([0 for car in self.cars if car.is_waiting])
    
    @property
    def is_free(self):
        """
        Returns whether there is still room on the road.
        """

        # I guess there is still room as long as the last car engaged on the road if far enough from the start of the road
        if not len(self.cars):
            return True
        else:
            # CONVENTION SENSITIVE
            return (self.cars[0].length_covered > self.cars[0].length + self.cars[0].headway)

    @property
    def start(self):
        """
        Returns the start node of the lane.
        This property is provided for convenience.
        """

        return self.road.start

    @property
    def end(self):
        """
        Returns the end node of the lane.
        This property is provided for convenience.
        """

        return self.road.end

    @property
    def track(self):
        """
        Returns the track to which the lane belongs.
        This property is provided for convenience.
        """

        return self.road.track
