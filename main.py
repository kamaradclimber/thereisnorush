class Track:
   "City model"
   
   def __init__(self, newNodes = [], newRoads = []): # TODO : check if the default arguments are given by copy or by reference
      self.nodes = newNodes
      self.roads = newRoads
   
   def addNode(self, newCoordinates):
      if (not len(self.nodes)):
         self.nodes = []
      
      self.nodes += [Node(newCoordinates)]
   
   def addRoad(self, newBegin, newEnd, newLength):
      if (not len(self.roads)):
         self.roads = []
      
      self.roads += [Road(newBegin, newEnd, newLength)]

class Road:
    "Connection between 2 nodes ; has a unique direction"
    
    def __init__(self, newBegin, newEnd, length):
        "donner les deux points de coordonnees des carrefours de depart et d'arrivee"
        self.begin  = newBegin
        self.end    = newEnd
        self.cars   = []
        self.length = length
        self.fires  = [False, False]
    def next(self,pos):
        plus_proche_obstacle = self.length-1
        for car in self.cars:
            plus_proche_obstacle = min(car.pos,plus_proche_obstacle)


class Node:
    def __init__(self, newCoordinates):
        self.roads = []
        self.x= newCoordinates[0]
        self.y= newCoordinates[1]

    def setFire(road, state):
        if (id(road.begin) == id(self)):
            road.fires[0] = state
        else:
            road.fires[1] = state
   
class Car:
    ""
    def __init__(self,path,departure_road):
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