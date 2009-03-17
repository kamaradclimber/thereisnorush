#include "constants.hpp"
#include "hpp"

//  Builds the main window.
MainWindow::MainWindow() : delta_t(0), last_update(clock()), selected_vehicle(NULL), selected_roundabout(NULL), timer()
{
    //   Set the interface
    setup_interface();

    //   Start the timer
    timer.start(10, this);
}

//  Sets up the Qt interface, layout, slots & properties
void MainWindow::setup_interface()
{
    //   Window settings
    setObjectName("MainWindow");

    QRect screen = QDesktopWidget().screenGeometry();
    resize(screen.width(), screen.height());

    setWindowTitle(TITLE);
    setWindowIcon(QIcon("icons/tinr_logo.png"));
    statusBar().showMessage("Ready");

    setCentralWidget(QWidget());

    //   Exit action
    QAction* act_exit = new QAction(QIcon("icons/exit.png"), "Exit", this);
        act_exit->setShortcut("Ctrl+Q");
        act_exit->setStatusTip("Exit application");
        connect(act_exit, SIGNAL("triggered()"), SLOT("close()"));

    //   Play action
    QAction act_play = new QAction(QIcon("icons/play.png"), "Play", this);
        //act_play->setShortcut("Ctrl+P");
        act_play->setStatusTip("Play simulation");
        connect(act_play, SIGNAL("triggered()"), play);

    //   Pause action
    QAction* act_pause = new QAction(QIcon("icons/pause.png"), "Pause", this);
        //act_pause->setShortcut("Ctrl+P");
        act_pause->setStatusTip("Pause simulation");
        connect(act_pause, SIGNAL("triggered()"), pause);

    //   Fast forward action
    QAction* act_fastforward = new QAction(QIcon("icons/forward.png"), "Fast forward", this);
        act_fastforward->setStatusTip("Fast forward simulation (x2 - x4 - x8)");
        connect(act_fastforward, SIGNAL("triggered()"), fastforward);

    //   Reset action
    QAction* act_reset = new QAction(QIcon("icons/reset.png"), "Reset", this);
        //act_reset->setShortcut("Ctrl+R");
        act_reset->setStatusTip("Reset simulation");
        connect(act_reset, SIGNAL("triggered()"), reset);

    //   File menu
    QMenu* file = menuBar()->addMenu("&File");
        file->addAction(act_exit);

    //   Simulation menu
    QMenu* simulation = menuBar()->addMenu("&Simulation");
        simulation->addAction(act_play);
        simulation->addAction(act_pause);
        simulation->addAction(act_fastforward);
        simulation->addAction(act_reset);

    //   Toolbar
    QToolBar* main_toolbar = addToolBar("Main toolbar");
        main_toolbar->addAction(act_play);
        main_toolbar->addAction(act_pause);
        main_toolbar->addAction(act_fastforward);
        main_toolbar->addAction(act_reset);

    //   Scene
    scene = new Scene(this);
        scene->setObjectName("scene");

    // Histogram
    //histogram = Histogram(this)
    //histogram.setObjectName("histogram")

    //   Information box
    QLabel* lbl_info = new QLabel("<i>Information</i>", this);
        lbl_info->setAlignment(Qt::AlignLeading|Qt::AlignLeft|Qt::.AlignTop);
        lbl_info->setWordWrap(true);
        lbl_info->setObjectName("lbl_info");

    QVBoxLayout* lay_info = new QVBoxLayout(this);
        lay_info->addWidget(lbl_info);
        //lay_info->addWidget(histogram);

    QGroupBox* box_info = new QGroupBox("Informations", this);
        box_info->setObjectName("box_info");
        box_info->setLayout(lay_info);

    //   Commands box
    entrance_lights = new QCheckBox("Display entrance traffic lights", this);
        entrance_lights->setObjectName("entrance_lights");
        entrance_lights->setChecked(false);

    exit_lights = new QCheckBox("Display exit traffic lights", this);
        exit_lights->setObjectName("exit_lights");
        exit_lights->setChecked(true);

    antialiasing = new QCheckBox("Use antialiasing", this);
        antialiasing->setObjectName("antialiasing");
        antialiasing->setChecked(false);

    display_density = new QCheckBox("Display density", this);
        display_density->setObjectName("display_density");
        display_density->setChecked(false);

    spawning = new QCheckBox("Roundabout is spawning", this);
        spawning->setObjectName("is_spawning");
        spawning->setCheckable(false);

    QLabel* lbl_spawn_delay = new QLabel("Spawn delay", this);
    spawn_delay = new QSpinBox(this);
        spawn_delay->setSingleStep(100);
        spawn_delay->setRange(1000, 30000);
        spawn_delay->setSuffix("ms");
        spawn_delay->setValue(SPAWN_DELAY * 1000.0);

    QGridLayout* lay_commands = new QGridLayout(this);
        lay_commands->addWidget(entrance_lights, 0, 0, 1, 2);
        lay_commands->addWidget(exit_lights, 1, 0, 1, 2);
        lay_commands->addWidget(antialiasing, 2, 0, 1, 2);
        lay_commands->addWidget(display_density, 3, 0, 1, 2);
        lay_commands->addWidget(spawning, 4, 0, 1, 2);
        lay_commands->addWidget(lbl_spawn_delay, 5, 0);
        lay_commands->addWidget(spawn_delay, 5, 1);

    QGroupBox* box_commands = new QGroupBox("Commands", this);
        box_commands->setObjectName("box_commands");
        box_commands->setLayout(lay_commands);

    //   Control panel
    QVBoxLayout* lay_panel = QVBoxLayout(this);
        lay_panel->addWidget(box_info);
        lay_panel->addStretch(1);
        lay_panel->addWidget(box_commands);

    QFrame* panel = new QFrame(this);
        panel->setObjectName("panel");
        panel->setLayout(lay_panel);

    QMetaObject::connectSlotsByName(this);

    //   Display
    QGridLayout* lay_window = QGridLayout(this);
        lay_window->addWidget(scene, 0, 0);
        lay_window->addWidget(panel, 0, 1);

        centralWidget()->setLayout(lay_window);
}

