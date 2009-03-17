#include "constants.hpp"
#include "lib.hpp"
#include "roundabout.hpp"
#include "vehicle.hpp"

using namespace std;

//  Default features
Roundabout::DEFAULT.set_color(QColor(Qt::red));
Roundabout::DEFAULT.set_height(3);
Roundabout::DEFAULT.set_max_slots(5);
Roundabout::DEFAULT.set_radius(10);
Roundabout::DEFAULT.set_rotation_speed(10);
Roundabout::DEFAULT.set_spawn_delay(2000);
Roundabout::DEFAULT.set_spawning(false);
Roundabout::DEFAULT.set_width(3);

//float ROUNDABOUT_ROTATION_RATE = 0.5;


//  Constructor/destructor
Roundabout::Roundabout() : radius(Roundabout::DEFAULT.get_radius()), max_slots(Roundabout::DEFAULT.get_max_slots()), rotation_speed(Roundabout::DEFAULT.get_rotation_speed()), spawning(Roundabout::DEFAULT.is_spawning()), spawn_delay(Roundabout::DEFAULT.get_spawn_delay())
{
}

Roundabout::Roundabout(Map* new_map, unsigned short new_x, unsigned short new_y) :
    map(new_map),
    position(new_x, new_y),
    radius(Roundabout::DEFAULT.get_radius()),
    max_slots(Roundabout::DEFAULT.get_max_slots()),
    rotation_speed(Roundabout::DEFAULT.get_rotation_speed()),
    slotss(),
    spawning(Roundabout::DEFAULT.is_spawning()),
    last_spawn(clock()),
    last_shift(clock()),
    spawn_delay(Roundabout::DEFAULT.get_spawn_delay()),
    local_load(0)
{
    //vehicle_spiraling_time = {}
}

Roundabout::~Roundabout()
{
}


//  Accessors
Slot* Roundabout::slot(unsigned short i) const
{
    return slotss[i];
}

unsigned short Roundabout::total_slots() const
{
    return slotss.size();
}

//  Connects a road to a slot, must be called during initialization.
void Roundabout::host(const Road* new_road)
{
    srand(time(NULL));

    //  Choose a random free slot, if any, to allocate for the road
    //  TODO : prevent from infinite loop !
    Slot* slot = slotss[rand() % slotss.size()]
    while (slot->road() != NULL)
    {
        slot = slotss[rand() % slotss.size()]
    }
    
    slot->connect_to(new_road);
}

//  Handles traffic lights.
void Roundabout::update_semaphores()
{
    //   Get the most loaded parent and lane
    Roundabout*     most_loaded_parent  = parents[0];
    Lane*           most_lested_lane    = chosen_one->get_lane_to(this);
    unsigned short  i                   = 0;

    while (i < slotss.size())
    {
        //  The road hasn't got any lane leading to this roundabout => go to next slot
        if (!slotss[i]->road()->can_lead_to(this))
        {
            continue;
        }
        
        Roundabout* parent = slotss[i]->other_extremity();

        if (parent->global_load() > most_loaded_parent->global_load())
        {
            most_loaded_parent  = parent;
            Lane* lane          = parent->get_lane_to(this);

            if (lane->total_vehicles() > most_loaded_lane->total_vehicles())
            {
                most_loaded_lane = lane;
            }
        }

        i++;
    }

    //   Open the way FROM this one, and close ways FROM others
    i = 0;
    while (i < slotss.size())
    {
        if (slotss[i]->other_extremity() == chosen_one)
        {
            slotss[i]->set_semaphore(ENTRANCE, true);
        }
        else
        {
            slotss[i]->set_semaphore(ENTRANCE, false);
        }

        i++;
    }

    //  Open the most lested lane (and do not close the others)
    most_loaded_lane->slot(this)->set_semaphore(ENTRANCE, true);

    //   Then, let's update each road, few rules because the general view overrules the local one.
    i = 0;
    while (i < slotss.size())
    {
        if (slotss[i]->road() != NULL
        &&  slotss[i]->road()->can_lead_to(this)
        &&  slotss[i]->semaphore(ENTRANCE)->last_update() - clock() > WAITING_TIME_LIMIT
        &&  slotss[i]->total_waiting_vehicles())
        {
            slotss[i]->set_semaphore(ENTRANCE, true);
        }

        i++;
    }
}

