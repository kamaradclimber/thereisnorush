#include <complex>
#include <iostream>

#include "lane.hpp"
#include "map.hpp"
#include "road.hpp"
#include "roundabout.hpp"
#include "scene.hpp"
#include "window.hpp"

using namespace std;


Scene::Scene(MainWindow* new_window) : 
        QWidget(new_window),
        m_window(new_window),
        m_painter(0),
        m_map() {
    m_map.load_demo_map();

    setSizePolicy(QSizePolicy(QSizePolicy::Expanding, QSizePolicy::Expanding));
    setMinimumSize(SCENE_WIDTH, SCENE_HEIGHT);
}

Scene::~Scene() {}

Map* Scene::map() {
    return &m_map;
}

//  /!\ Qt specific (please don't rename) : is triggered each time the update() method is called.
//  Specifies how the control should draw it
void Scene::paintEvent(QPaintEvent* event) {
    m_painter = new QPainter(this);

    //  Set antialiasing
    m_painter->setRenderHint(QPainter::Antialiasing, m_window->antialiasing());

    //  Draw background color and scene
    m_painter->fillRect(QRectF(QPointF(0, 0), QPointF(width(), height())), QColor(Qt::black));
    draw();

    m_painter->end();
}

//  Draws the complete scene on the screen.
void Scene::draw() {
    //   Draw the roads and roundabouts
    unsigned short i(0);

    while (i < m_map.roads_count()) {
        draw(m_map.road(i));
        i++;
    }

    i = 0;
    while (i < m_map.roundabouts_count()) {
        draw(m_map.roundabout(i));
        i++;
    }
    
    //   Manage selections
    //draw_selected_path();
}

//  Draws a given road on the screen and all the vehicles on it.
//  road (Road) : the aforementioned road.
void Scene::draw(Road* road) {
    Roundabout* start   = road->extremity(0);
    Roundabout* end     = road->extremity(1);
    
    //   Draw traffic lights (or not)
    /*if (m_window->entrance_lights->isChecked())
        draw(road, ENTRANCE);
    
    if (m_window->exit_lights->isChecked())
        draw(road, EXIT);*/

    //   Draw a line to represent the road
    m_painter->setPen(Road::DEFAULT.color());
    m_painter->drawLine(real(*start), imag(*start), real(*end), imag(*end));

    //   Draw lanes individually
    unsigned short i(0), j(0);
    while (j < 2) {
        while (i < road->lanes_count(j)) {
            draw(road->lane(j, i));
            i++;
        }

        i = 0;
        j++;
    }
}

//  When a vehicle is selected, draw its path
void Scene::draw_selected_path() {
    Vehicle* vehicle = m_window->selected_vehicle();

    if (!vehicle)           return;
    if (!vehicle->lane())   return;

    complex<float>* start = &(vehicle->position() - (complex<float>)(vehicle->width()/2) * (vehicle->lane()->v()));
    complex<float>* end   = vehicle->lane()->to();

    m_painter->setPen(QColor(Qt::blue));
    m_painter->drawLine(real(*start), imag(*start), real(*end), imag(*end));

    unsigned short i(0);
    while (i < vehicle->path_length() - 1) {
        start = vehicle->path(i);
        end   = vehicle->path(i+1);

        m_painter->drawLine(real(*start), imag(*start), real(*end), imag(*end));
        
        i++;
    }
}

//  Draws a lane and all the vehicles on it.
void Scene::draw(Lane* lane) {
    unsigned short i(0);
    while (i < lane->vehicles_count()) {
        draw(lane->vehicle(i));
        i++;
    }

    //  Draw semaphores, if supposed
    if (m_window->display_semaphores())     draw_semaphore(lane);
}

