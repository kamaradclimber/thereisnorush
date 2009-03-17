#ifndef SLOT
    #define SLOT

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

        Roundabout* get_roundabout()    const;
        Road*       get_road()          const;
        Vehicle*    get_vehicle()       const;

        void        connect_to(const Road*);

        Slot&       operator=(const Slot&);
    };
#endif

