﻿# -*- coding: utf-8 -*-
"""
File        :   gps.py
Description :   provides pathfinding information
"""

from constants  import *
import lib

class Gps():
    """
    
    """

    def __init__(self, new_algorithm = A_STAR):
        """

        """

        self.algorithm      = new_algorithm
        
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
            
            key_list = [i for i in range(len(current_node.leaving_roads)) if current_node.leaving_roads[i].end == next_node]
            
            if len(key_list) == 0:
                raise Exception('ERROR (in gps._build_path()) : there is no route.')
                
            path.append(key_list[0])
            
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
        
        #   Add the starting point to the "open" list
        self.open_list.append(origin)
        self.g_cost[origin] = 0
        self.h_cost[origin] = self.f_cost[origin] = self._heuristic_weight(origin, destination)
        
        self.start_time = lib.clock()
        nearest_parent  = {}
        self.path       = PATH_INEXISTENT
        
        #while (lib.clock() - self.start_time) < max_time:
        while len(self.open_list):
            #   The "parent" node, around which we look, is always the first node of the "open" list
            #   This node is transferred to the "closed" list
            current_parent = self.open_list[0]
            self.closed_list.append(current_parent)
            del self.open_list[0]

            #   The "parent" node is the destination : the path has been found.
            if current_parent == destination:
                self.path = PATH_FOUND
                break

            #   Set the first element of the open list as the one that has the smallest F-cost
            for (i, node) in enumerate(self.open_list):
                if self.f_cost[self.open_list[0]] > self.f_cost[node]:
                    (self.open_list[i], self.open_list[0]) = (self.open_list[0], node)
            
            #   Check the adjacent nodes
            children = [road.end for road in current_parent.leaving_roads]
            
            for child in children:
                #   Not already in the closed list neither in the open list
                if not (child in self.closed_list) and not (child in self.open_list):
                    #   Compute its G-cost, H-cost and F-cost
                    self.g_cost[child] = self.g_cost[current_parent] + road.weight
                    self.h_cost[child] = self._heuristic_weight(child, destination)
                    self.f_cost[child] = self.g_cost[child] + self.h_cost[child]
                    
                    nearest_parent[child] = current_parent
                    
                    #   Add the node to the open list, keeping the order (the first node has the smallest F-cost)
                    if len(self.open_list) and (self.f_cost[self.open_list[0]] > self.f_cost[child]):
                        self.open_list.insert(0, child)
                    else:
                        self.open_list.append(child)

                #   Already in the open list : check to see if this path is a better one than the currently known path
                elif child in self.open_list:
                    #   Compute the G-cost of this possible new path
                    current_g_cost = self.g_cost[current_parent] + road.weight
                        
                    #   This path is shorter (lower G-cost) : store this path as default to reach this node
                    if current_g_cost < self.g_cost[child]:
                        #   Set this path as the shortest path to reach this node
                        nearest_parent[child]    = current_parent
                        self.g_cost[child]       = current_g_cost
                        self.f_cost[child]       = self.g_cost[current_parent] + self.h_cost[child]   # Do not forget to update the F-cost !
                        
                        #   Check if the open list is still in the right order
                        if self.f_cost[self.open_list[0]] > self.f_cost[child]:
                            i = self.open_list.index(child)
                            (self.open_list[0], self.open_list[i]) = (self.open_list[i], self.open_list[0])

        #   Save the path if it exists.
        if self.path == PATH_FOUND:
            
            current_node        = destination
            self.path           = []
            self.path_length = 0
            
            while current_node != origin:
                self.path.insert(0, current_node)
                if current_node in nearest_parent:
                    current_node = nearest_parent[current_node]
                else:
                    raise Exception('ERROR (in gps.find_path()): ill-formed parent list, a node has no parent.')
                    
                self.path_length += 1
            return self._build_path()

        return None