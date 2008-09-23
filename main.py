

class Road:
   "Porte très bien son nom"
   
   def __init__(self, newBegin, newEnd, length):
   """
      newCoordinates est un couple de carrefours
   """
   
      self.begin  = newBegin
      self.end    = newEnd
      self.cars   = []
      self.length = length
      self.fires  = [False, False]
   
class Carrefour
   ""
   def __init__(self, newRoads):
   """
      
   """
   
      self.roads = newRoads
   
   def setFire(road, state):
   """
   
   """
   
      if (id(road.begin) == id(self)):
         road.fires[0] = state
      else
         road.fires[1] = state
   
class Car
   ""
   
   def __init__(self, newBegin, newEnd, length):
   """
      
   """