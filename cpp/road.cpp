#include <complex>
#include <iostream>

#include "lane.hpp"
#include "road.hpp"
#include "roundabout.hpp"

using namespace std;

Road Road::DEFAULT = Road();


//  Build almost nothing (shouldn't be used)
Road::Road() : m_max_speed(50), m_color(QColor(Qt::white)) {}


//  Build a road between 2 roundabouts
Road::Road(Roundabout* roundabout1, Roundabout* roundabout2, unsigned short total_lanes1, unsigned short total_lanes2)  :
        m_color(QColor(Qt::white)),
        m_extremities(),
        m_max_speed(50),
        m_lanes(),
        m_vehicles() { 
    //  TODO
    //if (roundabout1->map() != roundabout2->map())        
        //throw(unsigned int i(0));

    //  Connect to extremities
    m_extremities[0] = roundabout1;
    m_extremities[1] = roundabout2;
    
    //  Build lanes
    m_lanes[0].resize(total_lanes1);
    m_lanes[1].resize(total_lanes2);

    unsigned short i(0);
    while (i < total_lanes1) {
        m_lanes[0][i] = new Lane(this, 0);
        i++;
    }

    i = 0;
    while (i < total_lanes2) {
        m_lanes[1][i] = new Lane(this, 1);
        i++;
    }
}


//  Destroy lanes
Road::~Road() {
    unsigned short i(0), j(0);
    while (j < 2) {
        while (i < m_lanes[j].size()) {
            delete m_lanes[j][i];
            i++;
        }
        
        j++;
        i = 0;
    }
}


//  Accessors
QColor Road::color() const {
    return m_color;
}

unsigned short Road::max_speed() const {
    return m_max_speed;
}

unsigned short Road::lanes_count() const {
    return m_lanes[0].size() + m_lanes[1].size();
}

unsigned short Road::lanes_count(unsigned short i) const {
    return m_lanes[i].size();
}

unsigned short Road::total_lanes_to(unsigned short i) const {
    return m_lanes[i].size();
}

Roundabout* Road::extremity(unsigned short i) {
    return m_extremities[i];
}

Lane* Road::lane(unsigned short direction, unsigned short i) {
    return m_lanes[direction][i];
}


//  Mutators
void Road::set_color(QColor new_color) {
    m_color = new_color;
}

void Road::set_max_speed(unsigned short new_value) {
    m_max_speed = new_value;
}

//  Given a roundabout, returns the other roundabout extremity of the road.
//  Returns NULL if the given roundabout is not an extremity of the road.
//  DEPRECATED
/*Roundabout* Road::other_extremity(const Roundabout* roundabout) const {
    if (roundabout == extremities[0])
        return extremities[1];
    else if (roundabout == extremities[1])
        return extremities[0];

    return NULL;
}*/


//  Returns True if the road has a lane that goes to the given roundabout, and False otherwise.
//  DEPRECATED
/*bool Road::can_lead_to(const Roundabout* roundabout) const {
    //   The road is not even connected to the roundabout => the answer is False
    if (roundabout == extremities[0])
        return lanes[1].size() > 0;
    else if (roundabout == extremities[1])
        return lanes[0].size() > 0;
}*/


//  Returns the unit parallel and perpendicular vectors to a the road, oriented towards the given roundabout.
//  DEPRECATED
/*complex<float>* Road::reference(const Roundabout* roundabout) const {
    complex<float> result[2] = lanes[0]->reference();

    if (lanes[0]->direction() != roundabout)
        return -(result);

    return result;
}*/


//  Update recursively the lanes and vehicles on the road
void Road::update(float delta_t) {
    unsigned short i(0), j(0);
    
    while (j < 2) {
        while (i < m_lanes[j].size()) {
            m_lanes[j][i]->update(delta_t);
            i++;
        }

        j++;
        i = 0;
    }
}

//  Returns a free lane on the road, if any.
//  DEPRECATED
/*Lane* Road::lane_to(const Roundabout* roundabout) const {
    unsigned short
        i = 0,
        j = 0;
    if (roundabout == extremities[0])
        i = 1;
    else if (roundabout != extremity[1])
        return NULL;

    while (j < lanes[i].size())
    {
        if (lanes[i][j].free())
            return lanes[i][j];

        j++;
    }

    if (lanes[i].size())
        return lanes[i][0];

    return NULL
}*/

//  Sets the state of the traffic lights on the road.
/*void Road::open(roundabout) {
    unsigned short i = 0;
    if (roundabout == extremity[1])
        i = 1;
    else if (roundabout != extremity[0])
        return void;

    //   Update if necessary
    semaphores[i][direction].open();
}*/

//  Returns whether there is still room on the road.
//  The road is free if at least one of its lane is free.
//  CONVENTION SENSITIVE : the given roundabout is the *direction*
//  DEPRECATED
/*bool Road::is_free(const Roundabout* direction) const {
    unsigned short
        i = 0,
        j = 0;
    if (direction == extremity[0])
        i = 1;
    else if (direction != extremity[1])
        return false;
    
    while (j < lanes[i].size()) {
        if (lanes[i].free())
            return true;

        j++;
    }

    return false;
}*/

//  Returns the total number of waiting vehicles on the road.
/*unsigned short Road::total_waiting_vehicles(const Roundabout* destination) const {
    unsigned short
        i       = 0,
        j       = 0,
        result  = 0;
    
    if (destination == extremity[0])
        i = 1;
    else if (destination != extremity[1])
        return 0;

    while (j < lanes[i].size())
    {
        result += lanes[i][j]->total_waiting_vehicles();
        j++;
    }

    return result;
}*/

//  Returns the width of the road, which is the sum of its lanes' width
/*unsigned float Road::width() const
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
}*/

//  Returns the calculated length of the road.
unsigned short Road::length() const {
    complex<float> result = *(m_extremities[0]) - *(m_extremities[1]);
    return abs(result);
}

//  Returns True if the road is one-way, and False otherwise.
/*bool Road::is_one_way() const
{
    if (lanes[0].size() && lanes[1].size())
        return false;
    
    return true;
}*/

//  Returns the total number of vehicles on the road
unsigned short Road::vehicles_count() const {
    unsigned short i(0), j(0), result(0);
    
    while (j < 2) {
        while (i < m_lanes[j].size()) {
            result += m_lanes[j][i]->vehicles_count();
            i++;
        }

        j++;
        i = 0;
    }

    return result;
}

unsigned short Road::waiting_vehicles_count() const {
    unsigned short i(0), j(0), result(0);
    
    while (j < 2) {
        while (i < m_lanes[j].size()) {
            result += m_lanes[j][i]->waiting_vehicles_count();
            i++;
        }

        j++;
        i = 0;
    }

    return result;
}
 
    
//  Returns the weight associated to the road, for pathfinding computations.
//  Here, the weight is the time needed to cover the road.
float Road::weight() const {
    float result = length()/m_max_speed;

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

    
//  Provided for convenience
Map* Road::map() {
    return m_extremities[0]->map();
}

