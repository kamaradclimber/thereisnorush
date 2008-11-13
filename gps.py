# -*- coding: utf-8 -*-
"""
File        :   gps.py
Description :   provides pathfinding information
"""

from constants  import *
import lib

class Gps():
    """
    Tool used to find the shortest path between 2 roundabouts.
    """

    def __init__(self):
        self.algorithm  = A_STAR
        self.path       = []
        
    def _build_path(self):
        """
        Given a list of nodes, returns a list of roads.
        """
        path = []
        
        for (i, current_node) in enumerate(self.path):
            if i < len(self.path) - 1:
                next_node   = self.path[i + 1]
                next_road   = current_node.get_road_to(next_node)
                
                if next_road is None:
                    raise Exception('ERROR (in gps._build_path()) : there is no route.')
                    
                path.append(next_road)
            
        return path
        
    def _heuristic_weight(self, origin, destination):
        """
        Returns an evaluation of the time needed to go from a node to another.
        """

        #   A naive heuristics : straight line distance
        distance = abs(origin.position - destination.position)
        speed    = ROAD_DEFAULT_MAX_SPEED
        
        return distance/speed
        
    def find_path(self, origin, destination, max_time = 1):
        """
        Performs an A* pathfinding to get a path from origin to destination.
        Returns a list of integers, representing the roads to take.
        
            origin (Roundabout)
            destination   (Roundabout)
            max_time   (float)     : maximum time allowed for the pathfinding algorithm (in seconds)
        """
        
        #   Before we start, let's check we need to do something
        if origin == destination or self._heuristic_weight(origin, destination) == 0:
            return None
        
        open_list   = []
        closed_list = []
        
        #   A*
        if self.algorithm == A_STAR:
            #   Initialisation
            start_time      = lib.clock()
            g_cost          = {}    # Minimal real cost found so far
            h_cost          = {}    # Remaining heuristic cost
            f_cost          = {}    # G-cost + H-cost
            nearest_parent  = {}
            
            #   Add the starting point to the "open" list
            open_list.append(origin)
            g_cost[origin]  = 0
            h_cost[origin]  = f_cost[origin] = self._heuristic_weight(origin, destination)
            
            while len(open_list):
                #   The parent node, around which we look, is always the first node of the "open" list
                #   Transfert the parent node to the "closed" list
                current_parent = open_list[0]
                closed_list.append(current_parent)
                del open_list[0]
    
                #   The parent node is the destination => the path is found.
                if current_parent == destination:
                    break
    
                #   Set the first element of the open list as the one that has the smallest F-cost
                for (i, node) in enumerate(open_list):
                    if f_cost[open_list[0]] > f_cost[node]:
                        (open_list[i], open_list[0]) = (open_list[0], node)
                
                for child in current_parent.children:
                    #   Not already in the closed list neither in the open list
                    if not (child in (closed_list + open_list)):
                        current_road = current_parent.get_road_to(child)

                        #   Store data for this child
                        g_cost[child]           = g_cost[current_parent] + current_road.weight
                        h_cost[child]           = self._heuristic_weight(child, destination)
                        f_cost[child]           = g_cost[child] + h_cost[child]
                        nearest_parent[child]   = current_parent
                        
                        #   Add the node to the open list, keeping the order (the first node has the smallest F-cost)
                        if len(open_list) and (f_cost[open_list[0]] > f_cost[child]):
                            open_list.insert(0, child)
                        else:
                            open_list.append(child)
    
                    #   Already in the open list => check if this path is a better one than the already known path
                    elif child in open_list:
                        current_g_cost = g_cost[current_parent] + current_road.weight
                        
                        #   This path is shorter than the existing one => store it
                        if current_g_cost < g_cost[child]:
                            nearest_parent[child]   = current_parent
                            g_cost[child]           = current_g_cost
                            f_cost[child]           = g_cost[current_parent] + h_cost[child]    # Do not forget to update the F-cost !
                            
                            #   Do not forget to keep the open-list sorted
                            if f_cost[open_list[0]] > f_cost[child]:
                                i = open_list.index(child)
                                (open_list[0], open_list[i]) = (open_list[i], open_list[0])
    
            #   Save the path if it exists.
            if destination in closed_list:
                current_node    = destination
                self.path       = []
                path_length     = 0
                
                while current_node != origin:
                    self.path.insert(0, current_node)
                    if current_node in nearest_parent:
                        current_node = nearest_parent[current_node]
                    else:
                        raise Exception('ERROR (in gps.find_path()): ill-formed parent list, a node has no parent.')
                        
                    path_length += 1

                return self._build_path()
    
            return None

        #   Dijkstra
        elif self.algorithm == DIJKSTRA:
            return None
        
        #   Unknown algorithm
        else:
            return None
