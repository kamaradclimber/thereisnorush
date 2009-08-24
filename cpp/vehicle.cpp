#include <algorithm>
#include <cmath>
#include <iostream>

#include "gps.hpp"
#include "lane.hpp"
#include "road.hpp"
#include "roundabout.hpp"
#include "vehicle.hpp"

using namespace std;


Vehicle Vehicle::DEFAULT_CAR        = Vehicle();
Vehicle Vehicle::DEFAULT_SPEED_CAR  = Vehicle(SPEED_CAR);
Vehicle Vehicle::DEFAULT_TRUCK      = Vehicle(TRUCK);


//  Build a default vehicle
Vehicle::Vehicle(VehicleModel model) :
    m_is_waiting(),
    m_start_waiting_delay(0.),
    m_total_waiting_delay(0.),
    m_gps(),
    m_color(QColor(Qt::white)),
    m_force(10),
    m_length(5),
    m_length_covered(0),
    m_mass(1),
    m_speed(0),
    m_width(4),
    m_path(),
    m_location(0)
    
    /*,sight_distance(),
    total_waiting_time(),
    last_waiting_time(),
    dead(),
    destination()*/ {
    //  Speed car features
    if (model == SPEED_CAR) {
        m_force  *= 3;
        m_mass   /= 1.5;
        m_color   = QColor(Qt::red);
    }

    //  Truck features
    else if (model == TRUCK) {
        m_color   = QColor(Qt::blue);
        m_force  *= 5;
        m_mass   *= 5;
        m_length *= 3;
    }
}

//  Constructor method.
/*Vehicle::Vehicle(Lane* new_lane, VehicleModel model) :
    sight_distance(5 * DEFAULT[STANDARD_CAR][LENGTH]),
    acceleration(0),
    total_waiting_time(0),
    last_waiting_time(0),
    dead(false),
    //gps(),
    destination(NULL)
{
    if (true) {}
    //   Several sub-categories : truck, long truck, bus
         if new_type == TRUCK:
         possible_sizes = [(2, 25), 
         (3, 60), 
         (4, 15)]

         m_length *= lib.proba_poll(possible_sizes)
         mass   *= m_length

    join(lane);
    generate_path();
}*/

//  Destructor : do nothing !
Vehicle::~Vehicle() {} 

//  Accessors
QColor Vehicle::color() const {
    return m_color;
}

bool Vehicle::is_waiting() const {
    return m_is_waiting;
}

unsigned int Vehicle::length() const {
    return m_length;
}

unsigned int Vehicle::length_covered() const {
    return m_length_covered;
}

Roundabout* Vehicle::path(unsigned int i) {
    return m_path[i];
}

unsigned int Vehicle::path_length() const {
    return m_path.size();
}

unsigned int Vehicle::speed() const {
    return m_speed;
}

unsigned int Vehicle::width() const {
    return m_width;
}

complex<float> Vehicle::position() {
    if (roundabout())
        return *(roundabout());

    return *(lane()->from()) + (complex<float>)m_length_covered * lane()->u() + (complex<float>)(m_width/2) * lane()->v();
}

//  Find (or not) the path to the given destination
void Vehicle::set_destination(Roundabout* destination) {
    if (!destination || !m_location || m_location->map() != destination->map())     return;
    // EXPERIMENTAL : leaving nodes only
    //srand(time(NULL));
    //destination = map->roundabouts[rand() % map->total_roundabouts()];
    

    //   Compute the path
    //   Each vehicle needs its own gps instance to avoid collisions and clean pathfinding
    Roundabout* origin;
    if (lane())     origin = lane()->from();
    else            origin = (dynamic_cast<Slot*>(m_location))->roundabout();

    m_path = m_gps.find_path(origin, destination);

    /*if (!(path.size()))
        destination = NULL;*/
}

//  Allocate the vehicle to the given location. The concept of location makes it possible to use this code for either a lane or a roundabout.
//      new_location    (road or lane or Roundabout)  :   lane or roundabout that will host, if possible, the vehicle

/*  Kills the vehicle, which simply disappears.
    void Vehicle::die(this)

    if location.vehicles:
    if this in location.vehicles:
    dead = True 
    location.vehicles.remove(this)
else:
raise Except("WARNING (in vehicle.die()) : a vehicle was not in its place !")*/

//  Expresses the vehicles' wishes :P
/*Road* Vehicle::next_way(bool read_only) {
    //   End of path
    if (!(path.size()))
        return NULL;
    
    Road* result = path[0];

    if (!read_only)
        path.erase(path.begin());
    
    return result;
}*/

//  Returns the position of the obstacle ahead of the vehicle, (obstacle, obstacle_is_light)
float Vehicle::next_obstacle() {
    if (!lane())
        return 0;
    
    //   The vehicle is the first of the queue : the next obstacle is the light
    if (lane()->vehicle(0) == this || !m_previous_vehicle) {
        //obstacle_is_light = True
        
        //   Green light
        //if (next_slot()->opened())
        //    return (lane()->length() + HEADWAY);
        return lane()->length();
    }

    //   Otherwise : the next obstacle is the previous vehicle
    //obstacle_is_light = False
    return m_previous_vehicle->length_covered() - m_previous_vehicle->length()/2;
}


                       

