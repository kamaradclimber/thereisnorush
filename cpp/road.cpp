#include <cmath>

#include "constants.hpp"
#include "lib.hpp"
#include "road.hpp"

using namespace std;

//  Constructors & destructor
Road::Road()
{
}

Road::Road(const Roundabout* roundabout1, const Roundabout* roundabout2) : max_speed(DEFAULT[ROAD][MAX_SPEED]), extremities(2), lanes(2), semaphores(2, vector<Semaphore>(2, Semaphore()))
{ 
    //  Default features
    DEFAULT.set_color(QColor(Qt::yellow));
    DEFAULT.set_max_speed(50);
    
    extremities[0] = roundabout1;
        extremities[0]->host(this);
    extremities[1] = roundabout2;
        extremities[1]->host(this);
    lanes[0].resize(1);
        lanes[0][0] = new Lane(this, 0);
    lanes[1].resize(1);
        lanes[1][0] = new Lane(this, 1);

    semaphores[0][0].open();
    semaphores[0][1].open();
    semaphores[1][0].open();
    semaphores[1][1].open();
}

Road::~Road()
{
}

//  Mutators
void Road::set_max_speed(unsigned short new_value)
{
    max_speed = new_value;
}

void Road::set_color(QColor new_color)
{
    color = new_color;
}

//  Given a roundabout, returns the other roundabout extremity of the road.
//  Returns NULL if the given roundabout is not an extremity of the road.
Roundabout* Road::other_extremity(const Roundabout* roundabout) const
{
    if (roundabout == extremities[0])
    {
        return extremities[1];
    }
    else if (roundabout == extremities[1])
    {
        return extremities[0];
    }

    return NULL;
}

//  Returns True if the road has a lane that goes to the given roundabout, and False otherwise.
bool Road::can_lead_to(const Roundabout* roundabout) const
{
    //   The road is not even connected to the roundabout => the answer is False
    if (roundabout == extremities[0])
    {
        return lanes[1].size() > 0;
    }
    else if (roundabout == extremities[1])
    {
        return lanes[0].size() > 0;
    }
}

//  Updates the road (will update the lanes on the road).
void Road::update()
{
    vector<Lane*> all_lanes(lanes[0]);
        all_lanes.insert(all_lanes.end(), lanes[1].begin(), lanes[1].end());
    
    unsigned short i = 0;
    while (i < all_lanes.size())
    {
        all_lanes[i]->update();
        i++;
    }
}

//  Returns a free lane on the road, if any.
Lane* Road::get_lane_to(const Roundabout* roundabout) const
{
    unsigned short
        i = 0,
        j = 0;
    if (roundabout == extremities[0])
    {
        i = 1;
    }
    else if (roundabout != extremity[1])
    {
        return NULL;
    }

    while (j < lanes[i].size())
    {
        if (lanes[i][j].free())
        {
            return lanes[i][j];
        }

        j++;
    }

    if (lanes[i].size())
    {
        return lanes[i][0];
    }

    return NULL
}

//  Returns the unit parallel and perpendicular vectors to a the road, oriented towards the given roundabout.
vector<Vector> Road::reference(const Roundabout* roundabout) const
{
    vector<Vector> result(2);

    //   Avoid recomputing them each time
    if (parallel != NULL) && (orthogonal != NULL)
    {
        result[0] = parallel;
        result[1] = orthogonal;
    else
    {
        //   Normalized parallel and orthogonal vectors
        parallel    = result[0]   = (extremity[1]->position() - extremity[0]->position()).normalize();
        orthogonal  = result[1]   = parallel.get_orthogonal();
    }

    return result;
}

//  Sets the state of the traffic lights on the road.
void Road::open(roundabout, direction)
{
    unsigned short i = 0;
    if (roundabout == extremity[1])
    {
        i = 1;
    }
    else if (roundabout != extremity[0])
    {
        return void;
    }

    //   Update if necessary
    semaphores[i][direction].open();
}

//  Returns whether there is still room on the road.
//  The road is free if at least one of its lane is free.
bool Road::free(const Roundabout* roundabout) const
{
    unsigned short
        i = 0,
        j = 0;
    if (roundabout == extremity[0])
    {
        i = 1;
    }
    else if (roundabout != extremity[1])
    {
        return false;
    }
    
    while (j < lanes[i].size())
    {
        if (lanes[i].free())
        {
            return true;
        }

        j++;
    }

    return false;
}

//  Returns the total number of waiting vehicles on the road.
unsigned short Road::total_waiting_vehicles(const Roundabout* destination) const
{
    unsigned short
        i       = 0,
        j       = 0,
        result  = 0;
    
    if (destination == extremity[0])
    {
        i = 1;
    }
    else if (destination != extremity[1])
    {
        return 0;
    }

    while (j < lanes[i].size())
    {
        result += lanes[i][j]->total_waiting_vehicles();
        j++;
    }

    return result;
}

//  Returns the width of the road, which is the sum of its lanes' width
unsigned float Road::width() const
{
    unsigned float result = 0;
    unsigned short i = 0;

    while (i < lanes[0].size())
    {
        result += lanes[0][i]->width();
        i++;
    }

    i = 0;
    while (i < lanes[1].size())
    {
        result += lanes[1][i]->width();
        i++;
    }

    return result;
}

//  Returns the calculated length of the road.
unsigned short Road::length() const
{
    return (extremities[0].position - extremities[1].position).norm();
}

//  Returns True if the road is one-way, and False otherwise.
bool Road::is_one_way() const
{
    if (lanes[0].size() && lanes[1].size())
    {
        return false;
    }
    
    return true;
}

//  Returns the total number of vehicles on the road
unsigned short Road::total_vehicles() const
{
    unsigned short
        i       = 0,
        result  = 0;
    vector<Lane*> all_lanes(all_lanes());
    
    while (i < all_lanes.size())
    {
        result += allanes[i]->total_vehicles();
        i++;
    }

    return result;
}
    
//  Returns the weight associated to the road, for pathfinding computations.
//  Here, the weight is the time needed to walk the road.
unsigned float Road::weight() const
{
    unsigned float result = length/max_speed;

    //for lane in lanes:
    //    if len(lane.vehicles)
    //        buffer = lane.vehicles[0].length_covered / 5 + (length - lane.vehicles[0].length_covered) / max_speed
    //    else:
    //        return length/max_speed
    //
    //    if buffer < result:
    //        result = buffer

    return result;
}

    
//  Returns the track to which the road belongs.
//  This property is provided for convenience.
Map* Road::map() const
{
    return extremities[0]->track();
}

