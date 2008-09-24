#  TODO  #######################################################################
#
#
################################################################################

class Track:
   "Our city model : a mathematical graph made of nodes linked to each other by roads"
   
#  Constructor #################################################################
   
    def __init__(self, newNodes = [], newRoads = []):
        """
        Constructor method: creates a track given the nodes and roads.
            self            : 
            newNodes (list) : 
            newRoads (list) :
        """ 
        # The arguments are cloned
        self.nodes = newNodes.copy()
        self.roads = newRoads.copy()
   
#  Mutators ####################################################################
   
    def addNode(self, newCoordinates):
        """
        Adds a node to the track.
            self                  :
            newCoordinates (list) :
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
        if (not len(self.roads)):
            self.roads = []
      
        self.roads += [Road(newBegin, newEnd, newLength)]
        newBegin.add_road_leaving(self)
        newEnd.add_road_arriving(self)

################################################################################

class Road:
    "Connection between 2 nodes ; one-way only"

#  Constructor #################################################################
    
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
        self.length  = length
        self.gates  = [False, False]
    
################################################################################
    
    def next(self, pos): # Please comment on this method, I can't understand it
        """
        """
        nearest_object = self.length - 1
        for car in self.cars:
            nearest_object = min(car.pos, nearest_object)

class Node:
   "Crossroads of our city ; may host several roads"
   
#  Constructor #################################################################
   
    def __init__(self, newCoordinates):
        """
        Constructor method: creates a new node.
            self                  :
            newCoordinates (list) :
        """
        self.roads         = []
        self.x             = newCoordinates[0]
        self.y             = newCoordinates[1]
        self.roadsComing   = []
        self.roadsLeaving  = []
     
#  Mutators ####################################################################
   
    def add_road_arriving(self, road):
        """
        Adds a road that whose endpoint is this node.
            self        :
            road (road) :
        """
        self.roadsComing += [road]
    
    def add_road_leaving(self, road):
        """
        Adds a road that departs from this node.
            self        :
            road (road) :
        """
        self.roadsLeaving += [road]
    
    def setGate(road, state):
        """
        Sets the state of the gates on the road.
            road  (road) :
            state (int)  :
        """
        if (id(road.begin) == id(self)):
            road.gates[0] = state
        else:
            road.gates[1] = state

################################################################################
   
class Car:
    "Those which will crowd our city >_<"
    
#  Path generation   ###########################################################
    
    def generatePath():
        """
        Assembles random waypoints into a the "path" list
        """
        from random import randint
        
        totalWaypoints  = randint(5, 18)
        path            = []
        
        for i in range(totalWaypoints): path += [randint(1, 100)]
        return path
    
#  Constructor #################################################################
    
    def __init__(self, path, departure_road):
        """
        Constructor method: a car is provided a (for now unmutable) sequence of directions.
            self                  :
            path (list)           :
            departure_road (road) :
        
        Définie par la liste de ces directions successives, pour le moment cette liste est fixe.
        """
        self.path = path
        # For now, the cars' speed is either 0 or 100
        self.speed = 0 # cette 'vitesse' est pour le moment 0 ou 100, ce sont des 'point de deplacements'
        self.pos = 0
        self.road = departure_road
        
    def update(self):
        """
        Updates the car speed and position, manages blocked pathways and queues.
        """
        next_object = self.road.next(self.pos)
        if self.pos + self.speed < next_object:
            self.pos += self.speed
        elif self.pos + self.speed < self.road.length:
            self.pos = next_object -1
        else:
            # Manage the "closed gate" event
            print "" #gerer le cas du feu rouge

circuit=Track()

circuit.addNode((10, 10))
circuit.addNode((50, 10))
circuit.addNode((10, 50))
circuit.addRoad(circuit.nodes[0], circuit.nodes[1], 150)
circuit.addRoad(circuit.nodes[1], circuit.nodes[2], 150)
circuit.addRoad(circuit.nodes[2], circuit.nodes[0], 150)