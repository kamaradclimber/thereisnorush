# -*- coding: utf-8 -*-

"""
File        :   init.py
Description :   defines the classes and constants needed for the simulation
"""

import string               # standard python library
from os   import getcwd     # standard python library, ne pas tout prendre, c'est plus propre :-)
from math import pi         # standard python library, ne pas tout prendre, c'est plus propre :-)

#   Useful constants

delta_t = 0.01  # TEMPORARY

BLACK       = (  0,   0,   0)
RED         = (255,   0,   0)
GREEN       = (  0, 255,   0)
BLUE        = (  0,   0, 255)
WHITE       = (255, 255, 255)

LIGHT_RED   = (255,  64,  64)
LIGHT_GREEN = ( 64, 255,  64)
LIGHT_BLUE  = ( 64,  64, 255)

RESOLUTION  = (WINDOW_WIDTH, WINDOW_HEIGHT) = (512, 384)

NODE_WIDTH  = 3
NODE_HEIGHT = 3
NODE_COLOR  = RED
NODE_RADIUS_DEFAULT = 10
LEAVING_GATE  = 0
INCOMING_GATE = 1

CAR_WIDTH   = 4
CAR_HEIGHT  = 4
CAR_COLOR   = WHITE

ROAD_COLOR  = WHITE

NODE        = "Node"
ROAD        = "Road"

class Track:
    """
    Our city model : a mathematical graph made of nodes, linked to each other by roads.
    """
   
    def __init__(self, new_nodes = None, new_roads = None):
        """
        Constructor method : creates a track given the nodes and roads, if any.
            new_nodes   (list)  :   a list of the nodes
            new_roads   (list)  :   a list of the roads
        """
        
        if (new_nodes is None) or (not isinstance(new_nodes, list)):
            self.nodes = []
        else:
            self.nodes = new_nodes
        
        if (new_roads is None) or (not isinstance(new_nodes, list)):
            self.roads = []
        else:
            self.roads = new_roads
    
    def add_element(self, elements):
        """
        Adds an element to the track, once it's been checked and validated.
            elements    (list)      :   a list describing the element [type, arg1, arg2…]
        """
        if (elements[0] == NODE):
            self.nodes.append(Node([elements[1], elements[2]]))
        elif (elements[0] == ROAD):
            new_road = Road(self.nodes[elements[1]], self.nodes[elements[2]], elements[3])
            self.roads += [new_road]
            new_road.connect(self.nodes[elements[1]], self.nodes[elements[2]])
        else:
            print "ERROR : unknown element type '" + elements[0] + "'."
            pass
    
    def parse_line(self, line):
        """
        Parses a line in a track description file.
            line    (string)    :   the line of text to be parsed
        """
        
        elements        = string.replace(line, ",", " ").split()
        kind            = ""
        total_arguments = 0
        
        #   Get element type
        if len(elements) != 0:
            kind = elements[0]
        
        #   Define how many arguments are expected
        if (kind == NODE):
            total_arguments = 2 #   abscissa and ordinate
        elif (kind == ROAD):
            total_arguments = 3 #   starting node, ending node and length
        else:
            print "ERROR : unknown element type '" + kind + "' !"
            pass
        
        #   Add the specified element to the track, if everything is OK
        if (len(elements) == 1 + total_arguments):
            try:
                for i in range(1, total_arguments):
                    elements[i] = int(elements[i])
                self.add_element(elements)
            except Exception, exc:
                print "ERROR : in parsing the following line : "
                print elements
                print exc 
                pass
        else:
            print "ERROR : wrong parameters given for the element '" + kind + "'."
            print elements
    
    def load_from_file(self, file_name):
        """
        Loads a track from a textfile, checks its validity, parses it
        and loads it in the simulation.
            file_name    (string)    :   the name of the file to load.
        """
        
        # TODO :
        #       · (T.LFF1) try to figure out a way to force the current directory to be the correct one (especially on Windows), since it raises an error when cwd isn't init.py's directory.
        
        try:
            # Attempts to load & read the file
            file_data   = open(file_name)
            lines       = []
            
            for line in file_data:
                lines += [line.strip()]
            
        except Exception, exc:
            # The file doesn't exists or any other error
            print "ERROR : the file " + file_name + " cannot be loaded."
            print "Current directory is : " + getcwd() 
            print exc 
            pass
            exit()
        
        for line in lines:
            self.parse_line(line)

class Road:
    """
    Connection between 2 nodes ; one-way only.
    """
    
    def __init__(self, new_begin = None, new_end = None, length = 100):
        """
        Constructor method : creates a new road.
            new_begin  (Node)    : starting point for the road
            new_end    (Node)    : ending point for the road
            new_length (int)     : road length
        """
        
        self.begin  = new_begin
        self.end    = new_end
        self.cars   = [] 
        self.length = int(length)
        self.gates  = [False, False]    # [gate at the beginning, gate at the end]
    
    def connect(self, starting_node, ending_node):
        """
        Connects the road to 2 nodes.
        """
        
        # TODO :
        #       · (N.AR1) add error handlers in order not to crash on misformed track files
        
        self.begin                  =   starting_node
        self.end                    =   ending_node
        ending_node.coming_roads    +=  [self]
        starting_node.leaving_roads +=  [self]
    
    @property
    def is_free(self):
        """
        Returns whether there is still room on the road
        """
        
        # I guess there is still room as long as the last car engaged on the road if far enough from the start of the road
        if not len(self.cars):
            return True
        elif self.cars[0].position > CAR_WIDTH * 1.5 + 1: #   Supposing we need at least a distance of 1 between 2 cars
            return True
        else:
            return False
    
    def update(self):
        if self.cars:
            queue_length = len(self.cars)
            if queue_length > 0:
                for i in range(queue_length - 1):
                    self.cars[-i-1].update(queue_length - (i+1))
                else:
                    self.cars[0].update(queue_length - 1)

    def add_car(self, new_car, new_position = 0):
        """
        Inserts a car at given position in the ordered list of cars.
            new_car      (Car)   :   car to be added
            new_position (float) :   curvilinear abscissa for the car
        """
        
        new_car.join(self, new_position)

