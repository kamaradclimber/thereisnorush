# -*- coding: utf-8 -*-

"""
File        :   node.py
Description :   defines the class "Node"
"""

try:
    NODE_FILE
except NameError:
    NODE_FILE = True
    
    import init
    from math import pi
    
    LEAVING_GATE             = 1
    INCOMING_GATE            = 0

    class Node:
        """
        Crossroads of our city ; may host several roads.
        """
        
        def __init__(self, new_coordinates, radius = init.NODE_RADIUS_DEFAULT):
            """
            Constructor method : creates a new node.
                new_coordinates (list) : the coordinates [x, y] for the node
            """
            
            self.x, self.y     = new_coordinates[0], new_coordinates[1]
            self.incoming_roads  = []
            self.leaving_roads = []
            self.cars          = []
            
            # Maximum available space to host cars : perimeter divided by cars' width
            # Nombre maximum de cases disponibles pour héberger les voitures : périmètre divisé par la longueur des voitures
            
            # TEMPORARY
            #self.max_cars      = int(2 * pi * radius / car.CAR_DEFAULT_LENGTH)
            self.max_cars = 10

        def num_waiting_cars(self, road):
            waiting_cars = 0
            if road.cars:
                for car in road.cars:
                    if car.waiting:
                        waiting_cars += 1
            return waiting_cars

        @property
        def is_full(self):
            """
            Returns whether there is no place left on the node
            """
           
            return (len(self.cars) >= self.max_cars)
        
        def update_gates(self):
            """
            Manages the gates of the roads. This function will be the key part of the code, that's why it is called everytime
            For now, only closes gates if the node is full.
            """

            # Number of cars that are waiting on all the incoming roads
            num_waiting = 0
            for road in self.incoming_roads:
                num_waiting += self.num_waiting_cars(road)

            # CAUTION: this *has* to be in a separate loop !
            for road in self.incoming_roads:
                # TESTING ONLY: there has to be at least 2 waiting cars for the node to open, otherwise it closes the gates!
                if self.num_waiting_cars(road) > 2:
                    self.set_gate(road, True)
                else:
                    self.set_gate(road, False)
                    pass


            # ne rien ajouter apres cette section, !
            if self.is_full:
                for i in range(len(self.leaving_roads)):
                    self.set_gate(self.leaving_roads[i], False)
                        
        #   I THINK THIS FUNCTION SHOULD BE DELETED ; PLEASE CONFIRM -- Ch@hine
        # There's no need to capitalize… you should give a proposition first, I guess. If you think it's better to remove this method, proceed. -- Sharayanan
        def manage_car(self, car, remaining_points):
            """
            Asks the node to take control over the car and move it appropriately.
            Demande au nœud de prendre le contrôle de la voiture et de la déplacer de manière adéquate.
            """
            
            if len(self.leaving_roads):
                # The node may, or may not, accept to host the car
                if len(self.cars) < self.max_cars:
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
            next_way = car.next_way(True) % len(self.leaving_roads) # Just read the next_way unless you really go there
            if (self.leaving_roads[next_way].is_free):
                car.join(self.leaving_roads[car.next_way(False) % len(self.leaving_roads)]) # No need for remaining_points since we start from *zero*
        
        def update(self):
            """
            Updates the node: rotate the cars, dispatch them...
            """
            # TODO :
            #       · (N.U1) Lock the gates when the node is full and (temporarily) open them otherwise (or at least, let us some control over them)
            #       · (N.U2) Implement cars' rotation on the node before calling update_car
            
            self.update_gates() # first, update gates, unless it should be unnecessary
            
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
                state   (bool)   :   the state (False = red, True = green) of the gate
            """

            if (id(road.begin) == id(self)):
                # The road begins on the node: there is a gate to pass before leaving
                road.gates[INCOMING_GATE] = state
            else:
                # The road ends on the road: there is a gate to pass to enter
                road.gates[LEAVING_GATE] = state