//   If you find another way to implement the equivalent of the following 2 slots, please just change it ! -- Ch@hine
void MainWindow::play()
{
    set_speed(1.0);
}

void MainWindow::pause()
{
    set_speed(0.0);
}

void MainWindow::reset()
{
}

//  Plays the simulation at 2, 4 or 8×
void MainWindow::fastforward()
{
    sim_speed = get_speed();

    if (sim_speed == 8)
    {
        set_speed(1);
    }
    else
    {
        set_speed(2*sim_speed);
    }
}

//  /!\ Qt specific (please don"t rename)
//  Specifies what has to be done when exiting the application.
void MainWindow::closeEvent(QCloseEvent* event)
{
    event->accept();
    exit();
}

//  /!\ Qt specific (please don"t rename)
//  Manages keyboard events
void MainWindow::keyPressEvent(QKeyEvent* event)
{
    if (event->key() == Qt::Key_Escape)
    {
        exit();
    }
}

//  Selects the roundabout placed on x, y
//  Deselects if there is none
void MainWindow::select_roundabout(unsigned short x, unsigned short y)
{
    Vector pos_click(x, y);

    selected_roundabout = NULL;
    
    unsigned short i = 0;
    while (i < map->roundabouts.size())
    {
        if ((map->roundabouts(i).position - pos_click).norm() < map->roundabouts(i)->radius)
        {
            selected_roundabout = map->roundabouts(i);
            break;
        }
        
        i++;
    }
}

