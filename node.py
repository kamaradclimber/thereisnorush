# -*- coding: utf-8 -*-

"""
File        :   node.py
Description :   defines the class "Node"
"""

import init
from pygame import time
from math   import pi
from random import randint

LEAVING_GATE             = 1
INCOMING_GATE            = 0
SPAWN_TIME               = 5000

class Node:
    """
    Crossroads of our city ; may host several roads.
    """
    
    def __init__(self, new_coordinates, radius = init.NODE_RADIUS_DEFAULT):
        """
        Constructor method : creates a new node.
            new_coordinates (list) : the coordinates [x, y] for the node
        """
        
        self.x, self.y     = new_coordinates[0], new_coordinates[1]
        self.incoming_roads  = []
        self.leaving_roads = []
        self.cars          = []
        self.spawn_timer   = time.get_ticks()
        
        # Maximum available space to host cars : perimeter divided by cars' width
        # Nombre maximum de cases disponibles pour héberger les voitures : périmètre divisé par la longueur des voitures
        
        # TEMPORARY
        #self.max_cars      = int(2 * pi * radius / car.CAR_DEFAULT_LENGTH)
        self.max_cars = 10

    def num_waiting_cars(self, road):
        """
        Returns the number of waiting cars on the road.
            road (Road) : the aforementioned road 
        """
        waiting_cars = 0
        if road.cars:
            for car in road.cars:
                if car.waiting:
                    waiting_cars += 1
        return waiting_cars
    
    def update_gate(self, road, waiting_cars):
        """
        Road-specific gate handling
            road (Road) : the road whose traffic ligths are to be handled
            waiting_cars (int) : the *total* number or cars waiting for the node
        """
        
        # TESTING ONLY: there has to be at least 2 waiting cars for the node to open, 
        # otherwise we wait 1 second and close the gates!
        # We may put some very complex behavior in this!
        if self.num_waiting_cars(road) > 1:
            self.set_gate(road, True)
        else:
            if road.gates_update[1] > 1000:
                self.set_gate(road, False)
    
    def update_gates(self):
        """
        Manages the gates of the roads. This function will be the key part of the code, that's why it is called everytime
        For now, only closes gates if the node is full.
        """

        # Number of cars that are waiting on all the incoming roads
        num_waiting = 0
        for road in self.incoming_roads:
            num_waiting += self.num_waiting_cars(road)

        # CAUTION: this *has* to be in a separate loop !
        for road in self.incoming_roads:
            
            # BEGINNING OF ROAD-SPECIFIC GATE HANDLING
            self.update_gate(road, num_waiting)
            # END OF GATE HANDLING

        # Do not add anything after this: it ensures the node closes when full!
        if self.is_full:
            for i in range(len(self.leaving_roads)):
                self.set_gate(self.leaving_roads[i], False)
                    
    #   I THINK THIS FUNCTION SHOULD BE DELETED ; PLEASE CONFIRM -- Ch@hine
    # There's no need to capitalize… you should give a proposition first, I guess. If you think it's better to remove this method, proceed. -- Sharayanan
    def manage_car(self, car, remaining_points):
        """
        Asks the node to take control over the car and move it appropriately.
        Demande au nœud de prendre le contrôle de la voiture et de la déplacer de manière adéquate.
        """
        
        if len(self.leaving_roads):
            # The node may, or may not, accept to host the car
            if len(self.cars) < self.max_cars:
                car.join(self)
        else: 
            # On est arrivé à dans une ime, faut-il faire disparaitre la voiture pour accélerer le programme ?
            # In my opinion, we should, hence the following line :
            car.die()
    
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
        
        if (len(self.incoming_roads) == 0) and (len(self.leaving_roads) > 0):
            # We are a "spawn node" : let's add a car at periodic rates
            if time.get_ticks() - self.spawn_timer > SPAWN_TIME:
                self.spawn_timer = time.get_ticks()
                
                chosen_road = self.leaving_roads[randint(0, len(self.leaving_roads) - 1)]
                new_car = init.new_car([], None)
                new_car.join(chosen_road)
        
        if self.cars:
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
                road.gates_update[INCOMING_GATE] = time.get_ticks()
        else:
            # The road ends on the road: there is a gate to  to enter
            if road.gates[LEAVING_GATE] != state:
                road.gates[LEAVING_GATE] = state
                road.gates_update[LEAVING_GATE] = time.get_ticks()

    @property
    def is_full(self):
        """
        Returns whether there is no place left on the node
        """
       
        return (len(self.cars) >= self.max_cars)

    @property
    def coords(self):
        return (int(self.x), int(self.y))