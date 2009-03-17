#ifndef ROAD
    #define ROAD
    
    #include <QColor>
    #include <vector>
    
    #include "constants.hpp"
    
    class Lane;
    class Map;
    class Roundabout;
    class Vector;

    //  A road acts as a container for several lanes and connects two roundabouts
    class Road
    {
        std::vector<Roundabout*>            extremities;
        std::vector< std::vector<Lane*> >   lanes;
        unsigned short                      max_speed;
        QColor                              color;

        public:
        Road();
        Road(const Roundabout*, const Roundabout*);
        ~Road();
        
        unsigned short      get_max_speed()                             const;

        Roundabout*         other_extremity(const Roundabout*)          const;
        bool                can_lead_to(const Roundabout*)              const;
        Lane*               get_lane_to(const Roundabout*)              const;
        std::vector<Vector> reference(const Roundabout*)                const;
        bool                free(const Roundabout*)                     const;
        unsigned short      total_waiting_vehicles(const Roundabout*)   const;
        float               width()                                     const;
        unsigned short      length()                                    const;
        bool                is_one_way()                                const;
        unsigned short      total_vehicles()                            const;
        float               weight()                                    const;
        Map*                map()                                       const;
        
        void                set_color(QColor);
        void                set_max_speed(unsigned short);

        void                update();
        void                open(const Roundabout*, Extremity);

        static Road         DEFAULT;
    };
#endif

