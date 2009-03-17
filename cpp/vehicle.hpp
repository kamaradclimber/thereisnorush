#ifndef VEHICLE
    #define VEHICLE

    #include <vector>

    #include "constants.hpp"
    
    class Road;

    //  Those which will crowd our city >_< .
    class Vehicle
    {
        unsigned short
            force,
            headway,
            length,
            mass,
            speed,
            width;
        QColor              color;
        std::vector<Road*>  path;
        bool                waiting;

        public:
        Vehicle(Initialization mode = DEFAULT);
        ~Vehicle();
    };
    
    //   Standard car
    const Vehicle DEFAULT_CAR(EMPTY);
        DEFAULT_CAR.set_length(5);
        DEFAULT_CAR.set_width(4);
        DEFAULT_CAR.set_headway(DEFAULT_CAR.length());
        DEFAULT_CAR.set_speed(0);
        DEFAULT_CAR.set_force(10);
        DEFAULT_CAR.set_mass(1);
        DEFAULT_CAR.set_color(QColor(Qt::white));

    //   Speed car
    const Vehicle DEFAULT_SPEED_CAR(EMPTY);
        DEFAULT_SPEED_CAR.set_length(5);
        DEFAULT_SPEED_CAR.set_width(4);
        DEFAULT_SPEED_CAR.set_headway(DEFAULT_CAR.length());
        DEFAULT_SPEED_CAR.set_speed(0);
        DEFAULT_SPEED_CAR.set_force(30);
        DEFAULT_SPEED_CAR.set_mass(1/1.5);
        DEFAULT_SPEED_CAR.set_color(QColor(Qt::red));

    //   Truck
    const Vehicle DEFAULT_TRUCK(EMPTY);
        DEFAULT_TRUCK.set_color(QColor(Qt::lightblue));
        DEFAULT_TRUCK.set_force(50);
        DEFAULT_TRUCK.set_headway(DEFAULT_CAR.length());
        DEFAULT_TRUCK.set_length(5);
        DEFAULT_TRUCK.set_mass(5);
        DEFAULT_TRUCK.set_speed(0);
        DEFAULT_TRUCK.set_width(4);
#endif
    
