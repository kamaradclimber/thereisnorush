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

    def __init__(self, roundabout1 = None, roundabout2 = None):
        """
        Constructor method : creates a new road.
        """

        self.roundabouts        = [roundabout1, roundabout2]
        self.max_speed          = ROAD_DEFAULT_MAX_SPEED
        self.lanes              = [Lane(self, roundabout1), Lane(self, roundabout2)]
        self.last_lights_update = {}
        self.lights             = {}
       
        for roundabout in self.roundabouts:
            if roundabout is not None:
                self.lights[roundabout]             = [True, True]                  # [ENTRANCE, EXIT]
                self.last_lights_update[roundabout] = [lib.clock(), lib.clock()]    # Same

                roundabout.host_road(self)
    
    def other_extremity(self, roundabout):
        """
        Given a roundabout, returns the other roundabout extremity of the road.
        Returns None if the given roundabout is not an extremity of the road.
        """
        
        #   The road is not even connected to the roundabout => no answer
        if not (roundabout in self.roundabouts):
            return None

        if roundabout == self.roundabouts[0]:
            return self.roundabouts[1]

        return self.roundabouts[0]
    
    def can_lead_to(self, roundabout):
        """
        Returns True if the road has a lane that goes to the given roundabout, and False otherwise.
        """
        
        #   The road is not even connected to the roundabout => the answer is False
        if not (roundabout in self.roundabouts):
            return False
        
        #   Check lane per lane if exists one that ends to the roundabout
        for lane in self.lanes:
            if lane.end == roundabout:
                return True

        return False

    def update(self):
        """
        Updates the road (will update the lanes on the road).
        """

        for lane in self.lanes:
            lane.update()
        
    def get_lane_to(self, roundabout):
        """
        Returns a free lane on the road, if any.
        """
        
        if not (roundabout in self.roundabouts):
            return None

        free_lanes = [lane for lane in self.lanes if (lane.is_free) and (lane.end == roundabout)]
        
        if not len(free_lanes):
            return None
            
        return free_lanes[0]
       
    def unit_vectors(self, roundabout):
        """
        Returns the unit parallel and perpendicular vectors to a the road, oriented towards the given roundabout.
        """
        
        if self.lanes[0].end == roundabout:
            return self.lanes[0].unit_vectors

        (parallel, orthogonal) = self.lanes[0].unit_vectors

        return (-parallel, -orthogonal)
   
    def set_light(self, roundabout, gate, state):
        """
        Sets the state of the traffic lights on the road.
        """
        
        if not (roundabout in self.roundabouts):
            raise Exception('ERROR in road.set_light() : the given roundabout is not an extremity of the road !')

        #   Set which gate is to be updated
        current_state = self.lights[roundabout][gate]
        
        #   Update if necessary
        if current_state != state:
            self.last_lights_update[roundabout][gate]   = lib.clock()
            self.lights[roundabout][gate]               = state

    @property
    def width(self):
        """
        Returns the width of the road, which is the sum of its lanes' width
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
        Returns True if the road is one-way, and False otherwise.
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

        #for lane in self.lanes:
        #    if len(lane.vehicles):
        #        buffer = lane.vehicles[0].length_covered / 5 + (self.length - lane.vehicles[0].length_covered) / self.max_speed
        #    else:
        #        return self.length/self.max_speed
        #
        #    if buffer < result:
        #        result = buffer

        return result
    
    @property
    def track(self):
        """
        Returns the track to which the road belongs.
        This property is provided for convenience.
        """

        return self.roundabouts[0].track

class Lane():
    """
    A lane is a one-way piece of road.
    """
    
    def __init__(self, new_road, new_start):
        """
        Creates a Lane on the parent new_road.
        """

        self.vehicles   = []
        self.width      = LANE_DEFAULT_WIDTH
        self.road       = new_road
        self.start      = new_start
        
        #   In order not to compute the unit vectors of the road several times, they are stored once they are computed
        self.parallel   = None
        self.orthogonal = None
        
    def update(self):
        """
        Updates the lane, and all the vehicles on it.
        """

        if not len(self.vehicles):
            return None
            
        queue_length = len(self.vehicles)
        
        #   Update the vehicles, from the first to the last
        for i in range(queue_length):
            self.vehicles[queue_length - 1 - i].act()
    
    def last_light_update(self, gate):
        """
        Return the time (in milliseconds) since the last update of a gate (0 or 1).
        """
        
        if gate == ENTRANCE:
            return self.road.last_lights_update[self.start][gate]

        return self.road.last_lights_update[self.end][gate]
    
    def light(self, gate):
        """
        Return the state of the given light.
        """

        if gate == ENTRANCE:
            return self.road.lights[self.start][gate]

        return self.road.lights[self.end][gate]

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

        #   I guess there is still room as long as the last vehicle engaged on the road if far enough from the start of the road
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
        
        return self.road.other_extremity(self.start)
    
    @property
    def length(self):
        """
        Returns the length of the lane, which is exactly the same as the length of its road.
        This property is provided for convenience.
        """

        return self.road.length

    @property
    def unit_vectors(self):
        """
        Returns the unit parallel and perpendicular vectors to the lane, oriented towards the end of the lane.
        """
        
        #   Avoid recomputing them each time
        if (self.parallel is not None) and (self.orthogonal is not None):
            parallel    = self.parallel
            orthogonal  = self.orthogonal
        else:
            #   Normalized parallel and orthogonal vectors
            parallel    = (self.end.position - self.start.position).normalize()
            orthogonal  = parallel.get_orthogonal()
            
            self.parallel   = parallel
            self.orthogonal = orthogonal

        return (parallel, orthogonal)
    
    @property
    def track(self):
        """
        Returns the track to which the lane belongs.
        This property is provided for convenience.
        """

        return self.road.track