//  Selects the vehicle placed on x, y.
//  Deselects if there is none.
void MainWindow::select_vehicle(unsigned short x, unsigned short y)
{
    Vector pos_click(x, y);
    unsigned short
        selection_radius    = 20,
        i                   = 0,
        j                   = 0,
        k                   = 0;

    selected_vehicle = NULL;

    while (i < map->roads().size())
    {
        while (j < map->roads(i)->lanes().size())
        {
            while (k < map->roads(i)->lanes(j)->vehicles().size())
            {
                Vector pos_vehicle(map->roads(i)->lanes(j)->start->position + map->roads(i)->lanes(j)->parallel() * map->roads(i)->lanes(j)->vehicles(k)->length_covered());

                if ((pos_vehicle - pos_click).norm() < selection_radius)
                {
                    selected_vehicle = map->roads(i)->lanes(j)->vehicles(k);
                    break;
                }

                k++;
            }
            k = 0;
            j++;
        }

        j = 0;
        i++;
    }
}

//  /!\ Qt specific (please don"t rename)
//  Passes or uses timer events to update the simulation
void MainWindow::timerEvent(QTimerEvent* event)
{
    if (event->timerId() == timer->timerId())
    {
        // Manage internal time events
        delta_t = clock() - last_update;
        last_update = clock();

        // Update the simulation and informations
        update_simulation();
        update_stats();
        //histogram.update();
        scene->update();
    }

    else
    {
        QFrame::timerEvent(event);
    }
}

//  Updates the simulation
void MainWindow::update_simulation()
{
    //  Update the roads (and the vehicles)
    unsigned short i = 0;
    while (i < map->roads().size())
    {
        map->roads(i)->update();
        i++;
    }

    //  Get informations from the roundabouts (separate loop)
    i = 0;
    while (i < map->roundabouts().size())
    {
        map->roundabouts(i)->local_load();
        i++
    }
    
    //  Update the roundabouts
    i = 0;
    while (i < map->roundabouts().size())
    {
        map->roundabouts(i)->update();
        map->roundabouts(i)->set_spawn_time(spawn_delay->value() /1000.0);
        
        i++;
    }
}

//  Displays informations on the simulation and selected objects
void MainWindow::update_stats()
{
    QString information("");
        information += "<b>Roads : </b>"        + QString::number(map->roads().size())          + "<br/>";
        information += "<b>Roundabouts : </b>"  + QString::number(map->roundabouts().size())    + "<br/>";

    unsigned short
        vehicles_on_roads       = 0,
        vehicles_waiting        = 0,
        vehicles_on_roundabouts = 0;

    unsigned short i = 0;
    while (i < map->roads().size())
    {
        vehicles_on_roads += map->roads(i)->total_vehicles();
        vehicles_waiting  += map->roads(i)->total_waiting_vehicles(map->roads(i)->roundabouts[0]) + map->roads(i)->total_waiting_vehicles(map->roads(i)->roundabouts[1]);

        i++;
    }

    i = 0;
    while (i < map->roundabouts().size())
    {
        vehicles_on_roundabouts += map->roundabouts(i)->vehicles();
        i++;
    }
    
    unsigned short total_vehicles = vehicles_on_roads + vehicles_on_roundabouts;

    information += "<b>Cars</b> (total) : " + QString::number(total_vehicles)           + "<br/>";
    information += "(on roads) : "          + QString::number(vehicles_on_roads)        + "<br/>";
    information += "(on roundabouts) : "    + QString::number(vehicles_on_roundabouts)  + "<br/>";
    information += "(waiting) : "           + QString::number(vehicles_waiting)         + "<br/>";

    information += selected_roundabout_informations();
    information += selected_vehicle_informations();
                                                   
    information += simulation_informations();
  
    lbl_info->setText(information);
    //histogram->append(total_vehicles);
}

QString MainWindow::simulation_informations()
{
    QString information("<br/><b>Simulation</b><br/>");    

    hours   = (get_simulation_time())[0]; 
    minutes = (get_simulation_time())[1];
    seconds = (get_simulation_time())[2];

    information += "Time elapsed : " + QString::number(hours) + "<sup>h</sup>&nbsp;" + QString::number(minutes) + "<sup>m</sup>&nbsp;" + QString::number(seconds) + "<sup>s</sup><br/>";
    information += "Speed : &times;" + QString::number(round(get_speed(), 2))   + "<br/>";
    
    if (!delta_t)
    {
        information += "FPS : " + QString::number(round(get_speed()/delta_t, 2)) + "<br/>";
        information += "&Delta;t (s) : " + QString::number(round(delta_t, 2)) + "<br/>";
    }
    
    return information;
}

