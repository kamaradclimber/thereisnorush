# -*- coding: utf-8 -*-
"""
File        :   node.py
Description :   defines the class "Node"
"""

import init
from pygame import time
from math   import pi
from random import randint

LEAVING_GATE    = 1
INCOMING_GATE   = 0
SPAWN_TIME      = 1000

class Node:
    """
    Crossroads of our city ; may host several roads.
    """
    
    def __init__(self, new_x, new_y, new_spawning=False, radius=init.NODE_RADIUS_DEFAULT):
        """
        Constructor method : creates a new node.
            new_coordinates (list) : the coordinates [x, y] for the node
        """
        
        self.x, self.y      = new_x, new_y
        self.incoming_roads = []
        self.leaving_roads  = []
        self.cars           = []
        self.spawning       = new_spawning
        self.spawn_timer    = time.get_ticks()
        self.max_cars = 42
        self.slots = [(None, None) for i in range(self.max_cars)]
    
    def add_me(self, object): #cet ajout doit se faire de facon géométrique ?
        pass
    def am_i_at_the_beginning(self,road):
        return id(road.begin) == id(self)

    def _update_gate(self, road, waiting_cars):
        """
        Road-specific gate handling
            road (Road) : the road whose traffic ligths are to be handled
            waiting_cars (int) : the *total* number or cars waiting for the node
        """

        if road.total_waiting_cars > 8 and am_i_at_the_beginning(road): # priorité  1- pas trop de queue pour partir
            self.set_gate(road, True)
        if road.total_waiting_cars > 8 and (not am_i_at_the_beginning(road)): # priorité  1- pas trop de queue pour rentrer sur le carrefour
            self.set_gate(road, True)
   
        if road.last_gate_update(1) > 10000: # priorité 1- pas trop d'attente
            self.set_gate(road, True)
    
    def update_gates(self):
        """
        Manages the gates of the roads. This function will be the key part of the code, that's why it is called everytime
        For now, only closes gates if the node is full.
        """

        # Number of cars that are waiting on all the incoming roads
        num_waiting = 0
        for road in self.incoming_roads:
            num_waiting += road.total_waiting_cars

        # CAUTION: this *has* to be in a separate loop !
        for road in self.incoming_roads:
            
            self._update_gate(road, num_waiting)
            
        
        if self.is_full: # priorité 0
            for road in self.leaving_roads:
                self.set_gate(road, False)
    
    def update_car(self, car):
        """
        Updates a given car on the node
        """
        # TODO :
        #       · (N.UC1) check for position on the node to account for rotation (cf. N.U2)
        
        # TEMPORARY : go to where you want
        next_way = car.next_way(True) % len(self.leaving_roads) # Just read the next_way unless you really go there
        if (self.leaving_roads[next_way].is_free):
            car.join(self.leaving_roads[car.next_way(False) % len(self.leaving_roads)]) # No need for remaining_points since we start from *zero*
    
    def update(self):
        """
        Updates the node: rotate the cars, dispatch them...
        """
        # TODO :
        #       · (N.U2) Implement cars' rotation on the node before calling update_car
        
        self.update_gates() # first, update gates, unless it should be unnecessary
        
        # We are a "spawn node" : let's add a car at periodic rates
        if self.spawning and len(self.leaving_roads):
            if time.get_ticks() - self.spawn_timer > SPAWN_TIME:
                self.spawn_timer = time.get_ticks()
                
                chosen_road = self.leaving_roads[randint(0, len(self.leaving_roads) - 1)]
                if chosen_road.is_free:
                    new_car = init.new_car([], chosen_road)
        
        for car in self.cars:
            self.update_car(car)
    
    def set_gate(self, road, state):
        """
        Sets the state of the gates on the road.
            road    (Road)  :   the road whose gates are affected
            state   (bool)   :   the state (False = red, True = green) of the gate
        """
        
        if (id(road.begin) == id(self)):
            # The road begins on the node: there is a gate to  before leaving
            if road.gates[INCOMING_GATE] != state:
                road.gates[INCOMING_GATE] = state
                if road.gates[INCOMING_GATE] != state: road.gates_update[INCOMING_GATE] = time.get_ticks()
        else:
            # The road ends on the road: there is a gate to  to enter
            if road.gates[LEAVING_GATE] != state:
                road.gates[LEAVING_GATE] = state
                if road.gates[LEAVING_GATE] != state: road.gates_update[LEAVING_GATE] = time.get_ticks()

    @property
    def is_full(self):
        """
        Returns whether there is no place left on the node
        """
        
        return (len(self.cars) >= self.max_cars)

    @property
    def coords(self):
        return (self.x, self.y)