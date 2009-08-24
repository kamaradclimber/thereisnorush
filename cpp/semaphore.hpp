#ifndef SEMAPHORE
    #define SEMAPHORE

    #include <ctime>

    enum SemaphoreState {RED, YELLOW, GREEN};
    
    class Semaphore {
        SemaphoreState  m_state;
        clock_t         m_last_update;

        public:
        Semaphore();

        SemaphoreState state()          const;
        clock_t         last_update()   const;

        void set(SemaphoreState);
        void open();
        void touch();
    };
#endif

