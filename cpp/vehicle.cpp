#include <algorithm>

#include "constants.hpp"
#include "gps.hpp"
#include "lib.hpp"
#include "road.hpp"
#include "roundabout.hpp"

Vehicle::Vehicle(Initialization mode) : 
    path(),
    waiting(),
    width(),
    speed(),
    headway(),
    length(),
    force(),
    mass(),
    color(),
    sight_distance(),
    acceleration(),
    total_waiting_time(),
    last_waiting_time(),
    dead(),
    destination()
{
}

//  Constructor method.
Vehicle::Vehicle(Lane* new_lane, VehicleType new_type) :
    path(),
    waiting(false),
    width(DEFAULT[new_type][WIDTH]),
    speed(DEFAULT[new_type][SPEED]),
    headway(DEFAULT[new_type][HEADWAY]),
    length(DEFAULT[new_type][LENGTH]),
    force(DEFAULT[new_type][FORCE]),
    mass(DEFAULT[new_type][MASS]),
    color(DEFAULT[new_type][COLOR]),
    sight_distance(5 * DEFAULT[STANDARD_CAR][LENGTH]),
    acceleration(0),
    total_waiting_time(0),
    last_waiting_time(0),
    dead(false),
    //gps(),
    destination(NULL)
{
    /*   Several sub-categories : truck, long truck, bus
         if new_type == TRUCK:
         possible_sizes = [(2, 25), 
         (3, 60), 
         (4, 15)]

         length *= lib.proba_poll(possible_sizes)
         mass   *= length*/

    join(lane);
    generate_path();
}

//  Find (or not) the path to the given (or not) destination.
void Vehicle::generate_path(const Roundabout* new_destination)
{
    srand(time(NULL));

    Roundabout* destination(new_destination);
    if (new_destination == NULL)
    {
        // EXPERIMENTAL : leaving nodes only
        destination = map->roundabouts[rand() % map->total_roundabouts()];
    }   
    //   Compute the path
    //   Each vehicle needs its own gps instance to avoid collisions and clean pathfinding
    path = map->find_path(lane->start(), destination);

    if (!(path.size()))
    {
        destination = NULL;
    }
}

//  Allocate the vehicle to the given location. The concept of location makes it possible to use this code for either a lane or a roundabout.
//      new_location    (road or lane or Roundabout)  :   lane or roundabout that will host, if possible, the vehicle
void Vehicle::join(Road* new_road)
{   
    if (new_road == NULL)
    {
        return void;
    }

    //   Leave the current location
    Roundabout* old_roundabout = roundabout();
    slot()->free();

    Lane* chosen_lane   = new_road->get_lane_from(old_roundabout);
        chosen_lane->add_vehicle(this);
        location = chosen_lane;
    
    acceleration    = force/mass;
    length_covered  = 0;
    speed           = 5;
}

void Vehicle::join(Roundabout* new_roundabout)
{
    if (new_roundabout == NULL)
    {
        return void;
    }
    
    //   Leave the current location
    Road* old_road = road();
    lane()->remove_vehicle();

    Slot* slot = old_road->slot(new_roundabout);
        slot->host(this);
        location = slot;
}

/*  Kills the vehicle, which simply disappears.
    void Vehicle::die(this)

    if location.vehicles:
    if this in location.vehicles:
    dead = True 
    location.vehicles.remove(this)
else:
raise Except("WARNING (in vehicle.die()) : a vehicle was not in its place !")*/

//  Expresses the vehicles' wishes :P
Road* Vehicle::next_way(bool read_only)
{
    //   End of path
    if (!(path.size()))
    {
        return NULL;
    }
    
    Road* result = path[0];

    if (!read_only)
    {
        path.erase(path.begin());
    }
    
    return result;
}

//  Returns the position of the obstacle ahead of the vehicle, (obstacle, obstacle_is_light)
unsigned short Vehicle::next_obstacle()
{
    if (lane() == NULL)
    {
        return 0;
    }
    
    //   The vehicle is the first of the queue : the next obstacle is the light
    if (lane()->vehicle(0) = this)
    {
        //obstacle_is_light = True
        
        //   Green light
        if (next_slot()->opened())
        {
            return (lane()->length() + headway);
        }
        
        return lane()->length();
    }

    //   Otherwise : the next obstacle is the previous vehicle
    //obstacle_is_light = False
    unsigned short rank = rand();

    return obstacle = lane()->vehicles(rank - 1)->length_covered() - lane()->vehicles(rank - 1)->length()/2;
}

