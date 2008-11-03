# -*- coding: utf-8 -*-
"""
File        :   gps.py
Description :   provides pathfinding information
"""

from constants  import *
import time

class Gps():
    """
    
    """

    def __init__(self):
        """

        """
        self.closed_list    = []
        self.open_list      = []
        
        self.path_length    = 0
        self.real_cost      = 0
        self.g_cost         = {}
        self.h_cost         = {}
        self.f_cost         = {}
        self.path           = []
        self.start_time     = 0
        
    def _build_path(self):
        """
        Given a list of nodes, returns a list of integers accounting for the road number at a roundabout.
        """
        path = []
        
        for i in range(len(self.path) - 1):
            current_node    = self.path[i]
            next_node       = self.path[i + 1]
            
            key = [i for i in range(len(current_node.leaving_roads)) if current_node.leaving_roads[i].end == next_node][0]
            path.append(key)
            
        return path
        
    def _heuristic_weight(self, start_node, end_node):
        """
        Returns an evaluation of the time needed to go from a node to another.
        """
        #   A naive heuristics : straight line distance
        distance = abs(start_node.position - end_node.position)
        speed    = ROAD_DEFAULT_MAX_SPEED
        
        return distance/speed
        
    def find_path(self, start_node, end_node, max_time = 1):
        """
        Performs an A* pathfinding to get a path from start_node to end_node.
        Returns a list of integers, representing the roads to take.
        
            start_node (Roundabout)
            end_node   (Roundabout)
            max_time   (float)     : maximum time allowed for the pathfinding algorithm (in seconds)
        """
        
        #   Before we start, let's check we need to do something
        if start_node == end_node or self._heuristic_weight(start_node, end_node) == 0:
            return None
        
        #   Add the starting point to the "open" list
        self.open_list.append(start_node)
        self.g_cost[start_node] = 0
        
        self.start_time = time.clock()
        parent          = {}
        
        while (time.clock() - self.start_time) < max_time:
            if len(self.open_list):
                #   The "parent" node, around which we look, is always the first node of the "open" list
                #   This node is transferred to the "closed" list
                current_parent = self.open_list[0]
                self.closed_list.append(current_parent)

                #   Set the first element of the open list as the one that has the smallest F-cost
                for (i, node) in enumerate(self.open_list):
                    if self.f_cost[self.open_list[0]] > self.f_cost[node]:
                        (self.open_list[i], self.open_list[0]) = (self.open_list[0], node)

                #   Check the adjacent nodes
                for road in current_parent.leaving_roads:
                    #   Not already in the closed list neither in the open list : add it to the open list
                    if not (road.end in self.closed_list) and not (road.end in self.open_list):
                        self.open_list.append(road.end)
                        
                        #   Compute its G-cost, H-cost and F-cost
                        self.g_cost[road.end] = self.g_cost[current_parent] + self._link_weight(road)
                        self.h_cost[road.end] = self._heuristic_weight(road.end, end_node)
                        self.f_cost[road.end] = self.g_cost[road.end] + self.h_cost[road.end]
                        
                        parent[road.end] = current_parent

                        #   Sort the open list (the first node must have the minimal F-cost)
                        buffer = [(self.f_cost[node], node) for node in self.open_list]
                        buffer.sort()
                        self.open_list = [node for (f_cost, node) in buffer]

                    #   Already in the open list : check to see if this path is a better one than the currently known path
                    elif road.end in self.open_list:
                        #   Compute the G-cost of this possible new path
                        current_g_cost = self.g_cost[current_parent] + self._link_weight(road)
                    		
                        #   This path is shorter (lower G-cost) : store this path as default to reach this node
                        if current_g_cost < self.g_cost[road.end]:
                            #   Set this path as the shortest path to reach this node
                            parent[road.end]        = current_parent
                            self.g_cost[road.end]   = current_g_cost
                            self.f_cost[road.end] = self.g_cost[current_parent] + self.h_cost[road.end] # Do not forget to compute the new F-cost !
                            
                            #   Sort again the open list (the first node must have the minimal F-cost)
                            buffer = [(self.f_cost[node], node) for node in self.open_list]
                            buffer.sort()
                            self.open_list = [node for (f_cost, node) in buffer]

            #   Empty open list : no path
            else:
                path = PATH_INEXISTENT
                break

            #   If target is added to open list then path has been found.
            if end_node in self.open_list:
                path = PATH_FOUND
                break

        #   Save the path if it exists.
        if path == PATH_FOUND:
            current_node        = end_node
            self.path           = []
            self.path_length    = 0

            while current_node != start_node:
                self.path.insert(0, current_node)
                current_node = parent[current_node]
                self.path_length += 1
            	
            return self._build_path()

        return None
        
