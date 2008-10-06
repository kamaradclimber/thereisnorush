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
    
    class Car:
        """
        Those which will crowd our city >_< .
        """
        
        def generate_path(self):
            """
            Assembles random waypoints into a "path" list
            """
            
            from random import randint
            
            # We may need more than a few nodes to begin with
            #total_waypoints = randint(5, 18)    # Number of nodes to reach
            # TEMPORARY
            total_waypoints = 2000
            
            path            = []
            
            for i in range(total_waypoints):
                path += [randint(0, 128)]
            
            return path
        
        def __init__(self, newPath, new_road):
            """
            Constructor method : a car is provided a (for now unmutable) sequence of directions.
                newPath (list)  :   a list of waypoints
                new_road (Road)  :   the road where the car originates
            
            Définie par la liste de ses directions successives, pour le moment cette liste est fixe.
            """
            
            self.path       = self.generate_path()
            # For now, the cars' speed is either 0 or 100
            # Cette « vitesse » est pour le moment 0 ou 100, ce sont des « point de deplacements »
            self.speed      = 0
            self.position   = 0
            self.location   = new_road  #   Where the car is ; can be a road or a node
        
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
            
            new_location.cars   +=  [self]
            self.position       =   new_position
            self.location       =   new_location
        
        def die(self):
            """
                Kills the car, which simply disappear ; should be mostly used in dead-ends.
            """
            
            if self.location.cars:
                for i in range(len(self.location.cars)):
                    if (id(self.location.cars[i]) == id(self)):
                        del self.location.cars[i]
                        self.location = None
                        break
        
        def next_way(self, read_only = False):
            """
            Expresses the cars' wishes :P
            """
            # Becomes useless since the function "rotate" manages it -- Ch@hine
            # Maybe, though this is temporary anyway, as the cars may later want to go less "randomly" -- Sharayanan
            if len(self.path) == 0:
                return 0
            else:
                direction = self.path[0]
                if not read_only:
                    del self.path[0]
                return direction
        
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
            
            if self.location.cars:
                if rank >= len(self.location.cars) - 1: 
                    # Le seul obstacle est un feu
                    obstacle = next_light
                else:
                    # L'obstacle est la voiture devant
                    obstacle = self.location.cars[rank + 1].position
            
            self.speed = 50
            
            next_position = self.position + self.speed * delta_t
            
            if next_position < obstacle:
                # « 1 trait danger, 2 traits sécurité : je fonce ! »
                self.position = next_position
            elif (obstacle != next_light) and (next_position >= obstacle):
                # On s'arrête au prochain obstacle
                
                # TEMPORARY: see buggy code below
                self.position = next_position
                
                # BUGGY CODE: for some reason, when cars join a road where multiple cars already crowd, they sometimes get "stuck" with them
                #                           and "teleport" the first car back at the beginning of the road, as if it had to be behind the last car…
                #                           This is not important for now, as this won't hamper the way the program works.
                #self.position = obstacle - CAR_WIDTH
                #self.speed = 0 #ca ne sert un peu à rien, pour le moment,  car la vitesse est remise à 50 après
            elif (obstacle == next_light) and (next_position >= obstacle):
                # On oublie les histoires de feu rouge pour le moment : la voiture s'arrête.
                remaining_points = self.speed - (self.location.length -1 - self.position) / delta_t
                self.position = self.location.length -1 #j'avance autant que je peux, puis demande au carrefour de me prendre en charge
                #self.speed = 0
    
                # Let's do some more stuff ! We ask the node to do with us what he wants
                self.location.end.manage_car(self, remaining_points) #j'indique le nbre de points de déplacement restants (combien coûte le carrefour ?)
                # I don't really get it: what do you mean by "remaining_points" ? -- Sharayanan
