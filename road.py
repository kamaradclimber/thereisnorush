# -*- coding: utf-8 -*-

"""
File        :   road.py
Description :   defines the class "Road"
"""

try:
    ROAD_FILE
except NameError:
    ROAD_FILE = True
    
    import init
    
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
            elif self.cars[0].position > init.CAR_WIDTH * 1.5 + 1: #   Supposing we need at least a distance of 1 between 2 cars
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