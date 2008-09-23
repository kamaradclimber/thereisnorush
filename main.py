class Circuit:
    def __init__(self,roads_list):
      self.roads = roads_list

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
    def __init__(self, coord):
        self.roads = []
        self.coordinates= coord

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


r1=Road((1,1),(1,2),3)
r2=Road((1,2),(2,2),3)
r3=Road((2,2),(1,1),3)
c1=Node((1,1))
c2=Node((1,2))
c3=Node((2,2))
circuit=Circuit([r1,r2,r3])