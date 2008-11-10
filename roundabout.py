# -*- coding: utf-8 -*-
"""
File        :   roundabout.py
Description :   defines the class "Roundabout"
"""

import lib
from vector         import Vector
import vehicle      as __vehicle__
from constants      import *


class Roundabout:
    """
    Crossroads of our city ; may host several roads.
    """

    def __init__(self,
                 new_track,
                 new_x, 
                 new_y, 
                 new_spawning   = False, 
                 new_radius     = ROUNDABOUT_RADIUS_DEFAULT):
        """
        Constructor method : creates a new roundabout.
        """
        
        self.track          = new_track
        self.position       = Vector(TRACK_SCALE * new_x + TRACK_OFFSET_X, 
                                     TRACK_SCALE * new_y + TRACK_OFFSET_Y)
        self.radius         = new_radius
        
        self.vehicles       = []
        self.to_kill        = [] 
        self.slots_vehicles = {}
        
        self.max_vehicles   = ROUNDABOUT_DEFAULT_MAX_CARS
        self.rotation_speed = ROUNDABOUT_DEFAULT_ROTATION_SPEED
        
        self.spawning       = new_spawning
        self.spawn_timer    = lib.clock()
        self.last_shift     = lib.clock()
        self.spawn_time     = SPAWN_TIME
        self.slots_roads    = [None for i in range(self.max_vehicles)]
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
            
    def _update_traffic_lights(self):
        """
        Handles traffic lights.
        """

        #   First, let's have a global view of situation 
        around_incoming_loads = []
        around_leaving_loads  = []
        
        #   TO FIX : if there are several lanes in a road, the same traffic light will be updated several times !
        region_load = [lane.start.global_load for lane in self.incoming_lanes]
        if region_load:
            the_chosen_one = self.incoming_lanes[region_load.index(max(region_load))]
            for lane in self.incoming_lanes:
                if lane == the_chosen_one:
                    self.set_gate(lane.road, True)
                else:
                    self.set_gate(lane.road, False)
        
        #   Then, let's update each road, few rules because the general view overrules the local one.
       
        for lane in self.incoming_lanes:
            #   Too long waiting time : open the gate and not close others
            if lane.last_gate_update(EXIT) > WAITING_TIME_LIMIT and lane.total_waiting_vehicles:
                self.set_gate(lane.road, True)

    def update_vehicle(self, vehicle):
        """
        Updates a given vehicle on the roundabout 
        """
        
        if not (vehicle in self.vehicle_spiraling_time):
            self.vehicle_spiraling_time[vehicle] = [vehicle.total_waiting_time, lib.clock()]
            
        vehicle.total_waiting_time = self.vehicle_spiraling_time[vehicle][0] + lib.clock() - self.vehicle_spiraling_time[vehicle][1]
        
        if not(vehicle.path is None) and self.leaving_lanes:
            next_way = vehicle.next_way(True) # Just read the next_way unless you really go there
            vehicle_slot = lib.find_key(self.slots_vehicles, vehicle)

            #   The vehicle has lost its slot   
            if vehicle_slot is None:
                raise Exception("ERROR (in Roundabout.update_vehicle()) : a vehicle has no slot !")
            
            #   The vehicle's slot is in front of a leaving road
            if (self.slots_roads[vehicle_slot] is not None):            
                if (self.leaving_roads[next_way].is_free) and self.slots_roads[vehicle_slot] == self.leaving_roads[next_way]:
                #la route sur laquelle on veut aller est vidée et surtout _en face_  du slot de la voiture
                    vehicle.join(self.leaving_roads[vehicle.next_way(False) % len(self.leaving_roads)].get_free_lane()) # cette fois on fait une lecture destructive

        #la voiture n'a pas d'endroit où aller : on la met dans le couloir de la mort
        else:
            self.to_kill.append(vehicle)

    def update(self):
        """
        Updates the roundabout : rotate the vehicles, dispatch them...
        """
        #   Make the cars rotate
        if lib.clock() - self.last_shift > ROUNDABOUT_ROTATION_RATE:
            self.last_shift = lib.clock()
            self.slots_roads = lib.shift_list(self.slots_roads)

        #   Spawning mode
        if self.spawning and len(self.leaving_lanes) and (lib.clock() - self.spawn_timer > self.spawn_time):
            self.spawn_timer    = lib.clock() 
            num_possible_lanes  = len(self.leaving_lanes)
            
            # Possible ways out. NB : the "1000/ " thing ensures *integer* probabilities.
            possible_lanes_events = [(self.leaving_lanes[i], 1000/num_possible_lanes) for i in range(num_possible_lanes)]
        
            chosen_lane = lib.proba_poll(possible_lanes_events)
            if chosen_lane.is_free:
                vehicle_type_events = [(STANDARD_CAR, 80), 
                                   (TRUCK       , 15), 
                                   (SPEED_CAR   ,  5)]
                                   
                new_vehicle = __vehicle__.Vehicle(chosen_lane, lib.proba_poll(vehicle_type_events))

        #   Update traffic lights
        self._update_traffic_lights()
                
        #   Update vehicles
        for vehicle in self.vehicles:
            self.update_vehicle(vehicle)
        
        #   Kill vehicles that have reached their destination
        for vehicle in self.to_kill:
            vehicle_slot = lib.find_key(self.slots_vehicles, vehicle)
            self.slots_vehicles[vehicle_slot] = None
            vehicle.die()

        self.to_kill = []
    
    def set_gate(self, road, state):
        """
        Sets the state of the traffic lights on the road.
            road    (Road)  :   the road whose traffic lights are affected
            state   (bool)   :   the state (False = red, True = green) of the gate
        """

        #   Set which gate is to be updated
        current_gate = road.roundabouts.index(self)
        
        #   Update if necessary
        if road.traffic_lights[current_gate] != state:
            road.traffic_lights_update[current_gate] = lib.clock()
            road.traffic_lights[current_gate]        = state

    def get_local_load(self):
        """
        Computes in per cent a number called load (inspired by the load of a Linux station)
        """
        
        if not len(self.incoming_lanes):
            return 0
        
        lanes_sum = sum([lane.total_waiting_vehicles * VEHICLE[STANDARD_CAR][DEFAULT_LENGTH] / lane.length for lane in self.incoming_lanes])
        self.local_load = lanes_sum + len(self.vehicles) / float(self.max_vehicles)

    @property
    def is_full(self):
        """
        Returns whether there is no place left on the roundabout.
        """

        return (len(self.vehicles) >= self.max_vehicles)
    
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
        for road in self.incoming_roads:
            total += road.total_waiting_vehicles

        return total

    @property
    def global_load(self):
        """
        
        """
        result      = 1 + self.local_load * 10  # The "1 +" is only to avoid zero-division ;
        closed_list = []

        for lane in self.incoming_lanes:
            if not lane.start in closed_list:
                result += lane.start.local_load
                closed_list.append(lane.start)

        for lane in self.leaving_lanes:
            if not lane.start in closed_list:
                result += lane.end.local_load
                closed_list.append(lane.end)

        return result
