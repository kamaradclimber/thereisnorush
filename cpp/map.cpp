#include <cstdlib>
#include <ctime>
#include <fstream>
#include <iostream>

#include "map.hpp"
#include "road.hpp"
#include "roundabout.hpp"
#include "slot.hpp"
    
using namespace std;

//  Constructor method : creates a track given the roundabouts and roads, if any.
//      new_roundabouts   (list)  :   a list of the roundabouts
//      new_roads   (list)  :   a list of the roads
Map::Map() : m_roads(), m_roundabouts()//, picture(NULL)
{}

Map::~Map() {
    unsigned short i(0);

    while (i < m_roads.size()) {
        delete m_roads[i];
        i++;
    }

    i = 0;
    while (i < m_roundabouts.size()) {
        delete m_roundabouts[i];
        i++;
    }
}

//  Accessors
Roundabout* Map::random_roundabout() {
    if (!m_roundabouts.size())      return 0;

    srand(time(0));

    return m_roundabouts[rand() % m_roundabouts.size()];
}

Road* Map::road(unsigned int i) {
    return m_roads[i];
}

Roundabout* Map::roundabout(unsigned int i) {
    return m_roundabouts[i];
}

unsigned int Map::roads_count() const {
    return m_roads.size();
}
 
unsigned int Map::roundabouts_count() const {
    return m_roundabouts.size();
}


//  Adds a vehicle on the track
/*void Map::add_vehicle(unsigned short roundabout_number) {
    Slot* slot = m_roundabouts[roundabout_number]->free_slot();
    
    Vehicle* new_car = new Vehicle;
    new_car->join(slot);
}*/


//  Loads a track from a textfile, checks its validity, parses it
//  and loads it in the simulation.
//      file_name    (string)    :   the name of the file to load.
void Map::load(string file_name, string picture) {
    ifstream file(file_name.c_str(), ios::in);
     
    if (!file) {
        cerr << "[Error (Map::load)] Cannot open map file !" << endl;
        return;
    }

    //        if len(file_picture) > 0:
    //            from pygame import image 
    //            try:
    //                track.picture = image.load(file_picture)
    //            except IOError:
    //                raise Exception("%s cannot be loaded (current directory is : %s)" % (file_picture, getcwd()))                 


    string line;
    while (getline(file, line)) {
        QString new_line = ((QString)(line.c_str())).trimmed();

        if (new_line.startsWith('#') || new_line == "")     continue;
        
        parse(new_line);
    }
    
    file.close();
}

//  Parses a line in a track description file.
//      line    (string)    :   the line of text to be parsed
void Map::parse(QString line) {
    //parse_errors = []
    QStringList elements = line.replace(",", " ").split(" ");
    
    if (elements[0] == ROUNDABOUT) {
        Roundabout* new_roundabout = new Roundabout(this, elements[1].toUShort(), elements[2].toUShort());
        if (elements[3].toUShort())      new_roundabout->set_spawning(true);

        m_roundabouts.push_back(new_roundabout);
    }
    else if (elements[0] == ROAD) {
        Road* new_road = new Road(m_roundabouts[elements[1].toUShort()], m_roundabouts[elements[2].toUShort()]);
        m_roads.push_back(new_road);
    }
    else
        cerr << "[ERROR] Unknown element type '" << elements[0].toStdString() << "' !";
}

void Map::load_demo_map() {
    // Temporary testing zone
    load("demo_map", "demo_track.png");
}
