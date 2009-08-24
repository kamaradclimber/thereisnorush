#include <iostream>

#include "lane.hpp"
#include "roundabout.hpp"
#include "slot.hpp"

using namespace std;


//  Constructors & destructor
Slot::Slot() {
}

Slot::Slot(Roundabout* roundabout, Lane* lane) :
        m_lane(lane),
        m_roundabout(roundabout),
        m_vehicle(0) {}
/*Slot::Slot(const Slot& new_slot)
{
    roundabout  = new_slot._roundabout();
    road        = new_slot._road();
    vehicle     = new_slot._vehicle();
}*/

Slot::~Slot()
{
}


//  Accessors
Class Slot::get_class() const {
    return SLOT;
}

Lane* Slot::lane() const {
    return m_lane;
}

Map* Slot::map() const {
    return m_roundabout->map();
}

Roundabout* Slot::roundabout() const {
    return m_roundabout;
}

Semaphore* Slot::semaphore() {
    return &m_semaphore;
}

Vehicle* Slot::vehicle() const {
    return m_vehicle;
}

bool Slot::is_free() const {
    if (!m_vehicle)
        return true;

    return false;
}

/*bool Slot::is_connected() const
{
    if (road != NULL)
    {
        return true;
    }

    return false;
}*/

/*Roundabout* Slot::other_side() const {
    if (is_connected())
        return road->other_extremity(roundabout);

    return Roundabout*();
}*/

unsigned short Slot::waiting_vehicles_count() const {
    return m_lane->waiting_vehicles_count();
}



//  Mutators
/*void Slot::connect_to(const Road* new_road) {
    road = new_road;
}*/


void Slot::host(Vehicle* vehicle) {
    if (!m_vehicle)
        m_vehicle = vehicle;
}

void Slot::release(Vehicle* vehicle) {
    if (!vehicle) {
        m_vehicle = 0;
        return void();
    }

    if (m_vehicle == vehicle)
        m_vehicle = 0;
}

//  Operators
/*Slot& Slot::operator=(const Slot& slot) {
    roundabout  = slot.roundabout();
    road        = slot.road();
    vehicle     = slot.vehicle();
    
    return *this;
}*/
