#ifndef CONSTANTS
    #define CONSTANTS
    
    #include <string>
    #include <vector>

    //   Revision information
    std::string TITLE = "There Is No Rush";

    enum Initialization
    {
        EMPTY,
        DEFAULT
    };
    
    //   Track
    //TRACK_OFFSET_X = 32
    //TRACK_OFFSET_Y = 32
    //TRACK_SCALE    = 3.5


    //   Pathfinders list
    enum Pathfinder
    {
       A_STAR,
       DIJKSTRA
    };

    //   Rules
    unsigned short
        WAITING_CARS_LIMIT = 8,
        WAITING_TIME_LIMIT = 10;

    //   Traffic lights
    enum Extremity
    {
        ENTRANCE,
        EXIT
    };

    unsigned short TF_RADIUS = 3;

    //   Resolution
    unsigned short
        SCENE_WIDTH     = 800,
        SCENE_HEIGHT    = 600,
        PANEL_WIDTH     = 200,
        PANEL_HEIGHT    = 500;

    //   Histograms
    //HISTOGRAM_WIDTH  = 100
    //HISTOGRAM_HEIGHT = 50
    //HISTOGRAM_SPAN   = 200
    //HISTOGRAM_COLOR  = 255, 128, 0, 128

    //   Others
    //DISPLAY_DENSITY = False
    float SPAWN_DELAY = 2.0;

    //   Not really constants... but cannot be placed in lib.py
    //simulation_speed    = 1.0
    //time_static_counter = 0.0
    //time_last_counter   = 0.0
#endif

