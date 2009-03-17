#include "lane.hpp"

using namespace std;

//  Creates a Lane on the parent new_road.
Lane::Lane(Road* new_road, bool new_direction) : road(new_road), vehicles(), width(DEFAULT[LANE][WIDTH]), direction(new_direction)
{
}

//  Updates the lane, and all the vehicles on it.
void Lane::update()
{
    unsigned short i = 0;
    while (i < vehicles.size())
    {
        vehicles[vehicles.size() - 1 - i]->act();
        i++;
    }
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
    unsigned short
        result  = 0,
        i       = 0;
    
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

//  Returns whether there is still room on the road.
bool Lane::free() const
{
    //   I guess there is still room as long as the last vehicle engaged on the road if far enough from the start of the road
    if (!(vehicles.size()))
    {
        return true;
    }
    
    return (vehicles.back()->length_covered() > vehicles->back()->length() + vehicles.back()->headway());
}

//  Returns the end roundabout of the lane.
//  This property is provided for convenience.
Roundabout* Lane::destination() const
{
    return road->extremity[1 - direction];
}


//  Returns the length of the lane, which is exactly the same as the length of its road.
//  This property is provided for convenience.
float Lane::length() const
{
    return road->length();
}

//  Returns the unit parallel and perpendicular vectors to the lane, oriented towards the end of the lane.
vector<Vector> Lane::reference() const
{
    if (!direction)
    {
        return road->reference();
    }

    return road->reference() * (-1);
}

//  Returns the track to which the lane belongs.
//  This property is provided for convenience.
Map* Lane::map() const
{
    return road->map();
}
