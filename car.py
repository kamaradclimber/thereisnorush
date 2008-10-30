# -*- coding: utf-8 -*-
"""
File        :   car.py
Description :   defines the class "Car"
"""

import init
from random         import randint
import constants    as __constants__
import road         as __road__
import roundabout   as __roundabout__

class Car:
    """
    Those which will crowd our city >_< .
    """

    def __init__(self, new_location, new_type = __constants__.STANDARD_CAR, new_position = 0):
        """
        Constructor method : a car is provided a (for now unmutable) sequence of directions.
            new_path (list)  :   a list of waypoints
            new_road (Road) :   the road where the car originates (for now, let's forbid the original location to be a roundabout)
        """
        self.path               = []
        self.waiting            = False
        self.width              = __constants__.CAR_DEFAULT_WIDTH
        self.speed              = __constants__.CAR_DEFAULT_SPEED 
        self.headway            = __constants__.CAR_DEFAULT_HEADWAY
        self.location           = new_location
        self.position           = new_position
        self.acceleration       = 0
        self.stress             = 0
        self.sight_distance     = 5 * __constants__.CAR_DEFAULT_LENGTH
        self.consecutif_waiting = 0        


        if isinstance(new_location, __road__.Road):
            self.location.cars.insert(0, self)
        else:
            raise ValueError('ERROR (in car.__init__()) : new cars must be created on a road !')
        
        self.generate_path()        
        self.set_car_properties(new_type)

    def set_car_properties(self, new_type):
        """
        Sets the car's properties, given its type
        """
        
        # isn't there a better solution (I miss switch…)
        if new_type == __constants__.STANDARD_CAR:
            self.length = __constants__.CAR_DEFAULT_LENGTH    
            self.force  = __constants__.CAR_DEFAULT_FORCE    
            self.mass   = __constants__.CAR_DEFAULT_MASS    
            self.color  = __constants__.CAR_DEFAULT_COLOR
        
        elif new_type == __constants__.TRUCK:
            self.length =  __constants__.CAR_DEFAULT_LENGTH * 3
            self.force  =  __constants__.CAR_DEFAULT_FORCE  * 5
            self.mass   =  __constants__.CAR_DEFAULT_MASS   * 30            # They're ~30 tons heavy =]
            self.color  =  __constants__.LIGHT_BLUE   # And they're blue !
        
        else:
            raise Exception('ERROR (in car.set_car_properties()): unknown type of vehicle')
            
    def generate_path(self, minimum = 8, maximum = 11):
        """
        Assembles random waypoints into a "path" list.
        """
        self.path = [randint(0, 128) for i in range(randint(minimum, maximum))]
    
    def join(self, new_location, new_position = 0):
        """
        Allocate the car to the given location. The concept of location makes it possible to use this code for either a road or a roundabout.
            new_location    (Road or Roundabout)  :   road or roundabout that will host, if possible, the car
            new_position    (list)          :   position in the road or in the roundabout (note that the meaning of the position depends on the kind of location)
        """
        #   Leave the current location
        if self.location and self in self.location.cars:
            self.location.cars.remove(self)
        else:
            raise Exception("WARNING (in car.join()) : a car had no location !")

        #   Roundabout -> road
        if isinstance(self.location, __roundabout__.Roundabout) and isinstance(new_location, __road__.Road):
            car_slot = init.find_key(self.location.slots_cars, self)
            
            #   Remove car from its slot
            if car_slot is None:
                raise Exception("WARNING (in car.join()) : a car leaving from a roundabout had no slot !")
            else:
                self.location.slots_cars[car_slot] = None

            self.acceleration = self.force/self.mass

        #   Road -> roundabout
        elif isinstance(new_location, __roundabout__.Roundabout) and isinstance(self.location, __road__.Road):
            self.catch_slot(new_location)

        #   Road -> road OR roundabout -> roundabout : ERROR
        else:
            raise Exception('ERROR (in car.join()) : road to road OR roundabout to roundabout junction is forbidden !')
        
        #   Update data
        self.position = new_position
        self.location = new_location
        self.speed = 0
        self.location.cars.insert(0, self) #CONVENTiON SENSITIVE
    
    def catch_slot(self, roundabout):
        """
        Ajoute la voiture sur le carrefour en l'ajoutant sur le slot (supposé vide) en face de la route d'où elle vient
        """
        if self.location in roundabout.slots_roads:
            id_slot = roundabout.slots_roads.index(self.location)
            
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
        #   End of the path
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
            if self.location.gates[__constants__.LEAVING_GATE]:
                obstacle = self.location.length + self.headway
            #   Red light
            else:
                obstacle = self.location.length

            return (obstacle, obstacle_is_light)

        #   Otherwise : the next obstacle is the previous car
        obstacle_is_light = False
        obstacle = self.location.cars[self.rank + 1].position - self.location.cars[self.rank + 1].length/2

        return (obstacle, obstacle_is_light)
    
    def act(self):
        """
        Moves the car, THEN manages its speed, acceleration.
        """
        if not isinstance(self.location, __road__.Road):
            # We only manage cars on roads, we don't care about rndabts
            return None

        (obstacle, obstacle_is_light) = self._next_obstacle()

        #   Update the acceleration given the context
        
        # TEMPORARY : simple version that works, ask Sharayanan for explanations
        # This guarantees that the car will stop at the right location, although this is not 
        # very realistic, but let's focus on physics first -- Sharayanan
        self.sight_distance = (self.speed**2)/(2*self.force/self.mass)
        
        #   No obstacle at sight
        if self.position + self.length/2 + self.sight_distance < obstacle:
            # « 1 trait danger, 2 traits sécurité : je fonce ! »
            self.acceleration = self.force/self.mass

        #   Visible obstacle
        else:
            #   Set the parameters given the kind of obstacle
            if obstacle_is_light:
                delta_speed = - self.speed
            else:
                delta_speed = self.location.cars[self.rank + 1].speed - self.speed  # CONVENTION SENSITIVE
            
            delta_position  = obstacle - self.position - self.length/2 - self.headway
            
            self.acceleration   =   0
            #self.acceleration   +=  __constants__.ALPHA * delta_speed
            #self.acceleration   +=  __constants__.BETA  * delta_position
            #self.acceleration   =   min(self.acceleration, 10)      #   Prevent acceleration from outranging 10
            #self.acceleration   =   max(self.acceleration, -10)     #   Prevent acceleration from outranging -10
            
            # TEMPORARY : Simple version that *works*, ask Sharayanan for explanations
            if delta_speed:
                self.acceleration = self.force/self.mass * delta_speed/abs(delta_speed)
                
        #   Update the position given the speed
        self.position = min(self.position + self.speed * __constants__.delta_t, obstacle - self.length/2 - self.headway)
        
        #   Update the speed given the acceleration
        self.speed = max(min(self.speed + self.acceleration * __constants__.delta_t, self.location.max_speed), 5)

        #   Arrival at a roundabout
        if self.position >= self.location.length - self.length/2 - self.headway:
            #   Green light
            if self.location.gates[__constants__.LEAVING_GATE] :
                id_slot = self.location.end.slots_roads.index(self.location)    #slot in front of the car location
                
                #   The slot doesn't exist : creation of the slot
                if not self.location.end.slots_cars.has_key(id_slot):
                    self.location.end.slots_cars[id_slot] = None
                    
                #   The slot is free
                if self.location.end.slots_cars[id_slot] is None:
                    self.location.end.slots_cars[id_slot]   = self
                    self.waiting                            = False
                    self.join(self.location.end)
                    
                #   The slot isn't free
                else:
                    self.waiting = True
                    
            #   Red light
            else:
                self.waiting = True

        #   Waiting
        if self.position + self.length/2 + self.sight_distance > obstacle: 
            if not obstacle_is_light:
                self.waiting = self.location.cars[self.rank + 1].waiting    # CONVENTION SENSITIVE
            elif self.location.gates[__constants__.LEAVING_GATE]:
                self.waiting = False
            else:
                self.waiting = True
        
        #   experimental - stress
        if self.waiting : 
            self.stress += 1
            self.consecutif_waiting +=1
        else:
            self.consecutif_waiting = 0

    @property
    def rank(self):
        if self in self.location.cars:
            return self.location.cars.index(self)
        else:
            raise Exception("ERROR (in car.rank) : a car is not in her place !")
