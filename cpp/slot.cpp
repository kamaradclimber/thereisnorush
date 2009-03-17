#include "slot.hpp"


//  Constructors & destructor
Slot::Slot()
{

}

Slot::Slot(const Slot& new_slot)
{
    roundabout  = new_slot.get_roundabout();
    road        = new_slot.get_road();
    vehicle     = new_slot.get_vehicle();
}

Slot::~Slot()
{
}


//  Accessors
Roundabout* Slot::get_roundabout() const
{
    return roundabout;
}

Roundabout* Slot::other_side() const
{
    if (is_connected())
    {
        return road->other_extremity(roundabout);
    }

    return Roundabout*();
}

Road* Slot::get_road() const
{
    return road;
}

Vehicle* Slot::get_vehicle() const
{
    return vehicle;
}

bool Slot::is_connected() const
{
    if (road != NULL)
    {
        return true;
    }

    return false;
}


//  Mutators
void Slot::connect_to(const Road* new_road)
{
    road = new_road;
}

//  Operators
Slot& Slot::operator=(const Slot& slot)
{
    roundabout  = slot.get_roundabout();
    road        = slot.get_road();
    vehicle     = slot.get_vehicle();
    
    return *this;
}
