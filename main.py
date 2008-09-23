class Circuit:
   def __init__(self, newNodes, newRoads):
      self.nodes = newNodes
      self.roads = newRoads

class Road:
    "Porte tres bien son nom"
    
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



c1=Node((10, 10))
c2=Node((50,10))
c3=Node((10,50))
r1=Road(c1,c2,3)
r2=Road(c2,c3,3)
r3=Road(c3,c1,3)
circuit=Circuit([c1, c2, c3], [r1, r2, r3])