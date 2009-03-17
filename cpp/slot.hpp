#ifndef __SLOT__
    #define __SLOT__

    class Road;
    class Roundabout;
    class Vehicle;

    class Slot
    {
        Roundabout* roundabout;
        Road*       road;
        Vehicle*    vehicle;

        public:
        Slot();
        Slot(const Slot&);
        ~Slot();

        Roundabout* get_roundabout()            const;
        Roundabout* other_side()                const;
        Road*       get_road()                  const;
        Vehicle*    get_vehicle()               const;
        bool        is_connected()              const;

        void        connect_to(const Road*);

        Slot&       operator=(const Slot&);
    };
#endif

