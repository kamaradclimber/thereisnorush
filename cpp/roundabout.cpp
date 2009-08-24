#include <algorithm>
#include <iostream>

#include "lane.hpp"
#include "map.hpp"
#include "road.hpp"
#include "roundabout.hpp"
#include "slot.hpp"
#include "vehicle.hpp"

using namespace std;

Roundabout Roundabout::DEFAULT = Roundabout();
    

//  Default features
Roundabout::Roundabout() :
    complex<float>(),
    m_is_spawning(false), 
    m_g_cost(0),
    m_h_cost(0),
    m_last_spawn(0),
    m_last_shift(0),
    m_local_load(0),
    m_shift_delay(10),
    m_spawn_delay(2),
    m_map(0),
    m_color(QColor(Qt::red)),
    m_destination(0),
    m_nearest_parent(0),
    m_roads(),
    m_slots() {}


Roundabout::Roundabout(Map* new_map, unsigned short new_x, unsigned short new_y) :
    complex<float>((float)new_x, (float)new_y),
    m_is_spawning(false), 
    m_g_cost(0.),
    m_h_cost(0),
    m_last_spawn(0),
    m_last_shift(0),
    m_local_load(0),
    m_shift_delay(10),
    m_spawn_delay(2),
    m_map(new_map),
    m_color(QColor(Qt::red)),
    m_destination(0),
    m_nearest_parent(0),
    m_roads(),
    m_slots() {
        //vehicle_spiraling_time = {}
}

Roundabout::~Roundabout() {}


//  Accessors
QColor Roundabout::color() const {
    return m_color;
}

float Roundabout::f_cost() const {
    return m_g_cost + m_h_cost;
}

float Roundabout::g_cost() const {
    return m_g_cost;
}

float Roundabout::h_cost() const {
    return m_h_cost;
}

bool Roundabout::is_spawning() const {
    return m_is_spawning;
}

Map* Roundabout::map() {
    return m_map;
}

Roundabout* Roundabout::nearest_parent() {
    return m_nearest_parent;
}

Slot* Roundabout::slot(unsigned short i) {
    if (i < m_slots.size())     return m_slots.at(i);
    
    return 0;
}

float Roundabout::shift_delay() const {
    return m_shift_delay;
}

float Roundabout::spawn_delay() const {
    return m_spawn_delay;
}

unsigned short Roundabout::slots_count() const {
    return m_slots.size();
}

Slot* Roundabout::free_slot() {
    unsigned short i(0);
    while (i < m_slots.size()) {
        if (m_slots[i]->is_free())  return m_slots[i];
        
        i++;
    }

    return 0;
}


//  Mutators
Slot* Roundabout::book_slot(Lane* lane) {
    Slot* new_slot = new Slot(this, lane);
    m_slots.push_back(new_slot);
    
    return new_slot;
}

/*void Roundabout::set_f_cost(float value) {
    m_f_cost = value;
}*/

void Roundabout::set_g_cost(float value) {
    m_g_cost = value;
}

void Roundabout::set_h_cost(float value) {
    m_h_cost = value;
    //m_f_cost = m_g_cost + m_h_cost;
}

void Roundabout::set_destination(Roundabout* destination) {
    m_destination = destination;
}

void Roundabout::set_nearest_parent(Roundabout* parent) {
    m_nearest_parent = parent;
}

void Roundabout::set_spawn_delay(float delay) {
    m_spawn_delay = delay;
}

void Roundabout::set_spawning(bool state) {
    m_is_spawning = state;
}


// TODO
/*  Connects a road to a slot, must be called during initialization.
void Roundabout::host(const Road* new_road) {
    //  Already hosted => nothing to do
    if (binary_search(m_roads.begin(), m_roads.end(), new_road))
        return void();
    
    
    unsigned short i(0), j(0);
    while (j < 2) {
        while (i < new_road.total_lanes_to(j)) {
            Slot* slot = new Slot(this, new_road.lane(j, i));
            i++;
        }

        i = 0;
        j++;
    }

    slot->connect_to(new_road);
}*/

//  Build a road between current roundabout and the given one
//  CONVENTION SENSITIVE : lanes_to deals with the count of lanes going from the current roundabout to the given one
void Roundabout::connect_to(Roundabout* roundabout, unsigned short lanes_from, unsigned short lanes_to) {
    //  TODO : check if already connected
    Road* new_road = new Road(this, roundabout, lanes_from, lanes_to);
    m_roads.push_back(new_road);
}


