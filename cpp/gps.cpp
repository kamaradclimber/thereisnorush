#include <algorithm>
#include <iostream>
#include <vector>

#include "gps.hpp"
#include "lane.hpp"
#include "map.hpp"
#include "road.hpp"
#include "roundabout.hpp"

using namespace std;


//  Constructors/destructor
GPS::GPS() : algorithm(A_STAR) {}

GPS::~GPS() {}


//  Returns approximatively the time needed to reach another node
//  A naive heuristics : straight line distance
float GPS::heuristic_weight(const Roundabout* origin, const Roundabout* destination) const {
    float distance = abs(*origin - *destination);
    float speed    = Road::DEFAULT.max_speed();

    return distance/*/speed*/;
}


//  Performs an A* pathfinding to get a path from origin to destination
//  Returns a list of integers, representing the roads to follow
vector<Roundabout*> GPS::find_path(Roundabout* origin, Roundabout* destination) const { 
    //   Before we start, let's check we need to do something
    if (origin == destination || !abs(origin - destination))
        return vector<Roundabout*>();
    

    //   A* algorithm
    if (algorithm == A_STAR) {
        //   Initialization
        vector<Roundabout*> open_list;
        vector<Roundabout*> closed_list;

        open_list.push_back(origin);
        
        origin->set_g_cost(0);
        origin->set_h_cost(heuristic_weight(origin, destination));

        //  Mainloop
        Roundabout*     current_parent(0);
        unsigned short  i(0), slots_count(0);
        bool            found(false);

        while (open_list.size() && !found) {
            current_parent = open_list.back();
            open_list.pop_back();
            slots_count = current_parent->slots_count();
            i = 0;
            while (i < slots_count) {
                Roundabout* child   = current_parent->slot(i)->lane()->to();
                Road*   road    = current_parent->slot(i)->lane()->road();
                float current_g_cost = current_parent->g_cost() + road->weight();
                float current_h_cost = heuristic_weight(child, destination);
                
                //  No leaving lane => next
                if (child == current_parent) {i++; continue;}
                
                //  Path found
                if (child == destination)   {found = true; child->set_nearest_parent(current_parent); break;}
                

                //   Not yet in the closed list neither in the open list
                //   TODO: binary_search didn't work properly ; try to find why
                bool in_open_list(false);
                bool in_closed_list(false);
                unsigned short k(0);
                while (k < open_list.size()) {
                    if (open_list[k] == child)  {in_open_list = true;}
                    k++;
                }
                k = 0;
                while (k < closed_list.size()) {
                    if (closed_list[k] == child)  {in_closed_list = true;}
                    k++;
                }

                if (!in_open_list &&  !in_closed_list) {
                    //   Store data for this child
                    child->set_destination(destination);
                    child->set_nearest_parent(current_parent);
                    child->set_g_cost(current_g_cost);
                    child->set_h_cost(current_h_cost);

                    //   Add the node to the open list, keeping the order (the first node has the smallest F-cost)
                    unsigned int j(0);
                    while (j < open_list.size() && open_list[j]->f_cost() > child->f_cost())    {j++;}

                    open_list.insert(open_list.begin() + j, child);
                }


                //   Already in the open list => check if this path is a better one than the already known path
                else if (in_open_list && !in_closed_list) {
                    //   This path is shorter than the existing one => store it
                    if (current_g_cost < child->g_cost()) {
                        child->set_nearest_parent(current_parent);
                        child->set_g_cost(current_g_cost);
                        child->set_h_cost(current_h_cost);

                        //   Do not forget to keep the open-list sorted
                        remove(open_list.begin(), open_list.end(), child);

                        unsigned short j(0);
                        while (j < open_list.size() && open_list[j]->f_cost() > child->f_cost())    {j++;}
    
                        open_list.insert(open_list.begin() + j, child);
                    }
                }

                i++;
            }

            //   The parent node, around which we look, is always the first node of the "open" list
            //   Transfert the parent node to the "closed" list
            closed_list.push_back(current_parent);
        }


        //   Save the path if it exists.
        if (found) {
            Roundabout*         current_node = destination;
            vector<Roundabout*> path;

            while (current_node != origin) {
                path.insert(path.begin(), current_node);

                current_node = current_node->nearest_parent();
                if (!current_node)
                    cerr << "ERROR (in GPS::find_path()): ill-formed parent list, a node has no parent.";
            }
            
            return path;
        }

        return vector<Roundabout*>();
    }


    //   TODO : Dijkstra
    else if (algorithm == DIJKSTRA)
        return vector<Roundabout*>();


    //   Unknown algorithm
    return vector<Roundabout*>();
}
