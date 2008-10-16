# -*- coding: utf-8 -*-
"""
File        :   node.py
Description :   defines the class "Node"
"""

import init
from math   import pi
from pygame import time
from random import randint
from vector import Vector

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
        
        self.position       = Vector(new_x, new_y)
        self.incoming_roads = []
        self.leaving_roads  = []
        self.max_cars = 5
        self.cars           = []
        self.slots_cars     = {}
        self.slots_roads    = [None for i in range(self.max_cars)]
        self.spawning       = new_spawning
        self.spawn_timer    = time.get_ticks()
        self.time=0

    def add_me(self, road): #cet ajout doit se faire de facon géométrique ?
        """
        Connecte, lors d'une initialisation, la route à un slot sur le carrefour.
        """
        for i in range(100):
            rand=randint(0,self.max_cars-1)
            if not self.slots_roads[rand]: #l'emplacement est libre
                self.slots_roads[rand] = road
                break
            if i == 99: #on admet que tout est plein mais il faut quand meme ajouter cette route, tant pis, cest qu'on a mal concu le self.max_cars
                self.max_cars += 1
                self.slots_cars[self.max_cars] = None
                print "le self.max_cars est trop petit, mais comme le programmeur est malin, on n'arrete pas le programme pour autant :P "
                self.slots_roads.append(road)
            
    def glue_to_slot(self,car,old_location):
        """
        Ajoute la voiture sur le carrefour en l'ajoutant sur le slot (supposé vide) en face de la route d'où elle vient
        """
        if old_location in self.slots_roads:
            id_slot = self.slots_roads.index(old_location)
            self.slots_cars[id_slot] = car #on suppose bien entendu que celui ci est vide grâçe à la ligne  166 de car.py (r85)
        else:
            raise Exception("Je viens d'un endroit inconnu !")
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
        
        if road.last_gate_update(LEAVING_GATE) > 10000 and not road.gates[LEAVING_GATE] and road.total_waiting_cars > 0: # priorité 1- pas trop d'attente
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
        
        def my_kingdom_for_a_key(dict, item): #il faut absolument trouver la methode qui doit deja exister !:! #doublon mais temporaire
            for key in dict.keys():
                if dict[key] == item: return key
        # TEMPORARY : go to where you want
        next_way = car.next_way(True) % len(self.leaving_roads) # Just read the next_way unless you really go there
        car_slot = my_kingdom_for_a_key(self.slots_cars,car)
        if (self.leaving_roads[next_way].is_free) and self.slots_roads[car_slot] == self.leaving_roads[next_way]: #la route sur laquelle on veut aller est vidéeet surtout _en face_  du slot de la voiture

            car.join(self.leaving_roads[car.next_way(False) % len(self.leaving_roads)]) # No need for remaining_points since we start from *zero*
    
    def update(self):
        """
        Updates the node: rotate the cars, dispatch them...
        """
        # TODO :
        #       · (N.U2) Implement cars' rotation on the node before calling update_car
        self.time += 1 #on m'appelle à chaque tour

        #Rotation du carrefour
        if self.time == 0:
            def list_rotate(list): return [list[-1]] + list[0:len(list)-1] #implémante la rotation d'une liste # à déplacer
            self.slots_roads =  list_rotate(self.slots_roads)

        
        self.update_gates() # first, update gates, unless it should be unnecessary
        
        # We are a "spawn node" : let's add a car at periodic rates
        if self.spawning and len(self.leaving_roads):
            if time.get_ticks() - self.spawn_timer > SPAWN_TIME:
                self.spawn_timer = time.get_ticks()
                
                chosen_road = self.leaving_roads[randint(0, len(self.leaving_roads) - 1)]
                if chosen_road.is_free:
                    new_car = init.new_car(chosen_road)
        
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
    def time(self):
        """
        Donne le 'temps' depuis écoulé depuis la dernière rotation du carrefour.
        """
        return self.time % 1
