#ifndef __MAP__
    #define __MAP__

    #define ROUNDABOUT  "roundabout"
    #define ROAD        "road"

    #include <QString>
    #include <string>
    #include <vector>

    #include "vehicle.hpp"

    class Road;
    class Roundabout;

    //  Our city model : a mathematical graph made of roundabouts, linked to each other by roads.
    class Map {
        std::vector<Road*>          m_roads;
        std::vector<Roundabout*>    m_roundabouts;
        
        public:
        Map();
        ~Map();

        Roundabout*     random_roundabout();
        Road*           road(unsigned int);
        Roundabout*     roundabout(unsigned int);
        unsigned int    roads_count()               const;
        unsigned int    roundabouts_count()         const;

        void            add_vehicle(unsigned short);
        void            load(std::string, std::string picture = "");
        void            parse(QString);
        void            load_demo_map();
    };
#endif

