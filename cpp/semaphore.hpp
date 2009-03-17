#ifndef SEMAPHORE
    #define SEMAPHORE
    
    class Semaphore
    {
        bool
            red,
            yellow,
            green;
        unsigned float last_update;

        public:
        void open();
        void touch();
    };
#endif

