#ifndef VEHICLE
    #define VEHICLE

    #include <complex>
    #include <ctime>
    #include <QColor>
    #include <vector>

    #include "gps.hpp"

    #define HEADWAY 5
    
    class Lane;
    class Location;
    class Map;
    class Road;
    class Roundabout;
    class Slot;

    enum VehicleModel   {CAR, SPEED_CAR, TRUCK};

    //  Those which will crowd our city >_<
    class Vehicle {
        bool                        m_is_waiting;
        clock_t 
            m_start_waiting_delay,
            m_total_waiting_delay;
        float
            m_length_covered,
            m_mass;
        GPS                         m_gps;
        QColor                      m_color;
        unsigned int
            m_acceleration,
            m_force,
            m_length,
            m_speed,
            m_width;
        std::vector<Roundabout*>    m_path;
        Vehicle*                    m_previous_vehicle;
        Location*                   m_location;
        
        public:
        static Vehicle              DEFAULT_CAR;
        static Vehicle              DEFAULT_SPEED_CAR;
        static Vehicle              DEFAULT_TRUCK;
        
        Vehicle(VehicleModel model = CAR);
        ~Vehicle();

        QColor              color()                 const;
        bool                is_waiting()            const;
        Lane*               lane();
        unsigned int        length()                const;
        unsigned int        length_covered()        const;
        Roundabout*         path(unsigned int);
        unsigned int        path_length()           const;
        unsigned int        speed()                 const;
        unsigned int        width()                 const;

        float               next_obstacle();
        std::complex<float> position();
        Road*               road();
        Slot*               slot();
        Roundabout*         roundabout();
        Map*                map();
        
        void                set_waiting_state(bool);
        //void              set_location(void*);
        void                set_destination(Roundabout*);

        bool                join(Location*);
        void                update(float delta_t);
        void                update_on_slot(float delta_t);
        void                update_on_lane(float delta_t);
    };
#endif
    
