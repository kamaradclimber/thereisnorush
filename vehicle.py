# -*- coding: utf-8 -*-
"""
File        :   vehicle.py
Description :   defines the class "Car"
"""

import lib

from random         import randint, choice
from constants      import *
import gps          as __gps__
import road         as __road__
import roundabout   as __roundabout__

class Vehicle:
    """
    Those which will crowd our city >_< .
    """

    def __init__(self, new_location, new_type = STANDARD_CAR, new_length_covered = 0):
        """
        Constructor method.
        """
        
        #   Check the vehicle type
        if new_type not in VEHICLE_TYPES:
            raise Exception('ERROR (in vehicle.__init__()) : unknown type of vehicle !')
        
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
        self.sight_distance     = 5 * VEHICLE[STANDARD_CAR][DEFAULT_LENGTH]
        self.acceleration       = 0
        self.total_waiting_time = 0
        self.last_waiting_time  = 0
        self.dead               = False
        self.gps                = __gps__.Gps()
        self.destination        = None

        #   Several sub-categories : truck, long truck, bus
        if new_type == TRUCK:
            possible_sizes = [(2, 25), 
                              (3, 60), 
                              (4, 15)]
        
            self.length *= lib.proba_poll(possible_sizes)
            self.mass   *= self.length
        
        #   Cars must be created on a lane
        if isinstance(new_location, __road__.Lane):
            self.location = new_location
        else:
            raise ValueError('ERROR (in vehicle.__init__()) : new vehicles must be created on a lane !')
        
        self.location.vehicles.insert(0, self)
        self.length_covered = new_length_covered
        
        self.generate_path()        
    
    def generate_path(self, new_destination = None):
        """
        Find (or not) the path to the given (or not) destination.
        """
        
        #   Set the destination
        if isinstance(new_destination, __roundabout__.Roundabout) and new_destination in self.track.roundabouts:
            destination = new_destination
        else:
            # EXPERIMENTAL : leaving nodes only
            destination = choice([roundabout for roundabout in self.track.roundabouts if len(roundabout.parents)])
        
        #   Compute the path
        #   Each vehicle needs its own gps instance to avoid collisions and clean pathfinding
        self.path = self.gps.find_path(self.lane.start, destination)
        
        self.destination = None 
        if self.path and len(self.path):
            self.destination = destination
    
    def join(self, new_location):
        """
        Allocate the vehicle to the given location. The concept of location makes it possible to use this code for either a lane or a roundabout.
            new_location    (road or lane or Roundabout)  :   lane or roundabout that will host, if possible, the vehicle
        """
        #   Leave the current location
        if (self.location is not None) and (self in self.location.vehicles):
            self.location.vehicles.remove(self)
        else:
            raise Exception("WARNING (in vehicle.join()) : a vehicle had no location !")

        #   Roundabout -> Road
        if isinstance(self.location, __roundabout__.Roundabout) and isinstance(new_location, __road__.Road):
            #   Remove vehicle from its slot
            if self.slot is None:
                raise Exception("WARNING (in vehicle.join()) : a vehicle leaving from a roundabout had no slot !")
            else:
                self.roundabout.slots_vehicles[self.slot] = None

            self.acceleration   = self.force/self.mass
            next_roundabout     = new_location.other_extremity(self.location)
            self.location       = new_location.get_lane_to(next_roundabout)
            if self.location is None:
                raise Exception('problem')# TODO !

        #   Lane -> roundabout
        elif isinstance(new_location, __roundabout__.Roundabout) and isinstance(self.location, __road__.Lane):
            self.catch_slot(new_location)
            self.location       = new_location

        #   Lane -> lane OR roundabout -> roundabout : ERROR
        else:
            raise Exception('ERROR (in vehicle.join()) : road to road OR roundabout to roundabout junction is forbidden !')
        
        #   Update data
        self.length_covered = 0
        self.speed          = 0
        self.location.vehicles.insert(0, self)  # CONVENTION SENSITIVE
    
    def catch_slot(self, roundabout):
        """
        Ajoute la voiture sur le vehiclerefour en l'ajoutant sur le slot (supposé vide) en face de la route d'où elle vient
        """

        if (self.road is not None) and (self.road in roundabout.slots_roads):
            id_slot = roundabout.slots_roads.index(self.road)
            
            if roundabout.slots_vehicles.has_key(id_slot):
                if roundabout.slots_vehicles[id_slot] is None:
                    roundabout.slots_vehicles[id_slot] = self
                elif roundabout.slots_vehicles[id_slot] == self:
                     #print "WARNING (in vehicle.catch_slot()) : a vehicle tries to join the slot where it is already !"
                     pass
                else:
                    raise Exception("ERROR (in vehicle.catch_slot()) : a slot should be empty, but is not !")
            else:
                roundabout.slots_vehicles[id_slot] = self
                raise Exception("WARNING (in vehicle.catch_slot()) : a slot should have been initialized, but was not !")
        else:
            raise Exception("ERROR (in vehicle.catch_slot()) : a road has no slot !")

    def die(self):
        """
        Kills the vehicle, which simply disappears.
        """

        if self.location.vehicles:
            if self in self.location.vehicles:
                self.dead = True 
                self.location.vehicles.remove(self)
            else:
                raise Except("WARNING (in vehicle.die()) : a vehicle was not in its place !")
    
    def next_way(self, read_only = True):
        """
        Expresses the vehicles' wishes :P
        """
        #   End of path
        
        if self.path is None or not len(self.path):
            return None
        else:
            next = self.path[0]
            if not read_only:
                del self.path[0]
            if len(self.path) == 0:
                self.path = None 
                
            return next

    def _next_obstacle(self):
        """
        Returns the position of the obstacle ahead of the vehicle, (obstacle, obstacle_is_light)
        """

        if self.road is not None:
            #   The vehicle is the first of the queue : the next obstacle is the light
            if self.rank >= len(self.lane.vehicles) - 1:    # CONVENTION SENSITIVE
                obstacle_is_light = True
    
                #   Green light
                if self.lane.light(EXIT):
                    obstacle = self.road.length + self.headway
                
                #   Red light
                else:
                    obstacle = self.road.length
    
                return (obstacle, obstacle_is_light)
    
            #   Otherwise : the next obstacle is the previous vehicle
            obstacle_is_light = False
            obstacle = self.lane.vehicles[self.rank + 1].length_covered - self.lane.vehicles[self.rank + 1].length/2
    
            return (obstacle, obstacle_is_light)
        
        return None

    def act(self):
        """
        Moves the vehicle, THEN manages its speed, acceleration.
        """

        #   We only manage vehicles on roads, we don't vehiclee about roundabouts
        if not isinstance(self.location, __road__.Lane):
            return None

        (obstacle, obstacle_is_light) = self._next_obstacle()

        #   Update the acceleration given the context
        self.sight_distance = (self.speed**2)/(2*self.force/self.mass)
        
        #   No obstacle at sight : « 1 trait danger, 2 traits sécurité : je fonce ! »
        if self.length_covered + self.length/2 + self.sight_distance < obstacle:
            self.acceleration = self.force/self.mass

        #   Visible obstacle
        else:
            #   Set waiting attitude
            if not obstacle_is_light:
                self.change_waiting_attitude(self.lane.vehicles[self.rank + 1].is_waiting)    # CONVENTION SENSITIVE
            elif self.lane.light(EXIT):
                self.change_waiting_attitude(False)
            else:
                self.change_waiting_attitude(True)
            
            #   Start deceleration
            if obstacle_is_light:
                delta_speed = - self.speed
            else:
                delta_speed = self.lane.vehicles[self.rank + 1].speed - self.speed  # CONVENTION SENSITIVE
            
            delta_position  = obstacle - self.length_covered - self.length/2 - self.headway
            
            self.acceleration = 0
            
            if delta_speed:
                self.acceleration = self.force/self.mass * delta_speed/abs(delta_speed)
         
        #   Update the position and speed given the speed and acceleration
        self.length_covered = min(self.length_covered + self.speed * lib.delta_t, obstacle - self.length/2 - self.headway)
        self.speed          = max(min(self.speed + self.acceleration * lib.delta_t, self.road.max_speed), 5)

        #   Arrival at a roundabout
        if self.length_covered >= self.road.length - self.length/2 - self.headway:
            #   Green light
            if self.lane.light(EXIT):
                id_slot = self.lane.end.slots_roads.index(self.road)    #slot in front of the vehicle location
                
                #   The slot doesn't exist : creation of the slot
                if not self.lane.end.slots_vehicles.has_key(id_slot):
                    self.lane.end.slots_vehicles[id_slot] = None
                    
                #   The slot is free
                if self.lane.end.slots_vehicles[id_slot] is None:
                    self.lane.end.slots_vehicles[id_slot] = self
                    self.change_waiting_attitude(False)
                    self.join(self.lane.end)
                    
                #   The slot isn't free
                else:
                    self.change_waiting_attitude(True)
                    
            #   Red light
            else:
                self.change_waiting_attitude(True)

    def change_waiting_attitude(self, new_attitude):
        """
        Changes, if needed, the waiting attitude of a vehicle
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
    def position(self):
        """
        Returns the coordinates of the center of the vehicle.
        """
        if self.road is None:
            return None

        (d_position, a_position)    = self.lane.start.position, self.lane.end.position
        direction                   = (a_position - d_position)
        
        rate_covered = float(int(self.length_covered)) / float(int(self.road.length))
        
        (parallel, orthogonal) = self.lane.unit_vectors
       
        return d_position + direction * rate_covered + orthogonal * self.lane.width/2

    @property
    def rank(self):
        if (self.lane is not None) and (self in self.lane.vehicles):
            return self.lane.vehicles.index(self)
        else:
            raise Exception("ERROR (in vehicle.rank) : a vehicle is not in her place !")
    
    @property
    def lane(self):
        """
        Returns the lane where the vehicle is, if it is in a lane.
        This property is provided for convenience.
        """

        if isinstance(self.location, __road__.Lane):
            return self.location
        
        return None

    @property
    def road(self):
        """
        Returns the road where the vehicle is, if it is in a road.
        This property is provided for convenience.
        """
        
        if isinstance(self.location, __road__.Lane):
            return self.location.road

        return None

    @property
    def roundabout(self):
        """
        Returns the roundabout where the vehicle is, if it is in a roundabout.
        This property is provided for convenience.
        """

        if isinstance(self.location, __roundabout__.Roundabout):
            return self.location

        return None
   
    @property 
    def slot(self):
        """
        Returns the slot where the wehicle is, if it is in a roundabout.
        This property is provided for convenience.
        """

        if self.roundabout is None:
            return None

        return lib.find_key(self.roundabout.slots_vehicles, self)

    @property
    def track(self):
        """
        Returns the tracks where is the vehicle.
        This function is provided for convenience.
        """

        return self.location.track
