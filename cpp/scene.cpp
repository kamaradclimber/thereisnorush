//include "scene.hpp"
//include "constants.hpp"


Scene::Scene(QWidget* new_window, Map* new_map) : painter(NULL), window(new_window), map(new_map)
{
    setSizePolicy(QSizePolicy(QSizePolicy::Expanding, QSizePolicy::Expanding));
    setMinimumSize(SCENE_WIDTH, SCENE_HEIGHT);
}

Scene::~Scene()
{
}

//  /!\ Qt specific (please don't rename) : is triggered each time the update() method is called.
//  Specifies how the control should draw it
void Scene::paintEvent(QPaintEvent* event)
{
    painter = new QPainter();

    //  Set antialiasing
    painter->setRenderHint(QPainter::Antialiasing, window->use_antialiasing->isChecked());

    //  Draw background color and scene
    painter->fillRect(QRectF(QPointF(0, 0), QPointF(width(), height())), QColor(Qt::black));
    draw();

    painter->end();
}

//  Draws the complete scene on the screen.
void Scene::draw()
{
    //   Draw the roads and roundabouts
    unsigned short i = 0;

    while (i < map->roads.size())
    {
        draw(map->roads[i]);
        i++;
    }

    i = 0;
    while (i < map->roundabouts.size())
    {
        draw(map->roundabouts[i]);
        i++;
    }
    
    //   Manage selections
    draw_selected_path()
}

//  Draws a given road on the screen and all the vehicles on it.
//  road (Road) : the aforementioned road.
void Scene::draw(const Road& road)
{
    Vector
        pos_start   = road.roundabouts(0)->position.ceil(),
        pos_end     = road.roundabouts(1)->position.ceil();
    
    //   Draw traffic lights (or not)
    if (window->entrance_lights->isChecked())
    {
        draw(road, ENTRANCE);
    }
    
    if (window->exit_lights->isChecked())
    {
        draw(road, EXIT);
    }

    //   Draw a line to represent the road
    painter->setPen(DEFAULT[ROAD][COLOR]);
    painter->drawLine(pos_start.x, pos_start.y, pos_end.x, pos_end.y);

    //   Draw lanes individually
    unsigned short i = 0;
    while (i < road.lanes().size())
    {
        draw(road.lanes(i));
        i++;
    }
}

//  When a vehicle is selected, draw its path
void Scene::draw_selected_path()
{
    Vehicle vehicle = window->selected_vehicle;

    if (vehicle == NULL)
    {
        return void;
    }

    if (vehicle.lane() != NULL)
    {
        Vector
            pos_start = vehicle->position() - vehicle->lane().orthogonal() * vehicle->width()/2;
            pos_end   = vehicle->lane().end().position();

        painter->setPen(QColor(Qt::blue));
        painter->drawLine(pos_start.x, pos_start.y, pos_end.x, pos_end.y);

        if (vehicle->path != NULL)
        {
            unsigned short i = 0;
            while (i < vehicle->path.size())
            {
                pos_start = vehicle->path[i]->roundabouts(0)->position;
                pos_end   = vehicle->path[i]->roundabouts(1)->position;

                painter->drawLine(pos_start.x, pos_start.y, pos_end.x, pos_end.y);
                
                i++;
            }
        }
    }
}

//  Draws a lane and all the vehicles on it.
void Scene::draw(const Lane& lane)
{
    unsigned short i = 0;
    while (i < lane.vehicles().size())
    {
        draw(lane.vehicles(i));
        i++;
    }
}

//  Draws a given vehicle on the screen.
//  vehicle (Car) : the aforementioned vehicle.
void Scene::draw(const Vehicle& vehicle)
{
    if (vehicle.road() == NULL)
    {
        return void;
    }

    //   Get them once
    r_width     = vehicle.width();
    r_length    = vehicle.length();
    parallel    = vehicle.lane().reference(PARALLEL);
    orthogonal  = vehicle.lane().reference(ORTHOGONAL);

    //   Vehicles are rectangles whose sides are parallel and perpendicular to the road
    Vector points[4];
        points[0] = vehicle.position() - parallel * r_length/2 - orthogonal * r_width/2;
        points[1] = vehicle.position() + parallel * r_length/2 - orthogonal * r_width/2;
        points[2] = vehicle.position() + parallel * r_length/2 + orthogonal * r_width/2;
        points[3] = vehicle.position() - parallel * r_length/2 + orthogonal * r_width/2;
    
    QPointF polygon[4];
    unsigned short i = 0;
    while (i < 4)
    {
        polygon[i] = QPointF(points[i].x, points[i].y);
        i++;
    }
    
    //   Draw the vehicle
    painter->setBrush(vehicle.color());
    painter->setPen(QColor(Qt::black));
    painter->drawPolygon(polygon[0], polygon[1], polygon[2], polygon[3]);

    //   Selected vehicle : draw selection circle
    if (window->selected_vehicle == &vehicle)
    {
        painter->setPen(DEFAULT[ROUNDABOUT][COLOR]);
        painter->setBrush(QColor(Qt::transparent));
        painter->drawEllipse(vehicle.position().x - vehicle.length(), vehicle.position().y - vehicle.length(), 2*vehicle.length(), 2*vehicle.length());
    }
}