QString MainWindow::selected_roundabout_informations()
{
    QString information("");

    if (selected_roundabout != NULL)
    {
        information += "<br/><b>Selected roundabout :</b><br/>";
        information += "position : ("   + QString::number(selected_roundabout->x()) + "," + QString::number(selected_roundabout->y()) + ") <br/>";
        information += "radius : "      + QString::number(selected_roundabout->radius()) + "<br/>";
        information += "vehicles : "    + QString::number(selected_roundabout->vehicles().size()) + "<br/>";
        information += "load : "        + QString::number(round(selected_roundabout->global_load(), 2)) + "<br/>";
    
        if (selected_roundabout->spawning())
        {
            information += "<b>Spawning mode</b><br/>";
        }
        if (!selected_roundabout->leaving_lanes().size())
        {
            information += "<b>Destroying mode</b><br/>";
        }
        if (selected_roundabout->vehicles().size())
        {
            unsigned short
                avg_waiting_time    = 0,
                i                   = 0;

            while (i < selected_roundabout->vehicles().size())
            {
                avg_waiting_time += selected_roundabout->vehicles(i)->total_waiting_time() / float(selected_roundabout->vehicles().size());
                i++;
            }
            
            information += "<br/><b>Average waiting time</b> (s) : " + QString::number(round(avg_waiting_time, 2)) + "<br/>";
        }
        
        if (!spawning->isCheckable())
        {
            spawning.setCheckable(true);
            spawning.setChecked(selected_roundabout->spawning());
        }
        else
        {
            selected_roundabout->spawning = spawning.isChecked();
        }
    }
    else
    {
        spawning.setCheckable(false);
    }

    return information;
}

QString MainWindow::selected_vehicle_informations()
{
    QString information("");

    if (selected_vehicle != NULL)
    {
        Vehicle* vehicle = selected_vehicle;

        if (vehicle->dead())
        {
            selected_vehicle = NULL;
            return information;
        }

        information += "<br/><b>Selected vehicle :</b><br/>";

        if (vehicle->position != NULL)
        {
            information += "position : ("       + QString::number(round(vehicle->x(), 2)) + ", " + QString::number(round(vehicle->y(), 2)) + ") <br/>";
            information += "length, width : "   + QString::number(vehicle->length()) + ", " +  QString::number(vehicle->width()) +"<br/>";
            information += "speed : "           + QString::number(round(vehicle->speed(), 2)) + "<br/>";
            information += "waiting time : "    + QString::number(round(vehicle->total_waiting_time(), 2)) + "<br/>";
        }

        if (vehicle->destination() != NULL)
        {
            information += "destination : " + QString::number(vehicle->destination()->name()) + " <br/>";
        }

        if (vehicle->waiting())
        {
            information += "<b>Waiting or braking</b><br/>";
        }
    }

    return information;
}

//  Returns the time multiplied by the simulation speed
unsigned float MainWindow::clock() const
{
    if (!time_last_counter)
    {
        time_last_counter = time.clock()

    time_interval = time.clock() - time_last_counter
    time_static_counter += time_interval * simulation_speed
            
    time_last_counter = time.clock()
    
    return time_static_counter
    
void set_speed(new_speed)
    //
    Sets the simulation speed
    Please use this instead of directly addressing simulation_speed
    //
    
    simulation_speed = new_speed
    
void get_speed()
    //
    Returns the simulation speed
    Please use this instead of directly addressing simulation_speed
    //
    return simulation_speed

void get_simulation_time()
    //
    Returns the simulation time (h, m, s)
    //
    
    timer = time_static_counter
    
    hours   = int(timer / 3600.0) % 24
    minutes = int(timer / 60.0)   % 60
    seconds = int(timer)          % 60
    
    return hours, minutes, seconds
