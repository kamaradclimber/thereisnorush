# -*- coding: utf-8 -*-

"""
File        :   car.py
Description :   defines the class "Car"
"""

delta_t = 0.01  # TEMPORARY

try:
    CAR_FILE
except NameError:
    CAR_FILE = True
    
    from road import Road
    from node import Node
    
    CAR_DEFAULT_LENGTH   = 5
    CAR_DEFAULT_WIDTH    = 4
    CAR_DEFAULT_HEADWAY  = CAR_DEFAULT_LENGTH #marge de sécurité
    CAR_DEFAULT_SPEED    = 0
    CAR_DEFAULT_MAX_SPEED= 50
    CAR_DEFAULT_ACCEL    = 10
    CAR_DEFAULT_COLOR    = ( 64,  64, 255)
    
    class Car:
        """
        Those which will crowd our city >_< .
        """
        
        def __init__(self,
                     newPath,
                     new_road,
                     new_speed = CAR_DEFAULT_SPEED,
                     new_accel = CAR_DEFAULT_ACCEL,
                     new_max_speed = CAR_DEFAULT_MAX_SPEED,
                     new_length = CAR_DEFAULT_LENGTH,
                     new_width = CAR_DEFAULT_WIDTH,
                     new_headway = CAR_DEFAULT_HEADWAY,
                     new_color = CAR_DEFAULT_COLOR):
            """
            Constructor method : a car is provided a (for now unmutable) sequence of directions.
                newPath (list)  :   a list of waypoints
                new_road (Road) :   the road where the car originates (for now, let's forbid the original location to be a node)
            
            Définie par la liste de ses directions successives, pour le moment cette liste est fixe.
            """
            
            # Car & driver properties, to use in dynamics & behavior management
            self.path       = []
            self.waiting    = False         # Indicates whether the car is waiting at the gates
            self.length    = new_length     # Car's length (from front to rear) / Longueur de la voiture (de l'avant à l'arrière)
            self.width     = new_width      # Car's width (from left to right) / Envergure de la voiture (de gauche à droite)   
            self.speed     = new_speed 
            self.position  = 0               
            self.headway   = new_headway    # Desired headway to the preceding car / Distance souhaitée par rapport à la voiture devant
            self.color     = new_color 
            self.max_speed = new_max_speed
            #self.max_accel =  # Car's maximum acceleration / Accélération maximale
            self.acceleration = new_accel      
            
            if isinstance(new_road, Road):
                self.location = new_road
            else:
                self.location = None
            
            self.generate_path()
        
        def generate_path(self):
            """
            Assembles random waypoints into a "path" list
            """
            
            from random import randint
            
            # We may need more than a few nodes to begin with
            #total_waypoints = randint(5, 18)    # Number of nodes to reach
            # TEMPORARY
            total_waypoints = 2000
            
            self.path       = []
            
            for i in range(total_waypoints):
                self.path += [randint(0, 128)]
        
        def join(self, new_location, new_position = 0):
            """
            Allocate the car to the given location. The concept of location makes it possible to use this code for either a road or a node.
                new_location    (Road or Node)  :   road or node that will host, if possible, the car
                new_position    (list)          :   position in the road or in the node (note that the meaning of the position depends on the kind of location)
            """
            
            if self.location:
                for i in range(len(self.location.cars)):
                    if (id(self.location.cars[i]) == id(self)):
                        # Important : do not write self.cars[i] = None, cause it erases the car itself and crashes
                        del self.location.cars[i]
                        break
            
            self.position       =   new_position
            old_location        =   self.location
            self.location       =   new_location
            
            # CONVENTION SENSITIVE
            new_location.cars   =  [self] + new_location.cars
            
            #   Each time a car joins or leaves a node, this one has to update the calculate again the best configuration for the gates
            if isinstance(old_location, Node):
                old_location.update_gates()
            elif isinstance(new_location, Node):
                new_location.update_gates()
        
        def die(self):
            """
            Kills the car, which simply disappear ; may be mostly used in dead-ends.
            """
            
            if self.location.cars:
                for i in range(len(self.location.cars)):
                    if (id(self.location.cars[i]) == id(self)):
                        del self.location.cars[i]
                        
                        #toutes les modifs suivantes sont justes pour le confort de l'esprit et ne changent pas grand chose
                        #cela dit, un jour mais cest pas pour tout de suite, il faudra verifier que les voitures non utilisées sont bien libérées de la memoire (ocaml le ferait, qu'en est-il de python ?)
                        self.location   = None
                        self.path       = []
                        self.speed      = 0
                        self.position   = 0
                        
                        break
        
        def next_way(self, read_only = False):
            """
            Expresses the cars' wishes :P
            """

            if len(self.path) == 0:
                return 0
            else:
                
                if not read_only:
                    del self.path[0]
                return self.path[0]
        
        def update(self, rank):
            """
            Updates the car speed and position, manages blocked pathways and queues.
                rank    (int)   :   position on the road (0 : last in)
            """
            
            # TODO :
            #       · (C.U1) resort to more "realistic" physics (e.g. acceleration, braking...)
            
            if not isinstance(self.location, Road):
                return None
            
            next_light = self.location.length - 1
            
            if rank >= len(self.location.cars) - 1: 
                # Le seul obstacle est un feu
                obstacle = next_light
            else:
                # L'obstacle est la voiture devant
                # CONVENTION SENSITIVE
                obstacle = self.location.cars[rank + 1].position - self.location.cars[rank + 1].length/2
            
            next_position = self.position + self.speed * delta_t
            
            if next_position + self.length / 2 + self.headway < obstacle:
                # « 1 trait danger, 2 traits sécurité : je fonce ! »
                self.position = next_position
                
                # EXPERIMENTAL: accounting for the physics of acceleration
                self.speed += self.acceleration * delta_t
                if self.speed > self.max_speed:
                    self.speed = self.max_speed
            elif obstacle < next_light:
                # On s'arrête au prochain obstacle
                
                if not self.waiting:
                    self.position = obstacle - self.length/2 - self.headway
                #CONVENTION SENSITIVE
                self.waiting = self.location.cars[rank + 1].waiting
                
                # EXPERIMENTAL : stop the car that is waiting 
                if self.waiting:
                    self.speed = 0
            elif obstacle >= next_light:

                if self.location.gates[1]:
                    # Everything's ok, let's go !
                    self.waiting = False
                    self.position = next_position
                    self.join(self.location.end)
                else:
                    # We have a closed gate in front of us : stop & align
                    self.position = self.location.length - self.headway - self.length / 2
                    self.waiting = True