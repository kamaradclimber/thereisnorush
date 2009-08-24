#ifndef __ROUNDABOUT__
    #define __ROUNDABOUT__
    
    #include <complex>
    #include <QColor>
    #include <vector>
    
    #include "slot.hpp"
    
    class Map;
    class Road;

    //  Crossroads of our city ; may host several roads.
    class Roundabout : public std::complex<float> {
        bool                m_is_spawning;
        float
            m_g_cost,     // Minimal real cost found so far
            m_h_cost,     // Remaining heuristic cost
            m_last_spawn,
            m_last_shift,
            m_local_load,
            m_shift_delay,
            m_spawn_delay;
        Map*                m_map;
        QColor              m_color;
        Roundabout*         m_destination;
        Roundabout*         m_nearest_parent;
        //unsigned short      m_height;
        std::vector<Road*>  m_roads;
        std::vector<Slot*>  m_slots;     // And not "slots" which is reserved by Qt ! (3 months to find out this bug...)
        
        public:
        static Roundabout DEFAULT;
        
        Roundabout();
        Roundabout(Map*, unsigned short, unsigned short);
        ~Roundabout();
        
        //std::complex<float> _position()              const;
        QColor              color()                     const;
        float               f_cost()                    const;
        float               g_cost()                    const;
        float               h_cost()                    const;
        bool                is_spawning()               const;
        float               local_load()                const;
        Map*                map();
        Roundabout*         nearest_parent();
        float               spawn_delay()               const;
        float               shift_delay()               const;
        Slot*               slot(unsigned short);
        unsigned short      slots_count()               const;

        Slot*               free_slot();
        float               global_load()               const;
        bool                is_full()                   const;
        unsigned short      vehicles_count()            const;
        unsigned short      waiting_vehicles_count()    const;
        
        Slot*               book_slot(Lane*);
        //void                set_f_cost(float);
        void                set_g_cost(float);
        void                set_h_cost(float);
        void                set_destination(Roundabout*);
        void                set_nearest_parent(Roundabout*);
        void                set_spawn_delay(float);
        void                set_spawning(bool);

        //void                host(const Road*);
        void                connect_to(Roundabout*, unsigned short, unsigned short);
        //void                update_semaphores();
        void                update(float);
        void                update_semaphores();
    };
#endif