//  Moves the vehicle, THEN manages its speed, acceleration.
void Vehicle::act()
{
    //   We only manage vehicles on roads, we don't vehiclee about roundabouts
    if (lane() == NULL)
    {
        return void;
    }

    unsigned float obstacle = next_obstacle();

    //   Update the acceleration given the context
    sight_distance = (pow(speed, 2))/(2*force/mass);

    //   No obstacle at sight : « 1 trait danger, 2 traits sécurité : je fonce ! »
    if (length_covered + length/2 + sight_distance < obstacle)
    {
        acceleration = force/mass;
    }
    
    //   Visible obstacle
    else
    {
        //   Set waiting attitude
        if (lane()->vehicle(0) != this)
        {
            set_waiting(lane()->vehicles(rank() + 1)->waiting());
        }
        else if (next_slot()->opened())
        {
            set_waiting(false);
        }
        else
        {
            set_waiting(true);
        }
        
        //   Start deceleration
        unsigned float
            delta_speed     = - speed,
            delta_position  = obstacle - length_covered - length/2 - headway;
        
        if (lane()->vehicle(0) != this)
        {
            delta_speed     = previous_vehicle()->speed() - speed;
        }
                
        acceleration = 0;

        if (delta_speed)
        {
            acceleration = force/mass * delta_speed/abs(delta_speed);
        }
    }

    //   Update the position and speed given the speed and acceleration
    length_covered = min(length_covered + speed * delta_t(), obstacle - length/2 - headway);
    speed          = max(min(speed + acceleration * delta_t(), lane()->max_speed()), 5);

    //   Arrival at a roundabout
    if (length_covered >= lane()->length() - length/2 - headway)
    {
        //   Green light
        if (next_slot()->opened() && next_slot()->is_free())
        {
            set_waiting(false);
            join(next_roundabout());
        }

        //   The slot isn't free
        else
        {
            set_waiting(true);
        }
    }
}
                        
//  Changes, if needed, the waiting attitude of a vehicle
void Vehicle::set_waiting(bool new_state)
{
    //   There is no change : do nothing
    if (new_state == waiting)
    {
        return void;
    }

    waiting = new_state;
    
    //   Start a "waiting" phase : reset the counter
    if (new_state)
    {
        start_waiting_time = clock();
        last_waiting_time  = 0;
    }

    //   Stop a "waiting" phase : look at the clock
    else
    {
        last_waiting_time  = clock() - start_waiting_time;
        total_waiting_time += last_waiting_time;
    }
}

//  Returns the coordinates of the center of the vehicle.
Vector Vehicle::position()
{
    return (location->position + location->parallel() * length_covered + location->orthogonal() * location->width()/2);
}


Vehicle* Vehicle::previous_vehicle(this)
{
    if (lane() == NULL || lane()->vehicle(0) == this)
    {
        return NULL;
    }
    
    if (previous_vehicle != NULL)
    {
        return previous_vehicle;
    }
    
    vector<int>::iterator i = find(lane()->vehicle().begin(), lane()->vehicle().end(), this) - 1;
    previous_vehicle = *i;

    return previous_vehicle;
}

/*  Returns the lane where the vehicle is, if it is in a lane.
//  This property is provided for convenience.
void Vehicle::lane()
{
    if isinstance(location, __road__.Lane)
    return location

    return NULL


void Vehicle::road(this)

    Returns the road where the vehicle is, if it is in a road.
    This property is provided for convenience.


if isinstance(location, __road__.Lane)
    return location.road

    return NULL


void Vehicle::roundabout(this)

    Returns the roundabout where the vehicle is, if it is in a roundabout.
    This property is provided for convenience.


if isinstance(location, __roundabout__.Roundabout)
    return location

    return NULL


void Vehicle::slot(this)

    Returns the slot where the wehicle is, if it is in a roundabout.
    This property is provided for convenience.


    if roundabout is NULL:
    return NULL

return lib.find_key(roundabout.slots_vehicles, this)
*/

//  Returns the tracks where is the vehicle.
//  This function is provided for convenience.
Map* Vehicle::map()
{
    return roundabout()->map();
}
