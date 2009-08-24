#include <iostream>

#include "lane.hpp"
#include "road.hpp"
#include "roundabout.hpp"
#include "vehicle.hpp"

using namespace std;


//  Default features
//Lane::DEFAULT._width(5);


//  Constructor/destructor
Lane::Lane() :// : m_width(Lane::DEFAULT.width())
        m_reference(),
        m_road(),
        m_semaphore(),
        m_slots(),
        m_direction(),
        m_vehicles() 
{}

Lane::Lane(Road* new_road, bool new_direction) :
        m_reference(),
        m_road(new_road),
        m_semaphore(),
        m_slots(),
        m_direction(new_direction),
        m_vehicles() {
    m_slots[TO] = to()->book_slot(this);
    m_slots[FROM] = from()->book_slot(this);
}

//  Destroy slots and release vehicles
Lane::~Lane() {
    delete m_slots[0];
    delete m_slots[1];
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
void Lane::_light(gate, state)



    //   Update if necessary
    if gate ==  ENTRANCE:
    if road.lights[start][gate] != state:
road.last_lights_update[start][gate]   = lib.clock()
    road.lights[start][gate]               = state
    else:
    if road.lights[end][gate] != state:
road.last_lights_update[end][gate]   = lib.clock()
    road.lights[end][gate]               = state*/

//  Accessors
Class Lane::get_class() const {
    return LANE;
}

Vehicle* Lane::last_vehicle() const {
    if (m_vehicles.size())    return m_vehicles.back();
    return 0;
}


//  Get the load of the lane
float Lane::load() const {
    if (!length())  return 0;

    unsigned short  i(0);
    float           result(0);
    while (i < m_vehicles.size()) {
        if (m_vehicles[i]->is_waiting())    result += m_vehicles[i]->length() + HEADWAY;
        i++;
    }

    result /= length();

    return result;
}


//  Returns the track to which the lane belongs (provided for convenience)
Map* Lane::map() const {
    return m_road->map();
}

Semaphore Lane::semaphore() const {
    return m_semaphore;
}

//
Road* Lane::road() const {
    return m_road;
}

Slot* Lane::slot(unsigned short i) const {
    if (i != TO && i != FROM)    return 0;

    return m_slots[i];
}

Vehicle* Lane::vehicle(unsigned int i) const {
    if (i >= m_vehicles.size())    return 0;

    return m_vehicles[i];
}

unsigned short Lane::vehicles_count() const {
    return m_vehicles.size();
}


unsigned int Lane::max_speed() const {
    return m_road->max_speed();
}

//  Returns the number of waiting vehicles on the lane.
unsigned short Lane::waiting_vehicles_count() const {
    unsigned short result(0), i(0);
    
    while (i < m_vehicles.size()) {
        if (m_vehicles[i]->is_waiting())    result++;

        i++;
    }
    
    return result;
}


//  Returns whether there is still room on the road
bool Lane::is_free() const {
    //   I guess there is still room as long as the last vehicle engaged on the road if far enough from the start of the road
    if (!(m_vehicles.size()))   return true;
    
    return (m_vehicles.back()->length_covered() > Vehicle::DEFAULT_CAR.length() + HEADWAY + Vehicle::DEFAULT_CAR.length());
}


//  Get the origin/destination of the lane (provided for convenience)
Roundabout* Lane::to() const {
    return m_road->extremity(m_direction);
}
Roundabout* Lane::from() const {
    return m_road->extremity(1 - m_direction);
}


//  Returns the length of the lane, which is exactly the same as the length of its road (provided for convenience)
float Lane::length() const {
    return m_road->length();
}


//  Get lane reference
complex<float> Lane::u() const {
    complex<float> result = *(to()) - *(from());
    result = result/(complex<float>)abs(result);
    return result;
}

complex<float> Lane::v() const {
    complex<float> tmp = u();
    return complex<float>(-imag(tmp), real(tmp));
}


void Lane::close() {
    m_semaphore.set(RED);
}

void Lane::host(Vehicle* vehicle) {
    m_vehicles.push_back(vehicle);
}

void Lane::open() {
    m_semaphore.set(GREEN);
}

void Lane::release(Vehicle* vehicle) {
    unsigned short i(0);
    while (i < m_vehicles.size()) {
        if (m_vehicles[i] == vehicle) {
            m_vehicles.erase(m_vehicles.begin() + i);
            break;
        }

        i++;
    }
}


//  Update the lane => update all vehicles on it
void Lane::update(float delta_t) {
    unsigned short i(0);
    while (i < m_vehicles.size()) {
        m_vehicles[m_vehicles.size() - 1 - i]->update(delta_t);
        i++;
    }
}
