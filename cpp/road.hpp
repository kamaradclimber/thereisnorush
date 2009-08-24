#ifndef __ROAD__
    #define __ROAD__
    
    //#include <complex>
    #include <QColor>
    #include <vector>

    class Lane;
    class Map;
    class Road;
    class Roundabout;
    class Vehicle;

    class Road {
        QColor                  m_color;
        Roundabout*             m_extremities[2];
        unsigned short          m_max_speed;
        std::vector<Lane*>      m_lanes[2];
        std::vector<Vehicle*>   m_vehicles;

        public:
        static Road DEFAULT;


        Road();
        Road(Roundabout*, Roundabout*, unsigned short total_lanes1 = 1, unsigned short total_lanes2 = 1);
        ~Road();

        QColor          color()                                 const;
        unsigned short  max_speed()                             const;
        unsigned short  total_lanes_to(unsigned short)          const;
        Roundabout*     extremity(unsigned short);
        Lane*           lane(unsigned short, unsigned short);
        unsigned short  lanes_count()                           const;
        unsigned short  lanes_count(unsigned short)             const;
        Map*            map();
        float           weight()                                const;

        unsigned short  length()                                const;
        unsigned short  vehicles_count()                        const;
        unsigned short  waiting_vehicles_count()                const;

        void            set_color(QColor);
        void            set_max_speed(unsigned short);
    
        
        void            update(float);
    };
#endif

