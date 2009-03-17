#ifndef __ROUNDABOUT__
    #define __ROUNDABOUT__
    
    #include <complex>
    #include <vector>
    
    #include "slot.hpp"
    
    class Map;
    class Road;

    //  Crossroads of our city ; may host several roads.
    class Roundabout
    {
        Map*                map;
        std::complex<float> position;
        std::vector<Slot*>  slots;
        bool                spawning;
        float
            f_cost, // G-cost + H-cost
            g_cost, // Minimal real cost found so far
            h_cost, // Remaining heuristic cost
            last_spawn,
            last_shift,
            local_load;
        unsigned short
            height,
            max_slots,
            radius,
            rotation_speed,
            spawn_delay,
            width;
        QColor              color;
        Roundabout*         nearest_parent;
        
        public:
        Roundabout();
        Roundabout(Map*, unsigned short, unsigned short);
        ~Roundabout();
        
        std::complex<float> get_position()              const;
        float               get_local_load()            const;
        float               get_f_cost()                const;
        float               get_g_cost()                const;
        float               get_h_cost()                const;
        Roundabout*         get_nearest_parent()        const;
        Slot*               slot(unsigned short)        const;
        unsigned short      total_slots()               const;
        
        float               global_load()               const;
        bool                full()                      const;
        unsigned short      total_waiting_vehicles()    const;
        
        void                set_f_cost(float);
        void                set_g_cost(float);
        void                set_h_cost(float);
        void                set_nearest_parent(Roundabout*);
        
        void                host(const Road*);
        void                update_semaphores();
        void                update();
    };
    
    /*  TO INCLUDE IN A STATIC MEMBER
    const Roundabout DEFAULT_ROUNDABOUT(EMPTY);
        DEFAULT_ROUNDABOUT.set_color(QColor(Qt::red));
        DEFAULT_ROUNDABOUT.set_height(3);
        DEFAULT_ROUNDABOUT.set_max_slots(5);
        DEFAULT_ROUNDABOUT.set_radius(10);
        DEFAULT_ROUNDABOUT.set_rotation_speed(10);
        DEFAULT_ROUNDABOUT.set_width(3);

    float ROUNDABOUT_ROTATION_RATE = 0.5;*/
#endif

