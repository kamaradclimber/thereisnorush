#include "lane.hpp"

using namespace std;

//  Default features
Lane::DEFAULT.set_width(5);


//  Constructor/destructor
Lane::Lane() : width(Lane::DEFAULT.get_width())
{
}

Lane::Lane(Road* new_road, bool new_direction) : road(new_road), vehicles(), width(Lane::DEFAULT.get_width()), direction(new_direction)
{
}


/*  Return the time (in milliseconds) since the last update of a gate (0 or 1).
void Lane::last_light_update(gate)



    if gate == ENTRANCE:
    return road.last_lights_update[start][gate]

    
    return road.last_lights_update[end][gate]*/

/*  Return the state of the given light.
void Lane::light(gate)



    if gate == ENTRANCE:
    return road.lights[start][gate]

    return road.lights[end][gate]*/

/*Sets the state of the traffic lights on the road.
void Lane::set_light(gate, state)



    //   Update if necessary
    if gate ==  ENTRANCE:
    if road.lights[start][gate] != state:
road.last_lights_update[start][gate]   = lib.clock()
    road.lights[start][gate]               = state
    else:
    if road.lights[end][gate] != state:
road.last_lights_update[end][gate]   = lib.clock()
    road.lights[end][gate]               = state*/


//  Returns the number of waiting vehicles on the lane.
unsigned short Lane::total_waiting_vehicles() const
{
    unsigned short result(0), i(0);
    
    while (i < vehicles.size())
    {
        if (vehicles[i]->waiting())
        {
            result++;
        }

        i++;
    }
    
    return result;
}


//  Returns whether there is still room on the road
bool Lane::is_free() const
{
    //   I guess there is still room as long as the last vehicle engaged on the road if far enough from the start of the road
    if (!(vehicles.size()))
    {
        return true;
    }
    
    return (vehicles.back()->length_covered() > Vehicles::DEFAULT->length() + Vehicles::DEFAULT->headway());
}


//  Get the origin/destination of the lane (provided for convenience)
Roundabout* Lane::origin() const
{
    return road->extremity[1 - direction];
}

Roundabout* Lane::destination() const
{
    return road->extremity[direction];
}


//  Returns the length of the lane, which is exactly the same as the length of its road (provided for convenience)
float Lane::length() const
{
    return road->length();
}


//  Returns the unit parallel and perpendicular vectors to the lane, oriented towards the end of the lane
vector<Vector> Lane::reference() const
{
    if (direction)
    {
        return road->reference();
    }

    return road->reference() * (-1);
}


//  Returns the track to which the lane belongs (provided for convenience)
Map* Lane::map() const
{
    return road->map();
}


//  Updates the lane, and all the vehicles on it.
void Lane::update()
{
    unsigned short i(0);
    while (i < vehicles.size())
    {
        vehicles[vehicles.size() - 1 - i]->act();
        i++;
    }
}