//  Draws a given vehicle on the screen.
//  vehicle (Car) : the aforementioned vehicle.
void Scene::draw(Vehicle* vehicle) {
    if (!vehicle->lane())               return;
    if (!m_window->display_vehicles())  return;

    //   Get them once
    unsigned short
        r_width     = vehicle->width(),
        r_length    = vehicle->length();
    complex<float>
        u           = vehicle->lane()->u(),
        v           = vehicle->lane()->v();

    //   Vehicles are rectangles whose sides are parallel and perpendicular to the road
    complex<float> points[4];
    points[0] = vehicle->position() - (complex<float>)(r_length/2) * u - (complex<float>)(r_width/2) * v;
    points[1] = vehicle->position() + (complex<float>)(r_length/2) * u - (complex<float>)(r_width/2) * v;
    points[2] = vehicle->position() + (complex<float>)(r_length/2) * u + (complex<float>)(r_width/2) * v;
    points[3] = vehicle->position() - (complex<float>)(r_length/2) * u + (complex<float>)(r_width/2) * v;

    
    QPointF polygon[4];
    unsigned short i(0);
    while (i < 4) {
        polygon[i] = QPointF(real(points[i]), imag(points[i]));
        i++;
    }
    
    //   Draw the vehicle
    m_painter->setBrush(vehicle->color());
    m_painter->setPen(QColor(Qt::black));
    m_painter->drawPolygon(polygon, 4);

    //   Selected vehicle : draw selection circle
    if (m_window->selected_vehicle() == vehicle) {
        m_painter->setPen(Roundabout::DEFAULT.color());
        m_painter->setBrush(QColor(Qt::transparent));
        m_painter->drawEllipse(real(vehicle->position()) - vehicle->length(), imag(vehicle->position()) - vehicle->length(), 2*vehicle->length(), 2*vehicle->length());
    }
}

//  Draws a given roundabout on the screen.
//  roundabout (Roundabout) : the aforementioned roundabout.
void Scene::draw(Roundabout* roundabout) {
    // TODO :
    //       · (DN1) draw the vehicles on the roundabout

    //   Draw a red circle to represent a roundabout
    //if (m_map.picture == NULL) {
        m_painter->setBrush(QColor(Qt::red));
        m_painter->setPen(QColor(Qt::transparent));
        m_painter->drawEllipse(real(*roundabout) - 2, imag(*roundabout) - 2, 4, 4);

        //return void();
    //}
    

    //   Selected roudabout : draw selection circle
    if (m_window->selected_roundabout() == roundabout) {
        m_painter->setPen(Roundabout::DEFAULT.color());
        m_painter->setBrush(QColor(Qt::transparent));
        m_painter->drawEllipse(real(*roundabout) - 8, imag(*roundabout) - 8, 16, 16);

    }
    
    if (roundabout->vehicles_count()) {
        // There are vehicles on the roundabout, we may want to draw them
        // albeit we can't use draw_vehicle here...

        //TEMPORARY : the number of vehicles on the roundabout is written
        complex<float> position(real(*roundabout) + 10, imag(*roundabout) + 10);
        m_painter->setPen(QColor(Qt::white));
        m_painter->drawText(real(position), imag(position), QString::number(roundabout->vehicles_count()));
    }
}
            
//  Draws traffic lights...
//  gate : EXIT (1) or ENTRANCE (1)
void Scene::draw_semaphore(Lane* lane) {
    //unsigned short i = 0;
    //while (i < road.roundabouts().size()) {
        //Roundabout* other_roundabout    = road.other_extremity(road.roundabouts(i));
    //bool        state               = road.lights(road.roundabouts(i), extremity);
    QColor colors[3];
    colors[0] = colors[1] = colors[2] = QColor(Qt::black);

    //Vector
    //        parallel    = road.reference(road.roundabouts(i)),
    //        orthogonal  = road.reference(road.roundabouts(i));

        if (lane->semaphore().state() == GREEN)     colors[0] = QColor(Qt::green);
        else                                        colors[2] = QColor(Qt::red);

        //if (extremity == EXIT && road.can_lead_to(road.roundabouts(i)))
            //Vector pos_start = road.roundabouts(i)->position() + orthogonal * 6 - parallel * 12;
        //else if (extremity == ENTRANCE && road.can_lead_to(other_roundabout))
            //pos_start = road.roundabouts(i)->position - orthogonal * 6 - parallel * 12;
        //else
        //    continue;
        complex<float> pos_start = *(lane->to()) + lane->v() * (complex<float>)6 - lane->u() * (complex<float>)12;

        unsigned short j(0);
        while (j < 3) {
            m_painter->setBrush(colors[j]);

            complex<float> position = pos_start + complex<float>(0, -1) * (complex<float>)(TF_RADIUS * 2 * j);
            m_painter->setPen(QColor(Qt::gray));
            m_painter->drawEllipse(real(position) - TF_RADIUS, imag(position) - TF_RADIUS, 2*TF_RADIUS, 2*TF_RADIUS);

            j++;
        }

        //i++;
}

//  /!\ Qt specific (please don't rename)
//  Manages what happens when a mouse button is pressed
void Scene::mousePressEvent(QMouseEvent* event) {
    // Experimental : select a roundabout or a vehicle
    //
    // TODO : 
    //   · (mPE.1) : avoid double selections (vehicle + roundabout)

    //m_window->select_vehicle(event->x(), event->y());
    m_window->select_roundabout(event->x(), event->y());
}
