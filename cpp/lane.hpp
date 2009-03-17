#ifndef LANE
    #define LANE
    
    #include <vector>

    #include "map.hpp"
    #include "road.hpp"
    #include "vector.hpp"
    
    class Vehicle;
    
    //  A lane is a one-way piece of road.
    class Lane
    {
        Road*                   road;
        std::vector<Vehicle*>   vehicles;
        unsigned short
            width,
            direction;
        
        public:
        Lane(Initialization mode = DEFAULT);
        Lane(Road*, bool);
        ~Lane();

        unsigned short      total_waiting_vehicles()    const;
        bool                free()                      const;
        Roundabout*         destination()               const;
        float               length()                    const;
        std::vector<Vector> reference()                 const;
        Map*                map()                       const;

        void                update();
    };

    //  Default features
    const Lane DEFAULT_LANE(EMPTY);
        DEFAULT_LANE.set_width(5);
#endif