class Node:
    """
    Crossroads of our city ; may host several roads.
    """
    
    def __init__(self, new_coordinates, radius = NODE_RADIUS_DEFAULT):
        """
        Constructor method : creates a new node.
            new_coordinates (list) : the coordinates [x, y] for the node
        """
        
        self.x, self.y     = new_coordinates[0], new_coordinates[1]
        self.coming_roads  = []
        self.leaving_roads = []
        self.cars          = []
        
        # Maximum available space to host cars : perimeter divided by cars' width
        # Nombre maximum de cases disponibles pour héberger les voitures : périmètre divisé par la longueur des voitures
        self.max_cars      = int(2 * pi * radius / CAR_WIDTH)
    
    def manage_car(self, car, remaining_points):
        """
        Asks the node to take control over the car and move it appropriately.
        Demande au nœud de prendre le contrôle de la voiture et de la déplacer de manière adéquate.
        """
        
        if len(self.leaving_roads):
            # The node may, or may not, accept to host the car
            if len(self.cars) < self.max_cars :
                # On s'est gardé de la div par 0 avec le test booléen 
                # Thanks to the above boolean test, we'll avoid division by zero
                car.join(self)
        else: 
            # On est arrivé à dans une impasse, faut-il faire disparaitre la voiture pour accélerer le programme ?
            # In my opinion, we should, hence the following line :
            car.die()
            pass
    
    def update_car(self, car):
        """
        Updates a given car on the node
        """
        # TODO :
        #       · (N.UC1) check for position on the node to account for rotation (cf. N.U2)
        #       · (N.UC2) check for the leaving_road to be free before branching on it (use read_only = True in newt_way() unless you branch) ; DONE !
        
        # TEMPORARY : go to where you want
        next_way = car.next_way() % len(self.leaving_roads)
        if (self.leaving_roads[next_way].is_free):
            car.join(self.leaving_roads[next_way]) # No need for remaining_points since we start from *zero*
    
    def update(self):
        """
        Updates the node: rotate the cars, dispatch them...
        """
        # TODO :
        #       · (N.U1) Lock the gates when the node is full and (temporarily) open them otherwise (or at least, let us some control over them)
        #       · (N.U2) Implement cars' rotation on the node before calling update_car
        
        if self.cars:
            for car in self.cars:
                self.update_car(car)
    
    @property
    def coords(self):
        return (self.x, self.y)
    
    def set_gate(self, road, state):
        """
        Sets the state of the gates on the road.
            road    (Road)  :   the road whose gates are affected
            state   (int)   :   the state (0 = red, 1 = green) of the gate
        """
        
        # TODO :
        #       · (N.SG1) use more explicit constant names (e.g. "GATE_LEAVING" instead of "0") ; DONE !
        #       · (N.SG2) lock gate usage when the node is full, see (N.U1)
        
        if (id(road.begin) == id(self)):
            # The road begins on the node: there is a gate to pass before leaving
            road.gates[LEAVING_GATE] = state
        else:
            # The road ends on the road: there is a gate to pass to enter
            road.gates[INCOMING_GATE] = state
            
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
        
        if self.location is not None:
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
                if self.location.cars[i] == self:
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
        
        if self.position + self.speed * delta_t < obstacle:
            # « 1 trait danger, 2 traits sécurité : je fonce ! »
            self.position += self.speed * delta_t
        elif obstacle != next_light:
            # On s'arrête au prochain obstacle
            self.position = obstacle - CAR_WIDTH
            self.speed = 0 #ca ne sert un peu à rien, pour le moment,  car la vitesse est remise à 50 après
        else:
            # On oublie les histoires de feu rouge pour le moment : la voiture s'arrête.
            remaining_points = self.speed - (self.location.length -1 - self.position) / delta_t
            self.position = self.location.length -1 #j'avance autant que je peux, puis demande au carrefour de me prendre en charge
            #self.speed = 0

            # Let's do some more stuff ! We ask the node to do with us what he wants
            self.location.end.manage_car(self, remaining_points) #j'indique le nbre de points de déplacement restants (combien coûte le carrefour ?)
            # I don't really get it: what do you mean by "remaining_points" ? -- Sharayanan

#   TESTING ZONE

if (__name__ == '__main__'):
    print "You should run interface.py instead of this file !"
    pass

# Temporary testing zone
track = Track()
track.load_from_file("track_default.txt")
#attention à l'ordre dans lequel on place les voitures ! si ce n'est pas dans lordre décroissant par position, tout le reste du programme est gêné !
# un tri, tout au début devrait résoudre ce bug issue2
track.roads[3].add_car(Car([], track.roads[3]), 5)
track.roads[6].add_car(Car([], track.roads[6]), 500)
track.roads[6].add_car(Car([], track.roads[6]), 30)
track.roads[6].add_car(Car([], track.roads[6]), 10)
track.roads[6].add_car(Car([], track.roads[6]), 10)