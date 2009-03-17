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
            direction;  // Index of the destination in Road::extremity
        
        public:
        static Lane DEFAULT;
        
        Lane();
        Lane(Road*, bool);
        ~Lane();

        unsigned short      total_waiting_vehicles()    const;
        bool                is_free()                   const;
        Roundabout*         origin()                    const;
        Roundabout*         destination()               const;
        float               length()                    const;
        std::vector<Vector> reference()                 const;
        Map*                map()                       const;

        void                update();
    };

#endif
