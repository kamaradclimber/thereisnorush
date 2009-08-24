#ifndef __SLOT__
    #define __SLOT__

    #include "location.hpp"
    #include "semaphore.hpp"

    class Lane;
    class Map;
    class Roundabout;
    class Vehicle;

    class Slot : public Location {
        Lane*       m_lane;
        Roundabout* m_roundabout;
        Semaphore   m_semaphore;
        Vehicle*    m_vehicle;

        public:
        Slot();
        Slot(Roundabout*, Lane*);
        //Slot(const Slot&);
        ~Slot();

        Class               get_class()             const;
        Lane*               lane()                  const;
        Roundabout*         roundabout()            const;
        Semaphore*          semaphore();
        //std::vector<Lane*>  lanes()                     const;
        Vehicle*            vehicle()               const;

        bool                is_free()               const;
        Map*                map()                   const;
        unsigned short      waiting_vehicles_count()    const;
        
        //Roundabout*       other_side()                const;
        //bool              is_connected()              const;

        //void              connect_to(const Road*);
        void                host(Vehicle*);
        void                release(Vehicle* vehicle = 0);

        //Slot&             operator=(const Slot&);
    };
#endif

