#include <fstream>

#include "constants.hpp"
#include "lib.hpp"
#include "map.hpp"
    
using namespace std;

//  Constructor method : creates a track given the roundabouts and roads, if any.
//      new_roundabouts   (list)  :   a list of the roundabouts
//      new_roads   (list)  :   a list of the roads
Map::Map() : roundabouts(), roads()//, picture(NULL)
{
}

//  Adds a vehicle on the track
void Map::add_vehicle(unsigned short road_number)
{
    Vehicle new_car(roads[road_number]);
}


//  Loads a track from a textfile, checks its validity, parses it
//  and loads it in the simulation.
//      file_name    (string)    :   the name of the file to load.
void Map::load(string file_name, string picture)
{
    ifstream file(file_name, ios::in);
     
    if (!file)
    {
        cerr << "Error";
        return void;        
    }

    //        if len(file_picture) > 0:
    //            from pygame import image 
    //            try:
    //                track.picture = image.load(file_picture)
    //            except IOError:
    //                raise Exception("%s cannot be loaded (current directory is : %s)" % (file_picture, getcwd()))                 

    QString line;
    while(getline(file, line))
    {
        QString line = line.trimmed();

        if (line.startsWith('#') || line == "")
        {
            continue;
        }
        
        parse(line);
    }
    
    file.close();
}

//  Parses a line in a track description file.
//      line    (string)    :   the line of text to be parsed
void Map::parse(QString line)
{
    //parse_errors = []
    elements = line.replace(",", " ").split(" ");
    
    if (elements[0] == ROUNDABOUT)
    {
        unsigned short spawning = elements[3].toUShort();
        Roundabout* new_roundabout = new Roundabout(this, elements[1].toUShort(), elements[2].toUShort());
            new_roundabout->set_spawning(spawning);

        roundabouts.push_back(new_roundabout);
    }
    else if (elements[0] == ROAD)
    {
        Road* new_road = new Road(roundabouts[elements[1].toUShort()], roundabouts[elements[2].toUShort()]);
        roads.push_back(new_road);
    }
    else
    {
        //cerr << "ERROR : unknown element type '" + elements[0] + "' !";
    }
}

void Map::load_demo_map()
{
    // Temporary testing zone
    load("demo_track.txt", "demo_track.png");
}