//  Updates a given vehicle on the roundabout 
void Roundabout::update(Vehicle* vehicle)
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
void Roundabout::update()
{
    unsigned short i = 0;
    //   Make the cars rotate
    if (clock() - last_shift > ROUNDABOUT_ROTATION_RATE)
    {
        Vehicle* temp = slotss.back()->vehicle();

        i = total_slots();
        while (i > 0)
        {
            slotss[i]->set_vehicle(slotss[i - 1]->vehicle());
            i--;
        }
        slotss[i]->set_vehicle(temp);

        last_shift = clock();
    } 
    
    //   Spawning mode
    if (spawning && (clock() - last_spawn > spawn_delay))
    {
        srand(time(NULL));

        Slot* slot = slotss[rand() % total_slots()];
        //  TODO : prevent from infinite loop !
        while (slot->vehicle() != NULL)
        {
            slot = slotss[rand() % total_slots()];
        }

        unsigned short  random  = rand() % 100;
        VehicleType     type    = STANDARD_CAR;
        
        if (80 <= random < 95)
        {
           type = TRUCK;
        }
        else if (95 <= random < 100)
        {
            type = SPEED_CAR;
        }

        Vehicle new_vehicle(slot, type);
        
        last_spawn = clock();
    }

    //   Update traffic lights
    update_semaphores();

    //   Update vehicles
    i = 0;
    while (i < total_slots())
    {
        update(slotss[i]->vehicle());
        i++;
    }

    /*   Kill vehicles that have reached their destination
            for vehicle in to_kill:
                vehicle_slot = lib.find_key(slots_vehicles, vehicle)
                    slots_vehicles[vehicle_slot] = None
                    vehicle.die()

                    to_kill = []*/

//  Computes in per cent a number called load (inspired by the load of a Linux station)
float Roundabout::get_local_load() const
{
    unsigned float roads_sum    = 0;
    unsigned short i            = 0;

    while (i < total_slots())
    {
        if (!(slotss[i]->road()->can_lead_to(this)))
        {
            continue;
        }
        
        roads_sum += slotss[i]->total_waiting_vehicles() * VEHICLE[STANDARD_CAR][DEFAULT_LENGTH] / slotss[i]->road()->length();
        
        i++;
    }
    
    return (roads_sum + total_vehicles()) / (float)(max_slots);
}

/*  Returns the first road found, if any, that can lead to the given roundabout.
//  Returns None if no road is found.
//  /!\ A road is returned only if it has a lane that leads to the given roundabout !
Road* Roundabout::get_road_to(const Roundabout* roundabout) const
{
    for road in hosted_roads:
        for lane in road.lanes:
            if lane.end == roundabout:
                return road

                    return None*/

//  Returns whether there is no place left on the roundabout.
bool Roundabout::is_full() const
{
    unsigned short i = 0;

    while (i < total_slots())
    {
        if (slotss[i]->vehicle() == NULL)
        {
            return false;
        }

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

//  Returns the number of vehicles waiting on all the incoming roads connected to this roudabout.
unsigned short Roundabout::total_waiting_vehicles() const
{
    unsigned short
        result  = 0,
        i       = 0;

    while (i < total_slots())
    {
        result += slotss[i]->total_waiting_vehicles();
        i++;
    }
    
    return result;
}

float Roundabout::global_load() const
{
    unsigned float result   = 1 + local_load() * 10  // The "1 +" is only to avoid zero-division ;
    unsigned short i        = 0;

    while (i < total_slots())
    {
        if (slotss[i]->road()->can_lead_to(this))
        {
            result += slotss[i]->other_extremity()->local_load();
        }
        
        i++;
    }

    return result;
}
