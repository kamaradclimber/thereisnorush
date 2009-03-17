#ifndef MAP
    #define MAP

    #include <QString>
    #include <string>
    #include <vector>

    class Road;
    class Roundabout;

    //  Our city model : a mathematical graph made of roundabouts, linked to each other by roads.
    class Map
    {
        std::vector<Roundabout*>    roundabouts;
        std::vector<Road*>          roads;
        
        public:
        Map();
        ~Map();

        void add_vehicle();
        void load(std::string, std::string picture = "");
        void parse(QString);
        void load_demo_map();
    };
#endif

