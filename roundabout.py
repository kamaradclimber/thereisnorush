# -*- coding: utf-8 -*-
"""
File        :   roundabout.py
Description :   defines the class "Roundabout"
"""

import lib


from vector         import Vector

import car          as __car__
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
        
        self.incoming_roads = []
        self.leaving_roads  = []
        self.cars           = []
        self.to_kill        = [] 
        self.slots_cars     = {}
        
        self.max_cars       = ROUNDABOUT_DEFAULT_MAX_CARS
        self.rotation_speed = ROUNDABOUT_DEFAULT_ROTATION_SPEED
        
        self.spawning       = new_spawning
        self.spawn_timer    = lib.clock()
        self.last_shift     = lib.clock()
        
        self.slots_roads    = [None for i in range(self.max_cars)]
        self.local_load     = 0
        
        self.car_spiraling_time = {}

    def host_road(self, new_road):
        """
        Connects a road to a slot, must be called during initialization.
        """

        #   Error handling
        if new_road in self.slots_roads and (new_road in self.incoming_roads or new_road in self.leaving_roads):
            return None

        #   Reference road
        if id(new_road.start) == id(self):
            self.leaving_roads.append(new_road)
        else:
            self.incoming_roads.append(new_road)
        
        #   Choose a random free slot, if any, to allocate for the road
        free_slots = [i for (i, road) in enumerate(self.slots_roads) if road is None]

        if len(free_slots):
            self.slots_roads[free_slots[0]] = new_road
            self.slots_cars[free_slots[0]]  = None
        else:
            raise Exception("ERROR (in Roundabout.host_road()) : there is no slot to host any further roads !")
            
    def _update_traffic_lights(self):
        """
        Handles traffic lights.
        """

        #   First, let's have a global view of situation 
        around_incoming_loads = []
        around_leaving_loads  = []
        
        relative_tolerance = 0.05
                
        for road in self.leaving_roads:
            around_leaving_loads.append(road.end.global_load)
            delta_load = self.global_load - road.start.global_load
            
            if delta_load >= 0 : 
                self.set_gate(road, True)
            elif abs(delta_load/self.global_load) > relative_tolerance:
                self.set_gate(road, False)
        
        #   Then, let's update each road, few rules because the general view overrules the local one.
       
        for road in self.incoming_roads:
            #   Too long waiting time : open the gate and not close others
            if road.last_gate_update(EXIT) > WAITING_TIME_LIMIT and road.total_waiting_cars:
                self.set_gate(road, True)

    def update_car(self, car):
        """
        Updates a given car on the roundabout 
        """

        if not (car in self.car_spiraling_time):
            self.car_spiraling_time[car] = [car.total_waiting_time, lib.clock()]
            
        car.total_waiting_time = self.car_spiraling_time[car][0] + lib.clock() - self.car_spiraling_time[car][1]
        
        if not(car.path is None) and self.leaving_roads:
            next_way = car.next_way(True) # Just read the next_way unless you really go there
            car_slot = lib.find_key(self.slots_cars, car)

            #   The car has lost its slot   
            if car_slot is None:
                raise Exception("ERROR (in Roundabout.update_car()) : a car has no slot !")
            
            #   The car's slot is in front of a leaving road
            if self.slots_roads[car_slot] in self.leaving_roads:            
                if (self.leaving_roads[next_way].is_free) and self.slots_roads[car_slot] == self.leaving_roads[next_way]:
                #la route sur laquelle on veut aller est vidée et surtout _en face_  du slot de la voiture
                    car.join(self.leaving_roads[car.next_way(False) % len(self.leaving_roads)].get_free_lane()) # cette fois on fait une lecture destructive

        #la voiture n'a pas d'endroit où aller : on la met dans le couloir de la mort
        else:
            self.to_kill.append(car)

    def update(self):
        """
        Updates the roundabout : rotate the cars, dispatch them...
        """
        #   Make the cars rotate
        if lib.clock() - self.last_shift > ROUNDABOUT_ROTATION_RATE:
            self.last_shift = lib.clock()
            self.slots_roads = lib.shift_list(self.slots_roads)

        #   Spawning mode
        if self.spawning and len(self.leaving_roads) and (lib.clock() - self.spawn_timer > SPAWN_TIME):
            self.spawn_timer = lib.clock() 
            num_possible_roads    = len(self.leaving_roads)
            # Possible ways out. NB : the "1000/ " thing ensures *integer* probabilities.
            possible_roads_events = [(self.leaving_roads[i], 1000/num_possible_roads) for i in range(num_possible_roads)]
        
            chosen_road = lib.proba_poll(possible_roads_events)
            if chosen_road.is_free:
                car_type_events = [(STANDARD_CAR, 80), 
                                   (TRUCK       , 15), 
                                   (SPEED_CAR   ,  5)]
                                   
                new_car = __car__.Car(chosen_road.get_free_lane(), lib.proba_poll(car_type_events))

        #   Update traffic lights
        self._update_traffic_lights()
                
        #   Update cars
        for car in self.cars:
            self.update_car(car)
        
        #   Kill cars that have reached their destination
        for car in self.to_kill:
            car_slot = lib.find_key(self.slots_cars, car)
            self.slots_cars[car_slot] = None
            car.die()

        self.to_kill = []
    
    def set_gate(self, road, state):
        """
        Sets the state of the traffic lights on the road.
            road    (Road)  :   the road whose traffic lights are affected
            state   (bool)   :   the state (False = red, True = green) of the gate
        """
        #   Set which gate is to be updated
        if id(road.start) == id(self):
            current_gate = ENTRANCE
        else:
            current_gate = EXIT
        
        #   Update if necessary
        if road.traffic_lights[current_gate] != state:
            road.traffic_lights_update[current_gate] = lib.clock()
            road.traffic_lights[current_gate]        = state

    def get_local_load(self):
        """
        Computes in per cent a number called load (inspired by the load of a Linux station)
        """
        
        if not self.incoming_roads:
            return 0
        
        roads_sum = sum([road.total_waiting_cars * VEHICLE[STANDARD_CAR][DEFAULT_LENGTH] / road.length for road in self.incoming_roads])
        self.local_load = (roads_sum + len(self.cars)) / float(self.max_cars)

    @property
    def is_full(self):
        """
        Returns whether there is no place left on the roundabout.
        """

        return (len(self.cars) >= self.max_cars)

    @property
    def total_waiting_cars(self):
        """
        Returns the number of cars waiting on all the incoming roads connected to this roudabout.
        """

        total = 0
        for road in self.incoming_roads:
            total += road.total_waiting_cars

        return total

    @property
    def global_load(self):
        """
        
        """
        result = self.local_load * 10
        for road in self.incoming_roads:
            result += road.start.local_load
        for road in self.leaving_roads:
            result += road.end.local_load

        return result
