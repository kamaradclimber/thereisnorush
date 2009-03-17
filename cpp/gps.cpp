#include <algorithm>
#include <iostream>
#include <vector>

#include "constants.hpp"
#include "gps.hpp"
#include "road.hpp"
#include "roundabout.hpp"

using namespace std;


//  Constructors/destructor
GPS::GPS() : algorithm(A_STAR)
{
}

GPS::~GPS()
{
}


//  Returns approximatively the time needed to reach another node
//  A naive heuristics : straight line distance
float GPS::heuristic_weight(const Roundabout* origin, const Roundabout* destination) const
{
    float
        distance = norm(origin->get_position() - destination->get_position()),
        speed    = Road::DEFAULT.get_max_speed();

    return distance/speed;
}


//  Performs an A* pathfinding to get a path from origin to destination.
//  Returns a list of integers, representing the roads to take.
vector<Roundabout*> GPS::find_path(Roundabout* origin, Roundabout* destination) const
{ 
    //   Before we start, let's check we need to do something
    if (origin == destination || !heuristic_weight(origin, destination))
    {
        return vector<Roundabout*>();
    }
    

    //   A* algorithm
    if (algorithm == A_STAR)
    {
        //   Initialization
        vector<Roundabout*>
            open_list,
            closed_list;

        open_list.push_back(origin);
        
        origin->set_g_cost(0);
        origin->set_h_cost(heuristic_weight(origin, destination));
        
        
        //  Mainloop
        Roundabout*     current_parent(open_list.front());
        unsigned short  i(0);
        while (open_list.size() || current_parent == destination)
        {
            i = 0;
            while (i < current_parent->total_slots())
            {
                //  Connected to no road => next !
                if (!(current_parent->slot(i)->is_connected()))
                {
                    continue;
                }
                
                Roundabout* child   = current_parent->slot(i)->other_side();
                Road*       road    = current_parent->slot(i)->get_road();
                
                //  No leaving lane => next
                if (!(road->can_lead_to(child)))
                {
                    continue;
                }
                

                //   Not already in the closed list neither in the open list
                if (!binary_search(open_list.begin(), open_list.end(), child)
                &&  !binary_search(closed_list.begin(), closed_list.end(), child))
                {
                    //   Store data for this child
                    child->set_destination(destination);
                    child->set_nearest_parent(current_parent);

                    //   Add the node to the open list, keeping the order (the first node has the smallest F-cost)
                    unsigned short j(0);
                    while (j < open_list.size() && open_list[j]->get_f_cost() < child->get_f_cost())
                    {
                        j++;
                    }

                    open_list.insert(open_list.begin() + j, child);
                }


                //   Already in the open list => check if this path is a better one than the already known path
                else if (binary_search(open_list.begin(), open_list.end(), child))
                {
                    float current_g_cost = current_parent->get_g_cost() + road->weight();

                    //   This path is shorter than the existing one => store it
                    if (current_g_cost < child->get_g_cost())
                    {
                        child->set_nearest_parent(current_parent);

                        //   Do not forget to keep the open-list sorted
                        remove(open_list.begin(), open_list.end(), child);

                        unsigned short j(0);
                        while (j < open_list.size() && open_list[j]->get_f_cost() < child->get_f_cost())
                        {
                            j++;
                        }
    
                        open_list.insert(open_list.begin() + j, child);
                    }
                }
            }

            //   The parent node, around which we look, is always the first node of the "open" list
            //   Transfert the parent node to the "closed" list
            closed_list.push_back(current_parent);
            open_list.erase(open_list.begin());
            current_parent = open_list.front();
        }


        //   Save the path if it exists.
        if (binary_search(closed_list.begin(), closed_list.end(), destination))
        {
            Roundabout*         current_node = destination;
            vector<Roundabout*> path;

            while (current_node != origin)
            {
                path.insert(path.begin(), current_node);

                current_node = current_node->get_nearest_parent();
                if (current_node == NULL)
                {
                    cerr << "ERROR (in GPS::find_path()): ill-formed parent list, a node has no parent.";
                }
            }
            
            return path;
        }

        return vector<Roundabout*>();
    }


    //   TODO : Dijkstra
    else if (algorithm == DIJKSTRA)
    {
        return vector<Roundabout*>();
    }


    //   Unknown algorithm
    return vector<Roundabout*>();
}