//  Draws a given roundabout on the screen.
//  roundabout (Roundabout) : the aforementioned roundabout.
void Scene::draw(const Roundabout& roundabout)
{
    // TODO :
    //       · (DN1) draw the vehicles on the roundabout

    //   Draw a red circle to represent a roundabout
    if (map->picture == NULL)
    {
        painter->setBrush(QColor(Qt::red));
        painter->setPen(QColor(Qt::transparent));
        painter->drawEllipse(roundabout.position().x - roundabout.radius()/4, roundabout.position().y - roundabout.radius()/4, roundabout.radius()/2, roundabout.radius()/2);

        return void;
    }
    

    //   Selected roudabout : draw selection circle
    if (window->selected_roundabout() == &roundabout)
    {
        painter->setPen(DEFAULT[ROUNDABOUT][COLOR]);
        painter->setBrush(QColor(Qt::transparent));
        painter->drawEllipse(roundabout.position().x - roundabout.radius(), roundabout.position().y - roundabout.radius(), 2 * roundabout.radius(), 2 * roundabout.radius());

    }
    
    if (roundabout.vehicles().size())
    {
        // There are vehicles on the roundabout, we may want to draw them
        // albeit we can't use draw_vehicle here...

        //TEMPORARY : the number of vehicles on the roundabout is written
        position = Vector(roundabout.position().x + 10, roundabout.position().y + 10)
        painter->setPen(QColor(Qt::white));
        painter->drawText(position.x, position.y, QString::number(roundabout.vehicles().size()));
    }
}
            
//  Draws traffic lights...
//  gate : EXIT (1) or ENTRANCE (1)
void Scene::draw(const Road& road, Extremity extremity)
{
    unsigned short i = 0;
    while (i < road.roundabouts().size())
    {
        Roundabout* other_roundabout    = road.other_extremity(road.roundabouts(i));
        bool        state               = road.lights(road.roundabouts(i), extremity);
        QColor      colors[3]           = {QColor(Qt::black), QColor(Qt::black), QColor(Qt::black)};
        Vector
            parallel    = road.reference(road.roundabouts(i)),
            orthogonal  = road.reference(road.roundabouts(i));

        if (state)
        {
            colors[0] = QColor(Qt::green);
        }
        else
        {
            colors[2] = QColor(Qt::red);
        }

        if (extremity == EXIT && road.can_lead_to(road.roundabouts(i)))
        {
            Vector pos_start = road.roundabouts(i)->position() + orthogonal * 6 - parallel * 12;
        }
        else if (extremity == ENTRANCE && road.can_lead_to(other_roundabout))
        {
            pos_start = road.roundabouts(i)->position - orthogonal * 6 - parallel * 12;
        }
        else
        {
            continue;
        }

        unsigned short j = 0;
        while (j < 3)
        {
            painter->setBrush(colors[j]);

            Vector position = pos_start + Vector(0, -1) * TF_RADIUS * 2 * j;
            painter->setPen(QColor(Qt::gray));
            painter->drawEllipse(position.x - TF_RADIUS, position.y - TF_RADIUS, 2*TF_RADIUS, 2*TF_RADIUS);

            j++;
        }

        i++;
    }
}

//  /!\ Qt specific (please don't rename)
//  Manages what happens when a mouse button is pressed
void Scene::mousePressEvent(QMouseEvent* event)
{
    // Experimental : select a roundabout or a vehicle
    //
    // TODO : 
    //   · (mPE.1) : avoid double selections (vehicle + roundabout)

    window->select_vehicle(event->x(), event->y());
    window->select_roundabout(event->x(), event->y());
}
