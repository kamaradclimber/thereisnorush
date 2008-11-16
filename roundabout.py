# -*- coding: utf-8 -*-
"""
File        :   roundabout.py
Description :   defines the class "Roundabout"
"""

import lib
from vector         import Vector
import vehicle      as __vehicle__
from constants      import *
from random         import choice

class Roundabout:
    """
    Crossroads of our city ; may host several roads.
    """

    def __init__(self, new_track, new_x, new_y):
        """
        Constructor method : creates a new roundabout.
        """
        
        self.track          = new_track
        self.position       = Vector(TRACK_SCALE * new_x + TRACK_OFFSET_X, 
                                     TRACK_SCALE * new_y + TRACK_OFFSET_Y)
        self.radius         = ROUNDABOUT_RADIUS_DEFAULT
        self.max_vehicles   = ROUNDABOUT_DEFAULT_MAX_CARS
        self.rotation_speed = ROUNDABOUT_DEFAULT_ROTATION_SPEED
        self.vehicles       = []
        self.to_kill        = []
        self.slots_vehicles = {}
        self.slots_roads    = [None for i in range(self.max_vehicles)]
        self.spawning       = False
        self.last_spawn     = lib.clock()
        self.last_shift     = lib.clock()
        self.spawn_delay    = SPAWN_TIME
        self.local_load     = 0
        
        self.name = id(self)
        
        self.vehicle_spiraling_time = {}

    def host_road(self, new_road):
        """
        Connects a road to a slot, must be called during initialization.
        """
        
        #   Error handling
        if new_road in self.slots_roads:
            return None

        #   Choose a random free slot, if any, to allocate for the road
        free_slots = [i for (i, road) in enumerate(self.slots_roads) if road is None]

        if len(free_slots):
            self.slots_roads[free_slots[0]]     = new_road
            self.slots_vehicles[free_slots[0]]  = None
        else:
            raise Exception("ERROR (in Roundabout.host_road()) : there is no slot to host any further roads !")
            
    def _update_lights(self):
        """
        Handles traffic lights.
        """

        #   Get the most lested parent
        if len(self.parents):
            chosen_one = self.parents[0]
            for parent in self.parents:
                if parent.global_load > chosen_one.global_load:
                    chosen_one = parent
        
        #   Open the way FROM this one, and close ways FROM others
        for parent in self.parents:
            road = parent.get_road_to(self)

            if parent == chosen_one:
                road.set_light(self, EXIT, True)
            else:
                road.set_light(self, EXIT, False)
        
        #   Then, let's update each road, few rules because the general view overrules the local one.
        for parent in self.parents:
            road = parent.get_road_to(self)
            lane = road.get_lane_to(self)
            
            #   Too many cars waiting
            if road.total_waiting_vehicles(self) > 5:
                road.set_light(self, EXIT, True)

            #   Too long waiting time : open the gate and not close others
            if (lane.last_light_update(EXIT) - lib.clock() > WAITING_TIME_LIMIT) and (road.total_waiting_vehicles(self)):
                road.set_light(self, EXIT, True)

    def update_vehicle(self, vehicle):
        """
        Updates a given vehicle on the roundabout 
        """
        
        if not (vehicle in self.vehicle_spiraling_time):
            self.vehicle_spiraling_time[vehicle] = [vehicle.total_waiting_time, lib.clock()]
            
        vehicle.total_waiting_time = self.vehicle_spiraling_time[vehicle][0] + lib.clock() - self.vehicle_spiraling_time[vehicle][1]
        
        if (vehicle.path is not None) and (len(vehicle.path)) and len(self.children):
            next_way        = vehicle.next_way()

            #   The vehicle has lost its slot   
            if vehicle.slot is None:
                raise Exception("ERROR (in Roundabout.update_vehicle()) : a vehicle has no slot !")
            
            #   The vehicle's slot is in front of a leaving road
            if (self.slots_roads[vehicle.slot] is not None) and (self.slots_roads[vehicle.slot] == next_way) and (next_way.is_free(next_way.other_extremity(self))):
                #la route sur laquelle on veut aller est vidée et surtout _en face_  du slot de la voiture
                vehicle.join(vehicle.next_way(False)) # cette fois on fait une lecture destructive

        #la voiture n'a pas d'endroit où aller : on la met dans le couloir de la mort
        else:
            self.to_kill.append(vehicle)

    def update(self):
        """
        Updates the roundabout : rotate the vehicles, dispatch them...
        """

        #   Make the cars rotate
        if lib.clock() - self.last_shift > ROUNDABOUT_ROTATION_RATE:
            self.last_shift     = lib.clock()
            self.slots_roads    = lib.shift_list(self.slots_roads)

        #   Spawning mode
        if self.spawning and len(self.children) and (lib.clock() - self.last_spawn > self.spawn_delay):
            self.last_spawn = lib.clock() 
            chosen_child    = choice(self.children)
            chosen_road     = self.get_road_to(chosen_child)
            chosen_lane     = chosen_road.get_lane_to(chosen_child)

            if (chosen_lane is not None) and (chosen_lane.is_free):
                vehicle_type_events = [(STANDARD_CAR, 80), (TRUCK, 15), (SPEED_CAR, 5)]
                new_vehicle         = __vehicle__.Vehicle(chosen_lane, lib.proba_poll(vehicle_type_events))

        #   Update traffic lights
        self._update_lights()
                
        #   Update vehicles
        for vehicle in self.vehicles:
            self.update_vehicle(vehicle)
        
        #   Kill vehicles that have reached their destination
        for vehicle in self.to_kill:
            vehicle_slot = lib.find_key(self.slots_vehicles, vehicle)
            self.slots_vehicles[vehicle_slot] = None
            vehicle.die()

        self.to_kill = []
    
    def get_local_load(self):
        """
        Computes in per cent a number called load (inspired by the load of a Linux station)
        """
        
        if self.parents is None:
            return 0
        
        roads_sum = 0
        for parent in self.parents:
            road        =   parent.get_road_to(self)
            roads_sum   +=  road.total_waiting_vehicles(self) * VEHICLE[STANDARD_CAR][DEFAULT_LENGTH] / road.length

        self.local_load = roads_sum + len(self.vehicles) / float(self.max_vehicles)

    def get_road_to(self, roundabout):
        """
        Returns the first road found, if any, that can lead to the given roundabout.
        Returns None if no road is found.
        /!\ A road is returned only if it has a lane that leads to the given roundabout !
        """

        for road in self.hosted_roads:
            for lane in road.lanes:
                if lane.end == roundabout:
                    return road

        return None
    
    @property
    def is_full(self):
        """
        Returns whether there is no place left on the roundabout.
        """

        return (len(self.vehicles) >= self.max_vehicles)
    
    @property
    def hosted_roads(self):
        """
        Returns the list of the roads connected to the roundabout.
        The result is the list slots_roads from which None elements are removed.
        """
        
        result = []
        for road in self.slots_roads:
            if road is not None:
                result.append(road)

        return result

    @property
    def children(self):
        """
        Returns the list of the nearby roundabouts for which it exists a lane from the roundabout to go to.
        """
        
        result = []
        for road in self.hosted_roads:
            for lane in road.lanes:
                if lane.end != self and not (lane.end in result):
                    result.append(lane.end)

        return result

    @property
    def parents(self):
        """
        Returns the list of the nearby roundabouts from which it exists a lane to go to the roundabout.
        """
        
        result = []
        for road in self.hosted_roads:
            for lane in road.lanes:
                if lane.start != self and not (lane.start in result):
                    result.append(lane.start)

        return result
    
    @property
    def neighbours(self):
        """
        Returns the list of the nearby roundabouts.
        /!\ This list is not the concatenation of the lists "parents" and "children", because those lists may have common elements !
        """

        result = []
        for road in self.hosted_roads:
            result.append(road.other_extremity(self))   # this suppose that there is at most 1 road between 2 roundabouts

        return result

    #   The two following properties are deprecated, other properties are enough to retrieve this piece of information -- Ch@hine
    @property
    def incoming_lanes(self):
        """

        """
        
        result = []
        for road in self.slots_roads:
            if road is None:
                continue

            for lane in road.lanes:
                if lane.end == self:
                    result.append(lane)

        return result
    
    @property
    def leaving_lanes(self):
        """

        """

        result = []
        for road in self.slots_roads:
            if road is None:
                continue
                
            for lane in road.lanes:
                if lane.end == self:
                    result.append(lane)
                    
        return result

    @property
    def total_waiting_vehicles(self):
        """
        Returns the number of vehicles waiting on all the incoming roads connected to this roudabout.
        """

        total = 0
        for road in self.hosted_roads:
            total += road.total_waiting_vehicles

        return total

    @property
    def global_load(self):
        """
        
        """
        result      = 1 + self.local_load * 10  # The "1 +" is only to avoid zero-division ;
        
        for parent in self.parents:
            result += parent.local_load

        return result
