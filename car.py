# -*- coding: utf-8 -*-
"""
File        :   car.py
Description :   defines the class "Car"
"""

import lib


from random         import randint
from constants      import *
import road         as __road__
import roundabout   as __roundabout__

class Car:
    """
    Those which will crowd our city >_< .
    """

    def __init__(self, new_location, new_type = STANDARD_CAR, new_position = 0):
        """
        Constructor method.
        """
        #   Check the vehicle type
        if new_type not in VEHICLE_TYPES:
            raise Exception('ERROR (in car.__init__()) : unknown type of vehicle !')
        
        #   Initialization of the parameters
        self.path               = []
        self.is_waiting         = False
        self.width              = VEHICLE[new_type][DEFAULT_WIDTH]
        self.speed              = VEHICLE[new_type][DEFAULT_SPEED]
        self.headway            = VEHICLE[new_type][DEFAULT_HEADWAY]
        self.length             = VEHICLE[new_type][DEFAULT_LENGTH]
        self.force              = VEHICLE[new_type][DEFAULT_FORCE]
        self.mass               = VEHICLE[new_type][DEFAULT_MASS]
        self.color              = VEHICLE[new_type][DEFAULT_COLOR]
        self.location           = new_location
        self.position           = new_position
        self.acceleration       = 0
        self.sight_distance     = 5 * VEHICLE[STANDARD_CAR][DEFAULT_LENGTH]
        self.total_waiting_time = 0
        self.last_waiting_time  = 0
        
        #   Several sub-categories : truck, long truck, bus
        if new_type == TRUCK:
            possible_sizes = [(2, 25), 
                              (3, 60), 
                              (4, 15)]
        
            self.length *= lib.proba_poll(possible_sizes)
            self.mass   *= self.length
        
        #   Cars must be created on a lane
        if isinstance(new_location, __road__.Lane):
            self.location.cars.insert(0, self)
        else:
            raise ValueError('ERROR (in car.__init__()) : new cars must be created on a lane !')
        
        self.generate_path()        
    
    def generate_path(self, minimum = 8, maximum = 11):
        """
        Assembles random waypoints into a "path" list.
        """
        self.path = [randint(0, 128) for i in range(randint(minimum, maximum))]
    
    def join(self, new_location, new_position = 0):
        """
        Allocate the car to the given location. The concept of location makes it possible to use this code for either a lane or a roundabout.
            new_location    (road or lane or Roundabout)  :   lane or roundabout that will host, if possible, the car
            new_position    (list)          :   position in the lane or in the roundabout (note that the meaning of the position depends on the kind of location)
        """
        #   Leave the current location
        if self.location is not None and self in self.location.cars:
            self.location.cars.remove(self)
        else:
            raise Exception("WARNING (in car.join()) : a car had no location !")

        #   Roundabout -> Lane
        if isinstance(self.location, __roundabout__.Roundabout) and isinstance(new_location, __road__.Lane):
            car_slot = lib.find_key(self.location.slots_cars, self)
            
            #   Remove car from its slot
            if car_slot is None:
                raise Exception("WARNING (in car.join()) : a car leaving from a roundabout had no slot !")
            else:
                self.location.slots_cars[car_slot] = None

            self.acceleration = self.force/self.mass

        #   Lane -> roundabout
        elif isinstance(new_location, __roundabout__.Roundabout) and isinstance(self.location, __road__.Lane):
            self.catch_slot(new_location)

        #   Lane -> lane OR roundabout -> roundabout : ERROR
        else:
            raise Exception('ERROR (in car.join()) : road to road OR roundabout to roundabout junction is forbidden !')
        
        #   Update data
        self.position = new_position
        self.location = new_location
        self.speed = 0
        self.location.cars.insert(0, self) #CONVENTION SENSITIVE
    
    def catch_slot(self, roundabout):
        """
        Ajoute la voiture sur le carrefour en l'ajoutant sur le slot (supposé vide) en face de la route d'où elle vient
        """
        if self.location.parent in roundabout.slots_roads:
            id_slot = roundabout.slots_roads.index(self.location.parent)
            
            if roundabout.slots_cars.has_key(id_slot):
                if roundabout.slots_cars[id_slot] is None:
                    roundabout.slots_cars[id_slot] = self
                elif roundabout.slots_cars[id_slot] == self:
                     #print "WARNING (in car.catch_slot()) : a car tries to join the slot where it is already !"
                     pass
                else:
                    raise Exception("ERROR (in car.catch_slot()) : a slot should be empty, but is not !")
            else:
                roundabout.slots_cars[id_slot] = self
                raise Exception("WARNING (in car.catch_slot()) : a slot should have been initialized, but was not !")
        else:
            raise Exception("ERROR (in car.catch_slot()) : a road has no slot !")

    def die(self):
        """
        Kills the car, which simply disappears.
        """
        if self.location.cars:
            if self in self.location.cars:
                self.location.cars.remove(self)
            else:
                raise Except("WARNING (in car.die()) : a car was not in its place !")
    
    def next_way(self, read_only = True):
        """
        Expresses the cars' wishes :P
        """
        #   End of path
        if len(self.path) == 0:
            return None
        else:
            next = self.path[0]
            if not read_only:
                del self.path[0]
            return next

    def _next_obstacle(self):
        """
        Returns the position of the obstacle ahead of the car, (obstacle, obstacle_is_light)
        """
        #   The car is the first of the queue : the next obstacle is the light
        if self.rank >= len(self.location.cars) - 1:
            obstacle_is_light = True

            #   Green light
            if self.location.parent.traffic_lights[EXIT]:
                obstacle = self.location.parent.length + self.headway
            #   Red light
            else:
                obstacle = self.location.parent.length

            return (obstacle, obstacle_is_light)

        #   Otherwise : the next obstacle is the previous car
        obstacle_is_light = False
        obstacle = self.location.cars[self.rank + 1].position - self.location.cars[self.rank + 1].length/2

        return (obstacle, obstacle_is_light)
    
    def act(self, delay):
        """
        Moves the car, THEN manages its speed, acceleration.
        """
        #   We only manage cars on roads, we don't care about roundabouts
        if not isinstance(self.location, __road__.Lane):
            return None

        (obstacle, obstacle_is_light) = self._next_obstacle()

        #   Update the acceleration given the context
        self.sight_distance = (self.speed**2)/(2*self.force/self.mass)
        
        #   No obstacle at sight : « 1 trait danger, 2 traits sécurité : je fonce ! »
        if self.position + self.length/2 + self.sight_distance < obstacle:
            self.acceleration = self.force/self.mass

        #   Visible obstacle
        else:
            #   Set waiting attitude
            if not obstacle_is_light:
                self.change_waiting_attitude(self.location.cars[self.rank + 1].is_waiting)    # CONVENTION SENSITIVE
            elif self.location.parent.traffic_lights[EXIT]:
                self.change_waiting_attitude(False)
            else:
                self.change_waiting_attitude(True)
            
            #   Start deceleration
            if obstacle_is_light:
                delta_speed = - self.speed
            else:
                delta_speed = self.location.cars[self.rank + 1].speed - self.speed  # CONVENTION SENSITIVE
            
            delta_position  = obstacle - self.position - self.length/2 - self.headway
            
            self.acceleration = 0
            
            if delta_speed:
                self.acceleration = self.force/self.mass * delta_speed/abs(delta_speed)
                
        #   Update the position and speed given the speed and acceleration
        self.position   = min(self.position + self.speed * delay, obstacle - self.length/2 - self.headway)
        self.speed      = max(min(self.speed + self.acceleration * delay, self.location.parent.max_speed), 5)

        #   Arrival at a roundabout
        if self.position >= self.location.parent.length - self.length/2 - self.headway:
            #   Green light
            if self.location.parent.traffic_lights[EXIT] :
                id_slot = self.location.parent.end.slots_roads.index(self.location.parent)    #slot in front of the car location
                
                #   The slot doesn't exist : creation of the slot
                if not self.location.parent.end.slots_cars.has_key(id_slot):
                    self.location.parent.end.slots_cars[id_slot] = None
                    
                #   The slot is free
                if self.location.parent.end.slots_cars[id_slot] is None:
                    self.location.parent.end.slots_cars[id_slot] = self
                    self.change_waiting_attitude(False)
                    self.join(self.location.parent.end)
                    
                #   The slot isn't free
                else:
                    self.change_waiting_attitude(True)
                    
            #   Red light
            else:
                self.change_waiting_attitude(True)

    def change_waiting_attitude(self, new_attitude):
        """
        Changes, if needed, the waiting attitude of a car
        """
        #   There is no change : do nothing
        if new_attitude == self.is_waiting:
            return None
        
        #   Start a "waiting" phase : reset the counter
        if new_attitude:
            self.is_waiting         = True
            self.start_waiting_time = lib.clock()
            self.last_waiting_time  = 0
        
        #   Stop a "waiting" phase : look at the clock
        else:
            self.is_waiting         = False
            self.last_waiting_time  = lib.clock() - self.start_waiting_time
            self.total_waiting_time += self.last_waiting_time
            
    @property
    def rank(self):
        if self in self.location.cars:
            return self.location.cars.index(self)
        else:
            raise Exception("ERROR (in car.rank) : a car is not in her place !")
