#ifndef __GPS__
    #define __GPS__

    #include <vector>

    class Roundabout;    
    
    enum Pathfinder {A_STAR, DIJKSTRA};

    class GPS {
        Pathfinder algorithm;
        
        public:
        GPS();
        ~GPS();

        float                       heuristic_weight(const Roundabout*, const Roundabout*)  const;
        std::vector<Roundabout*>    find_path(Roundabout*, Roundabout*)                     const;
    };
#endif
