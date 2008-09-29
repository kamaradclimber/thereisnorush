#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
File          :   init.py
Description   :   defines the classes and constants needed for the simulation
ToDo          :   · Rewrite update() to account for tunnelling and crossing a node
"""

import tinr_io # ./tinr_io.py (IO operations)

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

#mytrack = Track()
#mytrack.nodes.append(Node(1,2))


class Track:
    """
    Our city model : a mathematical graph made of nodes, linked to each other by roads.
    """
   
    def __init__(self, newNodes=None, newRoads=None):
        """
        Constructor method : creates a track given the nodes and roads.
        :type newNodes: list    newNodes (list) :   a list of the nodes
            newRoads (list) :   a list of the roads
        """ 
        if newNodes is None:
            self.nodes = []
        else:
            self.nodes = newNodes
        if newRoads is None:
            self.roads = []
        else:
            self.roads = newRoads

   
#   Mutators
    
    def createRoad(self, newBegin, newEnd, newLength):
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
        self.length = length
        self.gates  = [False, False]
    
    def avance(self):
        long= len((self.cars))
        for i in range(1,long+1):
            self.cars[-i].update(long-i)

    def addCar(self, newCar, newPosition):
        """
            Inserts a car at given position in the _ordered_ (yes really ordered !) list of cars.
                newCar      (Car)   :   car to be added
                newPosition (float) :   curvilinear abscissa for the car
        """

        if (not len(self.cars)): self.cars = []
        
        self.cars       =  [newCar] + self.cars
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

    @property
    def coords(self):
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
    
    def update(self,rang):
        """
            Updates the car speed and position, manages blocked pathways and queues.
        """

        #TEMPORARY
        delta_t = 0.01
        
        # Needs to be rewritten to account for tunnelling, see Issue1 -- Sharayanan
        
        if rang == len(self.road.cars) -1 : 
            obstacle = None #light
        else:
            obstacle = self.road.cars[rang+1].position 
        
        self.speed = 50
        if self.position + self.speed*delta_t < obstacle:
            self.position += self.speed * delta_t
        elif obstacle != None:
            self.position = obstacle - CAR_WIDTH
            self.speed = 0
        else:
            #on oublie les histoires de feu rouge pour le moment: la voiture s'arrete
            self.position = self.road.length -1
            self.speed = 0
            

################################################################################



#   TESTING ZONE
#if __name__ == '__main__': # pour le moment ceci fait bugger on verra ca après !
track = Track()
tinr_io.load_track(track, "track_default.txt")
print track.roads
track.roads[1].addCar(Car([], track.roads[2]), 80)
track.roads[1].addCar(Car([], track.roads[1]), 30)
track.roads[1].addCar(Car([], track.roads[1]), 130)
