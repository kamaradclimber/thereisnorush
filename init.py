#!/usr/local/bin/python
# -*- coding: utf-8 -*-

################################################################################
#
# File        : init.py
# Description : defines the classes that represent elements of the simulation
#
# ToDo        : · Rewrite update() to account for tunnelling
#              
################################################################################

import tinr_io # ./tinr_io.py (IO operations)

class Track:
    """
    Our city model: a mathematical graph made of nodes, linked to each other by roads.
    """
   
# Constructor
   
    def __init__(self, newNodes = [], newRoads = []):
        """
        Constructor method: creates a track given the nodes and roads.
            self            : 
            newNodes (list) : a list of the nodes
            newRoads (list) : a list of the roads
        """ 
        # if possible, let's try to avoid copies
        self.nodes = newNodes
        self.roads = newRoads
   
#  Mutators
   
    def addNode(self, newCoordinates):
        """
        Adds a node to the track.
            self                  :
            newCoordinates (list) : coordinates (x, y) for the node
        """
        if (not len(self.nodes)): self.nodes = []
        
        self.nodes += [Node(newCoordinates)]
    
    def addRoad(self, newBegin, newEnd, newLength):
        """
        Adds a road to the track.
            self             :
            newBegin  (node) : starting point for the road
            newEnd    (node) : ending point for the road
            newLength (int)  : road length
        """
        if (not len(self.roads)): self.roads = []
      
        self.roads += [Road(newBegin, newEnd, newLength)]
        newBegin.add_road_leaving(self)
        newEnd.add_road_arriving(self)

################################################################################

class Road:
    "Connection between 2 nodes ; one-way only"

# Constructor
    
    def __init__(self, newBegin, newEnd, length):
        """
        Constructor method: creates a new road.
            self             :
            newBegin  (node) : starting point for the road
            newEnd    (node) : ending point for the road
            newLength (int)  : road length
        """
        self.begin   = newBegin
        self.end     = newEnd
        self.cars    = [] 
        # this list *has* to be  permanently orderer, i think, further reading on issue1 (see http://code.google.com/p/thereisnorush/issues)
        # I think not, see Issue1/Comment1 -- Sharayanan
        
        self.length  = length
        self.gates  = [False, False]
    
    def next(self, pos): 
        #on est francais remi ! tu peux parler dans ce langage, je le comprendrais :-)
        # It wasn't me… 
        
        # Bugged ? This function does not return anything, nor does it acts in any way
        # Planté ? Cette fonction ne retourne rien, ni n'agit d'une manière ou d'une autre
        """
            Returns the next object on the current road
            
            Beginning from the end of the road (position of the node), it browses the list of cars
            to see whether one of them blocks the way. 
            
            Actually there was a mistake, fixed. it should be more understandable now ;-)
        """
        nearest_object = self.length - 1
        for car in self.cars:
            if car.pos > pos: nearest_object = min( car.pos , nearest_object)

    def addCar(self, car_arriving, pos):
        """
            Inserts the arrivingcar at given position in the _ordered_ list of cars
        """

        if (len(self.cars)==0): self.cars = [] # If there's no list, create one!
        
        self.cars += [car_arriving] # Adds a new car to the list
        car_arriving.pos = (pos)    # Sets its position
        car_arriving.road = self    # Tells it it's on the road !

################################################################################

class Node:
    """
    Crossroads of our city ; may host several roads
    """
   
# Constructor
   
    def __init__(self, newCoordinates):
        """
        Constructor method: creates a new node.
            self                  :
            newCoordinates (list) : the coordinates (x, y) for the node
        """
        self.roads         = []
        self.x             = newCoordinates[0]
        self.y             = newCoordinates[1]
        self.roadsComing   = []
        self.roadsLeaving  = []

    def coords(self):
        """
            Returns the current node's coordinates.
        """
        return (self.x, self.y)
     
# Mutators
   
    def add_road_arriving(self, road):
        """
        Adds a road that whose endpoint is this node.
            self        :
            road (road) : the road object that ends here
        """
        self.roadsComing += [road]
    
    def add_road_leaving(self, road):
        """
        Adds a road that departs from this node.
            self        :
            road (road) : the road object that goes from here
        """
        self.roadsLeaving += [road]
    
    def setGate(road, state):
        """
        Sets the state of the gates on the road.
            road  (road) : the road whose gates are affected
            state (int)  : the state (0-1) of the gate
        """
        if (id(road.begin) == id(self)):
            road.gates[0] = state
        else:
            road.gates[1] = state

################################################################################
   
class Car:
    """
    Those which will crowd our city >_<
    """
    
# Path generation
    
    def generatePath(self):
        """
        Assembles random waypoints into a the "path" list
        """
        from random import randint
        
        totalWaypoints  = randint(5, 18)
        path            = []
        
        for i in range(totalWaypoints): path += [randint(1, 100)]
        return path
    
# Constructor
    
    def __init__(self, path, departure_road):
        """
        Constructor method: a car is provided a (for now unmutable) sequence of directions.
            self                  :
            path (list)           : a list of waypoints
            departure_road (road) : the road where the car originates
        
        Définie par la liste de ces directions successives, pour le moment cette liste est fixe.
        """
        self.path = path
        # For now, the cars' speed is either 0 or 100
        # Cette « vitesse » est pour le moment 0 ou 100, ce sont des « point de deplacements »
        self.speed = 0 
        self.pos = 0
        self.road = departure_road
        
    def update(self):
        """
        Updates the car speed and position, manages blocked pathways and queues.
        """
        
        # Needs to be rewritten to account for tunnelling, see Issue1 -- Sharayanan
        
        next_object = self.road.next(self.pos)
        if self.pos + self.speed < next_object:
            self.pos += self.speed
        elif self.pos + self.speed < self.road.length:
            self.pos = next_object -1
        else:
            # Manage the "closed gate" event
            # Gérer le cas du feu rouge
            print "" 

################################################################################
#
#  TESTING ZONE


circuit=Track()
tinr_io.load_track(circuit, "track_default.txt")
circuit.roads[1].addCar(Car([], circuit.roads[2]),80)
circuit.roads[1].addCar(Car([], circuit.roads[1]),30)
circuit.roads[1].addCar(Car([], circuit.roads[1]),130)
