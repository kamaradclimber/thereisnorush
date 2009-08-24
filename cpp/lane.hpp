#ifndef __LANE__
    #define __LANE__
    
    #include <complex>
    #include <vector>

    #include "location.hpp"
    #include "semaphore.hpp"
    
    class Map;
    class Road;
    class Roundabout;
    class Slot;
    class Vehicle;

    enum Extremity      {FROM, TO};
    
    //  A lane is a one-way piece of road.
    class Lane : public Location {
        std::complex<float>     m_reference[2];
        Road*                   m_road;
        Semaphore               m_semaphore;
        Slot*                   m_slots[2];
        unsigned short
            //m_width,
            m_direction;  // Index of the destination in Road::extremity
        std::vector<Vehicle*>   m_vehicles;
        
        public:
        static Lane DEFAULT;
        
        Lane();
        Lane(Road*, bool);
        ~Lane();

        Roundabout*             from()                      const;
        Class                   get_class()                 const;
        //std::complex<float>*    reference()                 const;
        Road*                   road()                      const;
        Roundabout*             to()                        const;
        Semaphore               semaphore()                 const;
        std::complex<float>     u()                         const;
        std::complex<float>     v()                         const;
        //unsigned short          width()                     const;
        

        bool                    is_free()                   const;
        Vehicle*                last_vehicle()              const;
        float                   length()                    const;
        float                   load()                      const;
        Map*                    map()                       const;
        //Semaphore*              semaphore();
        Slot*                   slot(unsigned short)        const;
        Vehicle*                vehicle(unsigned int)       const;
        unsigned short          vehicles_count()            const;

        unsigned int            max_speed()                 const;
        unsigned short          waiting_vehicles_count()    const;

        void                    close();
        void                    host(Vehicle*);
        void                    open();
        void                    release(Vehicle*);
        void                    update(float);
    };

#endif
