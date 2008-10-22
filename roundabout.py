# -*- coding: utf-8 -*-
"""
File        :   roundabout.py
Description :   defines the class "Roundabout"
"""

import constants
import init
from math   import pi
from pygame import time
from random import randint
from vector import Vector

class Roundabout:
    """
    Crossroads of our city ; may host several roads.
    """
    def __init__(self, new_x, new_y, new_spawning=False, radius=constants.ROUNDABOUT_RADIUS_DEFAULT):
        """
        Constructor method : creates a new roundabout.
            new_coordinates (list) : the coordinates [x, y] for the roundabout
        """
        
        self.position       = Vector(new_x, new_y)
        self.incoming_roads = []
        self.leaving_roads  = []
        self.max_cars       = 5
        self.cars           = []
        self.slots_cars     = {}
        self.slots_roads    = [None for i in range(self.max_cars)]
        self.spawning       = new_spawning
        self.spawn_timer    = time.get_ticks()
        self.last_rotation  = time.get_ticks()
        self.rotation_speed = constants.ROUNDABOUT_DEFAULT_ROTATION_SPEED
        
        self.to_kill = [] 
        
    def add_me(self, road):
        """
        Connecte, lors d'une initialisation, une route à un slot sur le carrefour.
        """
        if road in self.slots_roads:
            return None
        
        #   How many free slots there are
        total_free_slots = len([slot for slot in self.slots_roads if slot is None])

        if total_free_slots:
            #   Choose a random free slot to allocate for the road
            free_slots = [i for (i,slot) in enumerate(self.slots_roads) if slot is None]

            if free_slots:
                self.slots_roads[free_slots[0]] = road
                self.slots_cars[free_slots[0]]  = None
            else:
                raise Exception("WARNING: There is no slot to host any further roads!")
            
    def _update_gate(self, road, waiting_cars):
        """
        Road-specific gate handling
            road (Road) : the road whose traffic ligths are to be handled
            waiting_cars (int) : the *total* number or cars waiting for the roundabout
        """
        #   Too many waiting cars
        if road.total_waiting_cars > 8:
            if road.begin == self:
                self.set_gate(road, True)
            if road.end == self:
                self.set_gate(road, True)
        
        #   Too long waiting time
        if road.last_gate_update(constants.LEAVING_GATE) > 10000 and not road.gates[constants.LEAVING_GATE] and road.total_waiting_cars:
            self.set_gate(road, True)
    
    def update_gates(self):
        """
        Manages the gates of the roads. This function will be the key part of the code, that's why it is called everytime
        """
        # Number of cars that are waiting on all the incoming roads
        num_waiting = 0
        for road in self.incoming_roads:
            num_waiting += road.total_waiting_cars

        # CAUTION: this *has* to be in a separate loop !
        for road in self.incoming_roads:
            self._update_gate(road, num_waiting)
            
        if self.is_full: # priorité 0
            for road in self.incoming_roads:
                self.set_gate(road, False)
            for road in self.leaving_roads:
                self.set_gate(road, True)
    
    def update_car(self, car):
        """
        Updates a given car on the roundabout 
        """
        if not(car.next_way(True) is None):
            next_way = car.next_way(True) % len(self.leaving_roads) # Just read the next_way unless you really go there
            car_slot = init.find_key(self.slots_cars, car)
            if car_slot is None:
                #The car wasn't found!
                raise Exception("ERROR (in roundabout.update_car()) : a car has no slot !")
            
            if self.slots_roads[car_slot] in self.leaving_roads or self.slots_roads[car_slot] in self.incoming_roads:            
                # The slots_cars[car_slot] points to an existing road
                #car_slot does not point to a road but to a slot where the current car is - kamaradclimber
                if (self.leaving_roads[next_way].is_free) and self.slots_roads[car_slot] == self.leaving_roads[next_way]:
                #la route sur laquelle on veut aller est vidée et surtout _en face_  du slot de la voiture
                    car.join(self.leaving_roads[car.next_way(False) % len(self.leaving_roads)]) # cette fois on fait une lecture destructive
            else:
                # There is an issue ; either the slot is None, or it points to the wrong thing
                if self.slots_roads[car_slot] is not None:
                    raise Exception("ERROR: slots_roads[car_slot] points to a road that doesn't exist!")
        else : #la voiture n'a pas d'endroit où aller : on la met dans le couloir de la mort
            self.to_kill.append(car)

    def update(self):
        """
        Updates the roundabout : rotate the cars, dispatch them...
        """


        if time.get_ticks() - self.last_rotation > constants.ROUNDABOUT_ROTATION_RATE:
            self.last_rotation = time.get_ticks()
            self.slots_roads = init.shift_list(self.slots_roads)
            
        self.update_gates()
        
        if self.spawning and len(self.leaving_roads) and (time.get_ticks() - self.spawn_timer > constants.SPAWN_TIME): # We are a "spawn roundabout" : let's add a car at periodic rates
            self.spawn_timer = time.get_ticks()
            chosen_road = self.leaving_roads[randint(0, len(self.leaving_roads) - 1)]
            if chosen_road.is_free:
                new_car = init.new_car(chosen_road)

        for car in self.cars:
            self.update_car(car)
            
        for car in self.to_kill:
            car_slot = init.find_key(self.slots_cars, car)
            self.slots_cars[car_slot] = None
            car.die()

        self.to_kill = []
    
    def set_gate(self, road, state):
        """
        Sets the state of the gates on the road.
            road    (Road)  :   the road whose gates are affected
            state   (bool)   :   the state (False = red, True = green) of the gate
        """
        
        if (id(road.begin) == id(self)):
            # The road begins on the roundabout: there is a gate to  before leaving
            if road.gates[constants.INCOMING_GATE] != state:
                road.gates[constants.INCOMING_GATE] = state
                if road.gates[constants.INCOMING_GATE] != state: road.gates_update[constants.INCOMING_GATE] = time.get_ticks()
        else:
            # The road ends on the road: there is a gate to  to enter
            if road.gates[constants.LEAVING_GATE] != state:
                road.gates[constants.LEAVING_GATE] = state
                if road.gates[constants.LEAVING_GATE] != state: road.gates_update[constants.LEAVING_GATE] = time.get_ticks()

    @property
    def is_full(self):
        """
        Returns whether there is no place left on the roundabout.
        """
        return (len(self.cars) >= self.max_cars)