//  Changes, if needed, the waiting attitude of a vehicle
void Vehicle::set_waiting_state(bool new_state) {
    //   There is no change : do nothing
    if (new_state == m_is_waiting)
        return;

    m_is_waiting = new_state;
    
    //   Measure waiting delay
    if (new_state)
        m_start_waiting_delay = clock();
    else
        m_total_waiting_delay += clock() - m_start_waiting_delay;
}


/*Vehicle* Vehicle::previous_vehicle(this) {
    if (lane() == NULL || lane()->vehicle(0) == this)
        return NULL;
    
    if (previous_vehicle != NULL)
        return previous_vehicle;
    
    vector<int>::iterator i = find(lane()->vehicle().begin(), lane()->vehicle().end(), this) - 1;
    previous_vehicle = *i;

    return previous_vehicle;
}*/

//  Returns the lane where the vehicle is, if it is in a lane.
//  This property is provided for convenience.
Lane* Vehicle::lane() {
    if (m_location && m_location->get_class() == LANE)
        return dynamic_cast<Lane*>(m_location);

    return 0;
}


//Returns the road where the vehicle is, if it is in a road.
//This property is provided for convenience.
Road* Vehicle::road() {
    if (lane()) {
        Road* result = lane()->road();
        return result;
    }

    return NULL;
}

//  Returns the slot where the wehicle is, if it is in a roundabout.
//  This property is provided for convenience.
Slot* Vehicle::slot() {
    if (m_location && m_location->get_class() == SLOT)
        return dynamic_cast<Slot*>(m_location);

    return 0;
}

//  Returns the roundabout where the vehicle is, if it is in a roundabout.
//  This property is provided for convenience.
Roundabout* Vehicle::roundabout() {
    if (slot()) {
        Roundabout* result = slot()->roundabout();
        return result;
    }

    return 0;
}

//  Returns the tracks where is the vehicle.
//  This function is provided for convenience.
Map* Vehicle::map() {
    return m_location->map();
}

    
bool Vehicle::join(Location* location) {
    if (location == m_location)     return true;
    if (!location)                  {m_location->release(this); m_location = 0; m_previous_vehicle = 0; return true;}
    if (!location->is_free())       return false;

    if (m_location)     m_location->release(this);
    m_location = location;
    m_previous_vehicle = location->last_vehicle();
    m_location->host(this);

    m_acceleration      = m_force/m_mass;
    m_length_covered    = 0;
    m_speed             = 5;
    return true;
}


//  Moves the vehicle, THEN manages its speed, acceleration.
void Vehicle::update(float delta_t) {
    if (slot())     update_on_slot(delta_t);
    else            update_on_lane(delta_t);
}


void Vehicle::update_on_slot(float delta_t) {
    if (!m_path.size())                     {join(0); return;}
    if (slot()->lane()->to() != m_path[0])  return;
    if (!join(slot()->lane()))              return;

    m_path.erase(m_path.begin());
    update_on_lane(delta_t);
}

void Vehicle::update_on_lane(float delta_t) {
    //   Update the acceleration given the context
    float obstacle = next_obstacle();
    float sight_distance = pow(m_speed, 2) / (2*m_force/m_mass);
    float acceleration;

    //   No obstacle at sight : « 1 trait danger, 2 traits sécurité : je fonce ! »
    if (m_length_covered + m_length/2 + sight_distance < obstacle)      acceleration = m_force/m_mass;
    
    //   Visible obstacle
    else {
        //   Are we waiting in a traffic jam ?
        if (m_previous_vehicle)                                                     set_waiting_state(m_previous_vehicle->is_waiting());
        else if (dynamic_cast<Lane*>(m_location)->semaphore().state() == GREEN)     set_waiting_state(false);
        else                                                                        set_waiting_state(true);
        
        //   Start deceleration
        float delta_speed     = - m_speed;
        float delta_position  = obstacle - m_length_covered - m_length/2 - HEADWAY;
        
        if (m_previous_vehicle)     delta_speed += m_previous_vehicle->speed();
                
        acceleration = 0;
        if (delta_speed)    acceleration = m_force/m_mass * delta_speed/abs(delta_speed);
    }

    //   Update the position and speed given the speed and acceleration
    m_length_covered    = min(m_length_covered + m_speed*delta_t, obstacle - m_length/2 - HEADWAY);
    m_speed             = max((float)min(m_speed + acceleration*delta_t, (float)(lane()->max_speed())), (float)5);

    //   Arrival at a roundabout
    if (m_length_covered >= lane()->length() - m_length/2 - HEADWAY) {
        //   Green light
        if (lane()->semaphore().state() == GREEN && lane()->slot(TO)->is_free()) {
            set_waiting_state(false);
            join(lane()->slot(TO));
        }

        //   The slot isn't free
        else    set_waiting_state(true);
    }
}
 
