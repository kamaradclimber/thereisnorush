#  TODO  #######################################################################
#
#  Comment on the code
#  Change the file name, from "main.py" to "init.py" for example
#  Choose an indent scheme (I'd rather a 3 whitespaces tab)
#  I think we should rename "fires" or "lights" into "gates" (quite more semantic)
#
################################################################################

class Track:
   "Our city model : a mathematical graph made of nodes linked to each other by roads"
   
#  Constructor #################################################################
   
    def __init__(self, newNodes = [], newRoads = []): # TODO : check if the default arguments are given by copy or by reference
        self.nodes = newNodes
        self.roads = newRoads
   
#  Mutators ####################################################################
   
    def addNode(self, newCoordinates):
        if (not len(self.nodes)):
            self.nodes = []
      
        self.nodes += [Node(newCoordinates)]
    
   def addRoad(self, newBegin, newEnd, newLength):
        if (not len(self.roads)):
            self.roads = []
      
        self.roads += [Road(newBegin, newEnd, newLength)]
        newBegin.add_road_leaving(self)
        newEnd.add_road_arriving(self)

################################################################################

class Road:
    "Connection between 2 nodes ; has a unique direction"

#  Constructor #################################################################
    
    def __init__(self, newBegin, newEnd, length):
        self.begin   = newBegin
        self.end     = newEnd
        self.cars    = []
        self.length  = length
        self.lights  = [False, False]
    
################################################################################
    
    def next(self, pos): # Please comment on this method, I can't understand it
        plus_proche_obstacle = self.length-1
        for car in self.cars:
            plus_proche_obstacle = min(car.pos, plus_proche_obstacle)

class Node:
   "Crossroads of our city ; can host several roads"
   
#  Constructor #################################################################
   
    def __init__(self, newCoordinates):
        self.roads         = []
        self.x             = newCoordinates[0]
        self.y             = newCoordinates[1]
        self.roadsComing   = []
        self.roadsLeaving  = []
     
#  Mutators ####################################################################
   
    def add_road_ariving(self, road):
        self.roadsComing += [road]
    
    def add_road_leaving(self, road):
        self.roadsLeaving += [road]
    
    def setFire(road, state):
        if (id(road.begin) == id(self)):
            road.lights[0] = state
        else:
            road.lights[1] = state

################################################################################
   
class Car:
    "Those which will crowd our city >_<"
    
#  Path generation   ###########################################################
    
    def generatePath():
        from random import randint
        
        totalWaypoints  = randint(5, 18)
        path            = []
        
        for i in range(totalWaypoints):
            path += [randint(1, 100)]
        return path
    
#  Constructor #################################################################
    
    def __init__(self, path, departure_road):
        "definie par la liste de ces directions successives, pour le moment cette liste est fixe "
        self.path = path
        self.speed = 0 # cette 'vitesse' est pour le moment 0 ou 100, ce sont des 'point de deplacements'
        self.pos = 0
        self.road = departure_road
    def avance(self):
        prochain_obstacle = self.road.next(self.pos)
        if self.pos + self.speed < prochain_obstacle:
            self.pos += self.speed
        elif self.pos + self.speed < self.road.length:
            self.pos = prochain_obstacle -1
        else:
            print "" #gerer le cas du feu rouge

circuit=Track()

circuit.addNode((10, 10))
circuit.addNode((50, 10))
circuit.addNode((10, 50))
circuit.addRoad(circuit.nodes[0], circuit.nodes[1], 150)
circuit.addRoad(circuit.nodes[1], circuit.nodes[2], 150)
circuit.addRoad(circuit.nodes[2], circuit.nodes[0], 150)