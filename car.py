# -*- coding: utf-8 -*-
"""
File        :   car.py
Description :   defines the class "Car"
"""

import constants    as __constants__
import init
from random         import randint
import road         as __road__
import roundabout   as __roundabout__

class Car:
    """
    Those which will crowd our city >_< .
    """

    def __init__(self, new_location, new_position = 0):
        """
        Constructor method : a car is provided a (for now unmutable) sequence of directions.
            new_path (list)  :   a list of waypoints
            new_road (Road) :   the road where the car originates (for now, let's forbid the original location to be a roundabout)
        headway: Desired headway to the preceding car / Distance souhaitée par rapport à la voiture devant
        Définie par la liste de ses directions successives, pour le moment cette liste est fixe.
        """
        self.path               = []
        self.waiting            = False
        self.length             = __constants__.CAR_DEFAULT_LENGTH
        self.width              = __constants__.CAR_DEFAULT_WIDTH
        self.speed              = __constants__.CAR_DEFAULT_SPEED 
        self.position           = new_position               
        self.headway            = __constants__.CAR_DEFAULT_HEADWAY
        self.color              = __constants__.CAR_DEFAULT_COLOR 
        self.acceleration       = __constants__.CAR_DEFAULT_ACCEL     
        self.location           = new_location
        self.stress             = 0
        self.sight_distance     = 5 * __constants__.CAR_DEFAULT_LENGTH
        self.consecutif_waiting = 0 #ca sera utile: si jattend trop longtemps, jai envie de changer de trajet et de recalculer le trajet pour aller à mon objectif

        if isinstance(new_location, __road__.Road):
            self.location.cars.insert(0, self)
        else:
            raise ValueError('ERROR (in car.__init__()) : new cars must be created in a road !') # An "ERROR" is a problem that cannot be ignored : the program must then halt
        
        self.generate_path()
    
    def generate_path(self, minimum = 5, maximum = 8):
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
            print "WARNING (in car.join()) : a car had no location !"
        
        #   Each time a car joins or leaves a roundabout, this one has to update in order to calculate again the best configuration for the gates

        #   Roundabout -> road
        if isinstance(self.location, __roundabout__.Roundabout) and isinstance(new_location, __road__.Road):
            car_slot = init.find_key(self.location.slots_cars, self)
            
            #   Remove car from its slot
            if car_slot is None:
                raise Exception("WARNING (in car.join()) : a car leaving from a roundabout had no slot !")
            else:
                self.location.slots_cars[car_slot] = None

            self.location.update_gates()
            self.acceleration = __constants__.CAR_DEFAULT_ACCEL

        #   Road -> roundabout
        elif isinstance(new_location, __roundabout__.Roundabout) and isinstance(self.location, __road__.Road):
            self.catch_slot(new_location)
            # new_location.update_gates()  -but this not  to you to do this

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
                print "WARNING (in car.catch_slot()) : a slot should have been initialized, but was not !"
        else:
            raise Exception("ERROR (in car.catch_slot()) : a road has no slot !")

    def die(self):
        """
        Kills the car, which simply disappear.
        """
        if self.location.cars:
            if self in self.location.cars:
                self.location.cars.remove(self)
                #__constants__.angriness_mean += self.stress
                #__constants__.nb_died += 1
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
        Returns the position of the obstacle ahead of the car
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
            return None

        (obstacle, obstacle_is_light) = self._next_obstacle()

        #   Update the acceleration given the context
        
        # TEMPORARY : simple version that works, ask Sharayanan for explanations
        # This guarantees that the car will stop at the right location, although this is not 
        # very realistic, but let's focus on physics first -- Sharayanan
        self.sight_distance = (self.speed**2)/(2*__constants__.CAR_DEFAULT_ACCEL)
        
        #   No obstacle at sight
        if self.position + self.length/2 + self.sight_distance < obstacle:
            # « 1 trait danger, 2 traits sécurité : je fonce ! »
            self.acceleration = __constants__.CAR_DEFAULT_ACCEL

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
                self.acceleration = __constants__.CAR_DEFAULT_ACCEL * delta_speed/abs(delta_speed)
                
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