//  Handles traffic lights.
void Roundabout::update_semaphores() {
    // TODO : update every X seconds, and not permanently
    //   Get the most loaded parent and lane
    Roundabout*     most_loaded_parent(0);
    Lane*           most_loaded_lane(0);
    
    Roundabout* parent(0);
    unsigned short  i(0);

    while (i < m_slots.size()) {
        //  The lane doesn't lead to this roundabout => go to next slot
        if (m_slots[i]->lane()->from() == this)   {i++; continue;}
        
        parent = m_slots[i]->lane()->from();

        if (!most_loaded_parent || parent->global_load() > most_loaded_parent->global_load())   most_loaded_parent  = parent;
        if (!most_loaded_lane || m_slots[i]->lane()->load() > most_loaded_lane->load())         most_loaded_lane = m_slots[i]->lane();

        i++;
    }

    //   Open the way FROM this one, and close ways FROM others
    i = 0;
    while (i < m_slots.size()) {
        if (m_slots[i]->lane()->from() == most_loaded_parent)   m_slots[i]->lane()->open();
        else                                                    m_slots[i]->lane()->close();

        i++; 
    }

    //  Open the most lested lane (and do not close the others)
    most_loaded_lane->open();

    //   Then, let's update each road, few rules because the general view overrules the local one.
    i = 0;
    while (i < m_slots.size()) {
        if (m_slots[i]->lane()->to() == this
        &&  m_slots[i]->lane()->semaphore().last_update() - clock() > 100000
        &&  m_slots[i]->waiting_vehicles_count())
            m_slots[i]->lane()->open();

        i++;
    }
}

//  Updates a given vehicle on the roundabout 
/*void Roundabout::update(Vehicle* vehicle)
{
    if not (vehicle in vehicle_spiraling_time)
    vehicle_spiraling_time[vehicle] = [vehicle.total_waiting_time, lib.clock()]

    vehicle.total_waiting_time = vehicle_spiraling_time[vehicle][0] + lib.clock() - vehicle_spiraling_time[vehicle][1]

    if (vehicle.path is not None) and (len(vehicle.path)) and len(children)
next_way        = vehicle.next_way()

    //   The vehicle has lost its slot   
    if vehicle.slot is None:
    raise Exception("ERROR (in Roundabout.update_vehicle()) : a vehicle has no slot !")

                                                              //   The vehicle's slot is in front of a leaving road
                                                              if (slots_roads[vehicle.slot] is not None) and (slots_roads[vehicle.slot] == next_way) and (next_way.is_free(next_way.other_extremity(self)))
    //la route sur laquelle on veut aller est vidée et surtout _en face_  du slot de la voiture
vehicle.join(vehicle.next_way(False)) // cette fois on fait une lecture destructive

    //la voiture n'a pas d'endroit où aller : on la met dans le couloir de la mort
    else:
to_kill.append(vehicle)*/

//  Updates the roundabout : rotate the vehicles, dispatch them...
void Roundabout::update(float delta_t) {
    unsigned short i(0);

    //   Make the cars rotate
    if (clock() - m_last_shift > DEFAULT.shift_delay() && slots_count()) {
        Vehicle* temp = m_slots.back()->vehicle();
        if (temp)   temp->join(0);

        i = slots_count() - 1;
        while (i) {
            if (m_slots[i-1]->vehicle())    m_slots[i-1]->vehicle()->join(m_slots[i]);
            i--;
        }
        
        if (temp)   temp->join(m_slots[i]);

        m_last_shift = clock();
    } 
    
    //   Spawning mode
    if (m_is_spawning && (clock() - m_last_spawn > m_spawn_delay)) {
        srand(time(0));

        Slot* slot = free_slot();
        if (slot) {
            unsigned short  random(rand() % 100);
            VehicleModel    model(CAR);
            
            if (80 <= random && random < 95)            model = TRUCK;
            else if (95 <= random && random < 100)      model = SPEED_CAR;
    
            Vehicle* new_vehicle = new Vehicle(model);
            new_vehicle->join(slot);
            new_vehicle->set_destination(map()->roundabout(rand() % map()->roundabouts_count()));

            
            m_last_spawn = clock();
        }
    }

    //   Update traffic lights
    update_semaphores();

    //   Update vehicles
    i = 0;
    while (i < slots_count()) {
        if (!m_slots[i]->is_free())     m_slots[i]->vehicle()->update(delta_t);
        i++;
    }

    /*   Kill vehicles that have reached their destination
            for vehicle in to_kill:
                vehicle_slot = lib.find_key(slots_vehicles, vehicle)
                    slots_vehicles[vehicle_slot] = None
                    vehicle.die()

                    to_kill = []*/
}

