#ifndef __LOCATION__
    #define __LOCATION__

    enum Class {LANE, SLOT};

    class Map;
    class Semaphore;
    class Vehicle;

    class Location {
        public:
        //Location();
        //~Location();

        virtual bool        is_free()       const = 0;
        virtual Vehicle*    last_vehicle()  const {return 0;}
        virtual Map*        map()           const = 0;
        //virtual Semaphore   semaphore() = 0;
        virtual Class       get_class()     const = 0;
        
        virtual void        host(Vehicle*) = 0;
        virtual void        release(Vehicle*) = 0;
    };
#endif
