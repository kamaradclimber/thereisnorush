#!/usr/local/bin/python
# -*- coding: utf-8 -*-

################################################################################
#
# File          :   init.py
# Description   :   defines the classes and constants needed for the simulation
#
# ToDo          :   · Rewrite update() to account for tunnelling and crossing a node
#              
################################################################################

import tinr_io # ./tinr_io.py (IO operations)

class Track:
    """
        Our city model : a mathematical graph made of nodes, linked to each other by roads.
    """
   
#   Constructor
   
    def __init__(self, newNodes = [], newRoads = []):
        """
            Constructor method : creates a track given the nodes and roads.
                newNodes (list) :   a list of the nodes
                newRoads (list) :   a list of the roads
        """ 
        
        # if possible, let's try to avoid copies
        self.nodes = newNodes
        self.roads = newRoads
   
#   Mutators
   
    def addNode(self, newCoordinates):
        """
            Adds a node to the track.
                newCoordinates (list)   :   coordinates [x, y] for the node
        """
        
        if (not len(self.nodes)): self.nodes = []
        
        self.nodes += [Node(newCoordinates)]
    
    def addRoad(self, newBegin, newEnd, newLength):
        """
            Adds a road to the track.
                newBegin  (Node)    :   starting point for the road
                newEnd    (Node)    :   ending point for the road
                newLength (int)     :   road length
        """
        
        if (not len(self.roads)): self.roads = []
      
        self.roads += [Road(newBegin, newEnd, newLength)]
        newBegin.addRoad(self, False)
        newEnd.addRoad(self, True)

################################################################################

class Road:
    """
        Connection between 2 nodes ; one-way only.
    """

#   Constructor
    
    def __init__(self, newBegin, newEnd, length):
        """
            Constructor method : creates a new road.
                newBegin  (Node)    : starting point for the road
                newEnd    (Node)    : ending point for the road
                newLength (int)     : road length
        """
        
        self.begin  = newBegin
        self.end    = newEnd
        self.cars   = [] 
        # this list *has* to be  permanently orderer, i think, further reading on issue1 (see http://code.google.com/p/thereisnorush/issues)
        # I think not, see Issue1/Comment1 -- Sharayanan
        
        self.length = length
        self.gates  = [False, False]
    
    def nextObstacle(self, position):
        # Bugged ? This function does not return anything, nor does it acts in any way
        # Planté ? Cette fonction ne retourne rien, ni n'agit d'une manière ou d'une autre
        #   I've added the return value -- Ch@hine
        """
            Returns the next object on the current road
            
            Beginning from the end of the road (position of the node), it browses the list of cars
            to see whether one of them blocks the way. 
            
            Actually there was a mistake, fixed. it should be more understandable now ;-)
                position  ()    :   
        """
        
        nearestObject = self.length - 1
        for car in self.cars:
            if car.position > position: nearestObject = min(car.position , nearestObject)
        
        return nearestObject

    def addCar(self, newCar, newPosition):
        """
            Inserts a car at given position in the _ordered_ list of cars.
                newCar      (Car)   :   car to be added
                newPosition (float) :   curvilinear abscissa for the car
        """
        #   "newCar" should really be a pointer ; I've read that almost all functions parameters are taken by Python by reference ; is that true ? Or should I specify something in the code ? -- Ch@hine

        if (not len(self.cars)): self.cars = []
        
        self.cars       +=  [newCar]
        newCar.position =   newPosition
        newCar.road     =   self

################################################################################

class Node:
    """
        Crossroads of our city ; may host several roads.
    """
   
# Constructor
   
    def __init__(self, newCoordinates):
        """
            Constructor method : creates a new node.
                newCoordinates (list) : the coordinates [x, y] for the node
        """
        self.roads         = []
        self.x             = newCoordinates[0]
        self.y             = newCoordinates[1]
        self.roadsComing   = []
        self.roadsLeaving  = []

#   Accessors

    def getX(self):
        """
            Returns the current node's abscissa.
        """
        return (self.x)
    
    def getY(self):
        """
            Returns the current node's ordinate.
        """
        return (self.y)
    
    def getCoordinates(self):
        """
            Returns the current node's coordinates.
        """
        return (self.x, self.y)
    
#   Mutators
   
    def addRoad(self, road, isComing):
        """
            Connect a road to this node.
                road        (Road)  :   the road object to be connected
                isComing    (bool)  :   True if the roads comes to this node, False otherwise
        """
        
        if isComing:
            self.roadsComing    += [road]
        else:
            self.roadsLeaving   += [road]
    
    def setGate(self, road, state):
        """
            Sets the state of the gates on the road.
                road    (Road)  :   the road whose gates are affected
                state   (int)   :   the state (0 = closed, 1 = opened) of the gate
        """
        
        if (id(road.begin) == id(self)):
            road.gates[0] = state
        else:
            road.gates[1] = state

################################################################################

class Car:
    """
        Those which will crowd our city >_< .
    """
    
#   Path generation
    
    def generatePath(self):
        """
            Assembles random waypoints into a "path" list
        """
        
        from random import randint
        
        totalWaypoints  = randint(5, 18)
        path            = []
        
        for i in range(totalWaypoints):
            path += [randint(1, 100)]
        
        return path
    
#   Constructor
    
    def __init__(self, newPath, newRoad):
        """
            Constructor method : a car is provided a (for now unmutable) sequence of directions.
                newPath (list)  :   a list of waypoints
                newRoad (Road)  :   the road where the car originates
            
            Définie par la liste de ses directions successives, pour le moment cette liste est fixe.
        """
        
        self.path       = newPath
        # For now, the cars' speed is either 0 or 100
        # Cette « vitesse » est pour le moment 0 ou 100, ce sont des « point de deplacements »
        self.speed      = 0
        self.position   = 0
        self.road       = newRoad
    
    def update(self):
        """
            Updates the car speed and position, manages blocked pathways and queues.
        """
        
        # Needs to be rewritten to account for tunnelling, see Issue1 -- Sharayanan
        
        obstacle = self.road.nextObstacle(self.position)
        
        if self.position + self.speed < obstacle:
            self.position = self.speed
        else:
            self.position += obstacle - 1
            #   To do : how the car will cross the node to reach another road

################################################################################

#   Useful constants

BLACK       = (  0,   0,   0)
RED         = (255,   0,   0)
GREEN       = (  0, 255,   0)
BLUE        = (  0,   0, 255)
WHITE       = (255, 255, 255)

LIGHT_RED   = (255,  64,  64)
LIGHT_GREEN = ( 64, 255,  64)
LIGHT_BLUE  = ( 64,  64, 255)

RESOLUTION  = (WINDOW_WIDTH, WINDOW_HEIGHT) = (500, 500)

NODE_WIDTH  = 4
NODE_HEIGHT = 4
NODE_COLOR  = RED

CAR_WIDTH   = 4
CAR_HEIGHT  = 4
CAR_COLOR   = GREEN

ROAD_COLOR  = WHITE

#   TESTING ZONE

track = Track()
tinr_io.load_track(track, "track_default.txt")

track.roads[1].addCar(Car([], track.roads[2]), 80)
track.roads[1].addCar(Car([], track.roads[1]), 30)
track.roads[1].addCar(Car([], track.roads[1]), 130)
