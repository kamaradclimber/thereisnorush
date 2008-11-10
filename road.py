# -*- coding: utf-8 -*-
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
                    roundabout1     = None,
                    roundabout2     = None,
                    new_max_speed   = ROAD_DEFAULT_MAX_SPEED):
        """
        Constructor method : creates a new road.
        """

        self.roundabouts            = [roundabout1, roundabout2]
        self.max_speed              = new_max_speed
        
        self.lanes                  = [Lane(self, roundabout1), Lane(self, roundabout2)]
        
        self.traffic_lights_update  = [lib.clock(), lib.clock()]
        self.traffic_lights         = [True, False] # [at roundabouts[0], at roundabouts[1]]
       
        
        for roundabout in self.roundabouts:
            roundabout.host_road(self)
        
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
    def width(self):
        """

        """

        result = 0
        for lane in self.lanes:
            result += lane.width
        
        return result

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

        if not (None in self.roundabouts):
            return abs(self.roundabouts[0].position - self.roundabouts[1].position)
        
        return None
    
    @property
    def is_one_way(self):
        """

        """

        roundabouts = []
        for lane in self.lanes:
            if not (lane.start in roundabouts):
                roundabouts.append(lane.start)

            if len(roundabouts) > 1:
                return False

        return True

    
    @property
    def total_waiting_vehicles(self):
        """
        Returns the total number of waiting vehicles on the road.
        """

        result = 0
        for lane in self.lanes:
            result += lane.total_waiting_vehicles
        
        return result
    
    @property
    def total_vehicles(self):
        """
        Returns the total number of vehicles on the road
        """

        result = 0
        for lane in self.lanes:
            result += len(lane.vehicles)
            
        return result
    
    @property
    def weight(self):
        """
        Returns the weight associated to the road, for pathfinding computations.
        Here, the weight is the time needed to walk the road.
        """
        result = self.length/self.max_speed

        for lane in self.lanes:
            if len(lane.vehicles):
                buffer = lane.vehicles[0].length_covered / 5 + (self.length - lane.vehicles[0].length_covered) / self.max_speed
            else:
                return self.length/self.max_speed

            if buffer < result:
                result = buffer

        return result
    
    @property
    def track(self):
        """
        Returns the track to which the road belongs.
        """

        return self.roundabouts[0].track

class Lane():
    """
    A lane is a one-way piece of road
    """
    
    def __init__(self, new_road, new_start):
        """
        Creates a Lane on the parent new_road.
        The higher the index, the farther the lane.
        """

        self.vehicles   = []
        self.width      = LANE_DEFAULT_WIDTH
        self.road       = new_road
        self.start      = new_start
        
        #   In order not to compute the unit vectors of the road several times, they are stored once they are computed
        self.parallel               = None
        self.orthogonal             = None
        
    def update(self):
        """
        Updates the lane, and all the vehicles on it
        """

        if not len(self.vehicles):
            return None
            
        queue_length = len(self.vehicles)
        
        for i in range(queue_length):
            self.vehicles[queue_length - 1 - i].act()
    
    def last_gate_update(self, gate):
        """
            Return the time (in milliseconds) since the last update of a gate (0 or 1).
        """
        
        current_time = lib.clock()
        
        if gate == ENTRANCE:
            return (current_time - self.road.traffic_lights_update[self.road.roundabouts.index(self.start)])

        return (current_time - self.road.traffic_lights_update[self.road.roundabouts.index(self.end)])

    @property
    def total_waiting_vehicles(self):
        """
        Returns the number of waiting vehicles on the lane.
        """

        if not self.vehicles:
            return 0
        return len([0 for vehicle in self.vehicles if vehicle.is_waiting])
    
    @property
    def is_free(self):
        """
        Returns whether there is still room on the road.
        """

        # I guess there is still room as long as the last vehicle engaged on the road if far enough from the start of the road
        if not len(self.vehicles):
            return True
        else:
            # CONVENTION SENSITIVE
            return (self.vehicles[0].length_covered > self.vehicles[0].length + self.vehicles[0].headway)

    @property
    def end(self):
        """
        Returns the end roundabout of the lane.
        This property is provided for convenience.
        """
        
        if self.road.roundabouts[0] == self.start:
            return self.road.roundabouts[1]
        
        return self.road.roundabouts[0]
    
    @property
    def length(self):
        """

        """

        return self.road.length

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
    def track(self):
        """
        Returns the track to which the lane belongs.
        This property is provided for convenience.
        """

        return self.road.track
