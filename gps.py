# -*- coding: utf-8 -*-
"""
File        :   gps.py
Description :   provides pathfinding information
"""

import constants
import time

class Gps():

    def __init__(self):
        self.closed_list = []
        self.open_list   = []

        self.path_length      = 0
        self.real_cost        = 0
        self.g_cost           = {}
        self.h_cost           = {}
        self.f_cost           = {}
        self.path             = []
        self.start_time       = 0

    def _link_weight(self, road):
        """
        Returns the weight associated to an arc between two nodes
        """
        
        # Here, the weight is the time needed to walk the road
        return road.length / road.max_speed
        
    def _reconstruct_path(self, new_path):
        """
        Given a list of nodes, returns a list of integers accounting for the
        road number at a roundabout
        """
        path = []
        
        for i in range(len(new_path) - 1):
            cur_node  = new_path[i]
            next_node = new_path[i + 1]
            
            key = [i for i in range(len(cur_node.leaving_roads)) if cur_node.leaving_roads[i].end == next_node][0]
            path.append(key)
            
        return path
        
    def _heuristic_weight(self, start_node, end_node):
        """
        Returns an evaluation of the time needed to go from
        a node to another.
        """
        
        # A naive heuristics: straight line distance
        distance = abs(start_node.position - end_node.position)
        speed    = constants.ROAD_DEFAULT_MAX_SPEED
        
        return distance/speed
        
    def find_path(self, start_node, end_node, max_time = 1):
        """
        Performs an A* pathfinding to get a path from start_node to end_node
        Returns a list of integers, representing the roads to take.
        
            start_node (Roundabout)
            end_node   (Roundabout)
            max_time   (float)     : maximum time allowed for the pathfinding algorithm (in seconds)
        """
        
        # Before we start, let's check we need to do something
        if start_node == end_node or self._heuristic_weight(start_node, end_node) == 0:
            return None 
        
        # Add the starting point to the "open" list 
        self.open_list.append(start_node)
        self.g_cost[start_node] = 0
        
        self.start_time = time.clock()
        parent     = {}
        
        while (time.clock() - self.start_time) < max_time:
            if len(self.open_list) > 0:
                # The "parent" node, around which we look, is the first node of the "open" list
                cur_parent = self.open_list[0]
                # This node is transferred to the "closed" list, and the last element of 
                # the open list is placed on top (he has the lowest f cost, see [1] below)
                self.open_list[0] = self.open_list[-1]
                del self.open_list[-1]
                self.closed_list.append(cur_parent)
                
                # [1] We reorder to ensure the first element has the smallest f cost
                # I did this quite randomly, if you find better, feel free to modify
                for i in range(len(self.open_list)):
                    if self.f_cost[self.open_list[0]] < self.open_list[i]:
                        self.open_list[i], self.open_list[0] = self.open_list[0], self.open_list[i] 
                        

                # Check the adjacent nodes
                for road in cur_parent.leaving_roads:
                    # If not already on the closed list		
                    if not (road.end in self.closed_list):
                        # If not already on the open list, add it to the open list.			
                        if not (road.end in self.open_list):
                            self.open_list.append(road.end)
                            # Figure out its G cost
                            self.g_cost[road.end] = self.g_cost[cur_parent] + self._link_weight(road)

                            # Figure out its H and F costs, and parent
                            self.h_cost[road.end] = self._heuristic_weight(road.end, end_node)
                            self.f_cost[road.end] = self.g_cost[road.end] + self.h_cost[road.end]
                            parent[road.end] = cur_parent

                            # Move the new open list item to the proper place in the binary heap.
                            # Starting at the bottom, successively compare to parent items,
                            # swapping as needed until the item finds its place in the heap
                            # or bubbles all the way to the top (if it has the lowest F cost).
		
                            position = len(self.open_list) - 1
                            while (position != 0):
                                # While item hasn't bubbled to the top (position = 0)	
                                # Check if child's F cost is < parent's F cost. If so, swap them.	
                                if (self.f_cost[self.open_list[position]] <= self.f_cost[self.open_list[position/2]]):
                                    self.open_list[position/2], self.open_list[position] = self.open_list[position], self.open_list[position/2]
                                else:
                                    break

                    # If adjacent cell is already on the open list, check to see if this 
                    # path to that cell from the starting location is a better one. 
                    # If so, change the parent of the cell and its G and F costs.	
                    else:
                        # Figure out the G cost of this possible new path
                        temp_g_cost = self.g_cost[cur_parent] + self._link_weight(road)
                    		
                        # If this path is shorter (G cost is lower) then change
                        # the parent cell, G cost and F cost. 		
                        if (temp_g_cost < self.g_cost[road.end]):
                            # if G cost is less,
                            parent[road.end] = cur_parent
                            self.g_cost[road.end] = temp_g_cost # change the G cost			
                        
                			# Because changing the G cost also changes the F cost, if
                			# the item is on the open list we need to change the item's
                			# recorded F cost and its position on the open list to make
                			# sure that we maintain a properly ordered open list.
                            
                            key = [item for item in self.open_list if item == node][0] # Get the key for the current item
                            self.f_cost[self.open_list[key]] = self.g_cost[cur_parent] + self.h_cost[self.open_list[key]] # change the F cost
                            
                            #See if changing the F score bubbles the item up from it's current location in the heap
                            position = key;
                            while (position != 0): # While item hasn't bubbled to the top (position = 0)	
                                # Check if child is < parent. If so, swap them.	
                                if (self.f_cost[self.open_list[position]] < self.f_cost[self.open_list[m/2]]):
                                    self.open_list[position/2], self.open_list[position] = self.open_list[position], self.open_list[position/2]
                                else:
                                    break
	
            # If open list is empty then there is no path.	
            else:
                path = constants.PATH_INEXISTENT
                break

            # If target is added to open list then path has been found.
            if end_node in self.open_list:
                path = constants.PATH_FOUND
                break

        # Save the path if it exists.
        if (path == constants.PATH_FOUND):
            # Working backwards from the target to the starting location by checking
            # each cell's parent, figure out the length of the path.
            cur_position = end_node
            while cur_position != start_node:
            	
                # Look up the parent of the current cell.	
                cur_position = parent[cur_position]
                # Figure out the path length
                self.path_length += 1
            	
            # Copy the path information over to the databank. Since we are
            # working backwards from the target to the start location, we copy
            # the information to the data bank in reverse order.
            cur_position = end_node
    	
            while cur_position != start_node:
                # Add the current node at the beginning
                self.path.insert(0, cur_position)

                # Look up the parent of the current cell.	
                cur_position = parent[cur_position]

        # Finally, we ought to reconstruct the path in a readable manner,
        # ie transform this list of nodes into a list of numbers
        return self._reconstruct_path(self.path)
        