//  Computes in per cent a number called load (inspired by the load of a Linux station)
float Roundabout::local_load() const {
    float           result(0);
    unsigned short  i(0);

    while (i < slots_count()) {
        if (m_slots[i]->lane()->to() != this)   {i++; continue;}

        result += m_slots[i]->lane()->load();
        i++;
    }
    
    return (result + vehicles_count()) / (2*m_slots.size());
}

/*  Returns the first road found, if any, that can lead to the given roundabout.
//  Returns None if no road is found.
//  /!\ A road is returned only if it has a lane that leads to the given roundabout !
Road* Roundabout::_road_to(const Roundabout* roundabout) const
{
    for road in hosted_roads:
        for lane in road.lanes:
            if lane.end == roundabout:
                return road

                    return None*/

//  Returns whether there is no place left on the roundabout.
bool Roundabout::is_full() const {
    unsigned short i(0);

    while (i < slots_count()) {
        if (m_slots[i]->vehicle() == 0)     return false;

        i++;
    }

    return true;
}

/*Roundabout::hosted_roads(self)

    Returns the list of the roads connected to the roundabout.
    The result is the list slots_roads from which None elements are removed.


    result = []
    for road in slots_roads:
    if road is not None:
result.append(road)

    return result

    @property
Roundabout::children(self)

    Returns the list of the nearby roundabouts for which it exists a lane from the roundabout to go to.


    result = []
    for road in hosted_roads:
    for lane in road.lanes:
    if lane.end != self and not (lane.end in result)
result.append(lane.end)

    return result

    @property
Roundabout::parents(self)

    Returns the list of the nearby roundabouts from which it exists a lane to go to the roundabout.


    result = []
    for road in hosted_roads:
    for lane in road.lanes:
    if lane.start != self and not (lane.start in result)
result.append(lane.start)

    return result

    @property
Roundabout::neighbours(self)

    Returns the list of the nearby roundabouts.
    /!\ This list is not the concatenation of the lists "parents" and "children", because those lists may have common elements !


    result = []
    for road in hosted_roads:
result.append(road.other_extremity(self))   // this suppose that there is at most 1 road between 2 roundabouts

    return result

    //   The two following properties are deprecated, other properties are enough to retrieve this piece of information -- Ch@hine
    @property
Roundabout::incoming_lanes(self)




    result = []
    for road in slots_roads:
    if road is None:
    continue

    for lane in road.lanes:
    if lane.end == self:
result.append(lane)

    return result

    @property
Roundabout::leaving_lanes(self)




    result = []
    for road in slots_roads:
    if road is None:
    continue

    for lane in road.lanes:
    if lane.end == self:
result.append(lane)

    return result

    @property*/

unsigned short Roundabout::vehicles_count() const {
    unsigned short result(0), i(0);

    while (i < m_slots.size()) {
        if (m_slots[i]->vehicle() != 0)
            result++;

        i++;
    }

    return result;
}

//  Returns the number of vehicles waiting on all the incoming roads connected to this roudabout.
unsigned short Roundabout::waiting_vehicles_count() const
{
    unsigned short
        result  = 0,
        i       = 0;

    while (i < slots_count()) {
        if (m_slots[i]->lane()->from() == this)     {i++; continue;}

        result += m_slots[i]->lane()->waiting_vehicles_count();
        i++;
    }
    
    return result;
}

float Roundabout::global_load() const {
    float result(local_load());  // The "1 +" is only to avoid zero-division ;
    unsigned short i(0);

    while (i < slots_count()) {
        if (m_slots[i]->lane()->to() == this)   result += m_slots[i]->lane()->from()->local_load();
        
        i++;
    }

    return result/(m_slots.size() + 1);
}
