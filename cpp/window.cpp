#include <complex>
#include <iostream>

#include "lane.hpp"
#include "map.hpp"
#include "road.hpp"
#include "roundabout.hpp"
#include "scene.hpp"
#include "vehicle.hpp"
#include "window.hpp"

using namespace std;

//  Builds the main window.
MainWindow::MainWindow() : m_delta_t(0), m_last_update(clock()), m_selected_vehicle(0), m_selected_roundabout(0), m_timer() {
    //   Set the interface
    setup_interface();

    //   Start the timer
    m_timer.start(100, this);
}

MainWindow::~MainWindow() {
    /*delete m_entrance_lights;
    delete m_exit_lights;*/
    delete m_antialiasing;
    delete m_density;
    delete m_is_spawning;
    delete lbl_info;
    delete m_spawn_delay;
    delete m_scene;
}


//  Accessors
bool MainWindow::antialiasing() const {
    return (m_antialiasing->checkState() == Qt::Checked);
}

bool MainWindow::display_semaphores() const {
    return (m_display_semaphores->checkState() == Qt::Checked);
}

bool MainWindow::display_vehicles() const {
    return (m_display_vehicles->checkState() == Qt::Checked);
}


Map* MainWindow::map() const {
    return m_scene->map();
}

Roundabout* MainWindow::selected_roundabout() const {
    return m_selected_roundabout;
}

Vehicle* MainWindow::selected_vehicle() const {
    return m_selected_vehicle;
}


//  Sets up the Qt interface, layout, slots & properties
void MainWindow::setup_interface() {
    //   Window settings
    setObjectName("MainWindow");

    QRect screen = QDesktopWidget().screenGeometry();
    resize(screen.width(), screen.height());

    setWindowTitle(QString("There Is No Rush -- C++ reborn"));
    setWindowIcon(QIcon("icons/logo.png"));
    statusBar()->showMessage(QString("Ready"));

    m_central_widget = new QWidget;
    setCentralWidget(m_central_widget);

    //   Exit action
    QAction* act_exit = new QAction(QIcon("icons/exit.png"), "Exit", this);
        //act_exit->setShortcut("Ctrl+Q");
        act_exit->setStatusTip("Exit application");
        connect(act_exit, SIGNAL(triggered()), SLOT(close()));

    //   Play action
    QAction* act_play = new QAction(QIcon("icons/play.png"), "Play", this);
        //act_play->setShortcut("Ctrl+P");
        act_play->setStatusTip("Play simulation");
        connect(act_play, SIGNAL(triggered()), SLOT(play()));

    //   Pause action
    QAction* act_pause = new QAction(QIcon("icons/pause.png"), "Pause", this);
        //act_pause->setShortcut("Ctrl+P");
        act_pause->setStatusTip("Pause simulation");
        connect(act_pause, SIGNAL(triggered()), SLOT(pause()));

    //   Fast forward action
    QAction* act_fastforward = new QAction(QIcon("icons/forward.png"), "Fast forward", this);
        act_fastforward->setStatusTip("Fast forward simulation (x2 - x4 - x8)");
        connect(act_fastforward, SIGNAL(triggered()), SLOT(fastforward()));

    //   Reset action
    QAction* act_reset = new QAction(QIcon("icons/reset.png"), "Reset", this);
        //act_reset->setShortcut("Ctrl+R");
        act_reset->setStatusTip("Reset simulation");
        connect(act_reset, SIGNAL(triggered()), SLOT(reset()));

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
    m_scene = new Scene(this);
        m_scene->setObjectName("scene");

    // Histogram
    //histogram = Histogram(this)
    //histogram.setObjectName("histogram")

    //   Information box
    lbl_info = new QLabel("<i>Loading...</i>", this);
        lbl_info->setAlignment(Qt::AlignLeading|Qt::AlignLeft|Qt::AlignTop);
        lbl_info->setWordWrap(true);
        lbl_info->setObjectName("lbl_info");

    QVBoxLayout* lay_info = new QVBoxLayout(this);
        lay_info->addWidget(lbl_info);
        //lay_info->addWidget(histogram);

    QGroupBox* box_info = new QGroupBox("Statistics", this);
        box_info->setObjectName("box_info");
        box_info->setLayout(lay_info);

    //  Selection information
    lbl_selection = new QLabel("<i>No selection.</i>", this);
        lbl_info->setAlignment(Qt::AlignLeading|Qt::AlignLeft|Qt::AlignTop);
        lbl_info->setWordWrap(true);
        lbl_info->setObjectName("lbl_selection");

    QVBoxLayout* lay_selection = new QVBoxLayout(this);
        lay_selection->addWidget(lbl_selection);

    QGroupBox* box_selection = new QGroupBox("Selection", this);
        box_selection->setObjectName("box_selection");
        box_selection->setLayout(lay_selection);


    //   Commands box
    m_is_spawning = new QCheckBox("Roundabout is spawning", this);
        m_is_spawning->setObjectName("is_spawning");
        m_is_spawning->setCheckable(false);

    QLabel* lbl_spawn_delay = new QLabel("Spawn delay", this);
    m_spawn_delay = new QSpinBox(this);
        m_spawn_delay->setSingleStep(100);
        m_spawn_delay->setRange(1000, 30000);
        m_spawn_delay->setSuffix(" ms");
        m_spawn_delay->setValue(SPAWN_DELAY * 1000.0);

    QLabel* lbl_simulation_speed = new QLabel("Simulation speed", this);
    m_simulation_speed = new QSpinBox(this);
        m_simulation_speed->setSingleStep(1);
        m_simulation_speed->setRange(0, 10);
        m_simulation_speed->setSuffix(" x");
        m_simulation_speed->setValue(1);

    QGridLayout* lay_commands = new QGridLayout(this);
        lay_commands->addWidget(m_is_spawning, 0, 0, 1, 2);
        lay_commands->addWidget(lbl_spawn_delay, 1, 0);
        lay_commands->addWidget(m_spawn_delay, 1, 1);
        lay_commands->addWidget(lbl_simulation_speed, 2, 0);
        lay_commands->addWidget(m_simulation_speed, 2, 1);

    QGroupBox* box_commands = new QGroupBox("Commands", this);
        box_commands->setObjectName("box_commands");
        box_commands->setLayout(lay_commands);


    //  Display options
    m_display_semaphores = new QCheckBox("Display traffic lights", this);
        m_display_semaphores->setChecked(true);

    m_display_vehicles = new QCheckBox("Display vehicles", this);
        m_display_vehicles->setChecked(true);

    m_antialiasing = new QCheckBox("Use antialiasing", this);
        m_antialiasing->setObjectName("antialiasing");
        m_antialiasing->setChecked(false);

    /*m_display_density = new QCheckBox("Display density", this);
        m_display_density->setObjectName("display_density");
        m_display_density->setChecked(false);*/

    QGridLayout* lay_display = new QGridLayout(this);
        lay_display->addWidget(m_display_semaphores, 0, 0);
        lay_display->addWidget(m_display_vehicles, 1, 0);
        lay_display->addWidget(m_antialiasing, 2, 0);
        //lay_commands->addWidget(m_display_density, 3, 0, 1, 2);

    QGroupBox* box_display = new QGroupBox("Display options", this);
        box_display->setLayout(lay_display);
    
        
    //   Control panel
    QVBoxLayout* lay_panel = new QVBoxLayout(this);
        lay_panel->addWidget(box_info);
        lay_panel->addWidget(box_selection);
        lay_panel->addStretch(1);
        lay_panel->addWidget(box_display);
        lay_panel->addWidget(box_commands);

    QFrame* panel = new QFrame(this);
        panel->setObjectName("panel");
        panel->setLayout(lay_panel);

    QMetaObject::connectSlotsByName(this);

    //   Display
    QGridLayout* lay_window = new QGridLayout(m_central_widget);
        lay_window->addWidget(m_scene, 0, 0);
        lay_window->addWidget(panel, 0, 1);

    centralWidget()->setLayout(lay_window);
}

//   If you find another way to implement the equivalent of the following 2 slots, please just change it ! -- Ch@hine
void MainWindow::play() {
    m_simulation_speed->setValue(1);
}

void MainWindow::pause() {
    m_simulation_speed->setValue(0);
}

//  TODO
void MainWindow::reset() {
}

//  Plays the simulation at 2, 4 or 8×
void MainWindow::fastforward() {
    /*if (m_simulation_speed == 8)    m_simulation_speed = 1;
    else                            m_simulation_speed *= 2;*/
}

//  /!\ Qt specific (please don"t rename)
//  Specifies what has to be done when exiting the application.
void MainWindow::closeEvent(QCloseEvent* event) {
    event->accept();
    exit(EXIT_SUCCESS);
}

//  /!\ Qt specific (please don"t rename)
//  Manages keyboard events
void MainWindow::keyPressEvent(QKeyEvent* event) {
    if (event->key() == Qt::Key_Escape)     exit(EXIT_SUCCESS);
}

//  Selects the roundabout placed on x, y
//  Deselects if there is none
void MainWindow::select_roundabout(unsigned short x, unsigned short y) {
    complex<float> pos_click(x, y);

    m_selected_roundabout = 0;
    
    unsigned short i(0);
    while (i < map()->roundabouts_count()) {
        if (abs(*(map()->roundabout(i)) - pos_click) < 5) {
            m_selected_roundabout = map()->roundabout(i);
            break;
        }
        
        i++;
    }
}

//  Selects the vehicle placed on x, y.
//  Deselects if there is none.
//  TODO : optimize this function !
void MainWindow::select_vehicle(unsigned short x, unsigned short y) {
    complex<float> pos_click(x, y);
    unsigned short selection_radius(20);
    unsigned short i(0);
    unsigned short j(0);
    unsigned short k(0);
    unsigned short l(0);

    m_selected_vehicle = 0;

    while (i < map()->roads_count()) {
        while (j < map()->road(i)->lanes_count()) {
            while (l < 2) {
                while (k < map()->road(i)->lane(l, j)->vehicles_count()) {
                    Vehicle* vehicle = map()->road(i)->lane(l, j)->vehicle(k);
    
                    if (abs(vehicle->position() - pos_click) < selection_radius) {
                        m_selected_vehicle = vehicle;
                        break;
                    }
    
                    k++;
                }

                k = 0;
                l++;
            }
            
            l = 0;
            j++;
        }

        j = 0;
        i++;
    }
}

//  /!\ Qt specific (please don"t rename)
//  Passes or uses timer events to update the simulation
void MainWindow::timerEvent(QTimerEvent* event) {
    if (event->timerId() == m_timer.timerId()) {
        // Manage internal time events
        // TODO: use real value instead of 1000000 (clock per second)
        m_delta_t = (clock() - m_last_update) / 1000000.;
        m_last_update = clock();

        // Update the simulation and informations
        update_simulation(m_delta_t*m_simulation_speed->value());
        update_panel();
        //histogram.update();
        m_scene->update();
    }

    //else
        //QFrame::timerEvent(event);
}

void MainWindow::update() {
    // Manage internal time events
    // TODO: use real value instead of 100000 (clock per second)
    m_delta_t = (clock() - m_last_update) / 100000.;
    if (m_delta_t < 0.10) return;
    

    m_last_update = clock();

    // Update the simulation and informations
    update_simulation(m_delta_t);
    //update_panel();
    //histogram.update();
    m_scene->update();
}

//  Updates the simulation
void MainWindow::update_simulation(float delta_t) {
    //  Update the roads
    unsigned short i(0);
    while (i < map()->roads_count()) {
        map()->road(i)->update(delta_t);
        i++;
    }

    //  Get informations from the roundabouts (separate loop)
    /*i = 0;
    while (i < map()->roundabouts_count()) {
        map()->roundabout(i)->local_load();
        i++
    }*/
    
    //  Update the roundabouts
    i = 0;
    while (i < map()->roundabouts_count()) {
        map()->roundabout(i)->update(delta_t);
        map()->roundabout(i)->set_spawn_delay(m_spawn_delay->value() /1000.0);
        
        i++;
    }
}

//  Displays informations on the simulation and selected objects
void MainWindow::update_panel() {
    QString information("");
        information += "<strong>" + QString::number(map()->roads_count()) + "</strong> road(s)<br/>";
        information += "<strong>" + QString::number(map()->roundabouts_count()) + "</strong> roundabout(s)<br/>";

    unsigned short vehicles_on_roads(0);
    unsigned short vehicles_waiting(0);
    unsigned short vehicles_on_roundabouts(0);

    unsigned short i(0);
    while (i < map()->roads_count()) {
        vehicles_on_roads += map()->road(i)->vehicles_count();
        vehicles_waiting  += map()->road(i)->waiting_vehicles_count();

        i++;
    }

    i = 0;
    while (i < map()->roundabouts_count()) {
        vehicles_on_roundabouts += map()->roundabout(i)->vehicles_count();
        i++;
    }
    
    unsigned short total_vehicles(vehicles_on_roads + vehicles_on_roundabouts);

    information += "<strong>" + QString::number(total_vehicles) + "</strong> vehicles<br/>";
    information += "(<strong>" + QString::number(vehicles_on_roads) + "</strong> on roads)<br/>";
    information += "(<strong>" + QString::number(vehicles_on_roundabouts) + "</strong> on roundabouts)<br/>";
    information += "(<strong>" + QString::number(vehicles_waiting) + "</strong> waiting)<br/>";
                                                   
    information += simulation_informations();
  
    lbl_info->setText(information);
    

    //  Update selection information
    lbl_selection->setText(selection_report());
    //information += selected_vehicle_informations();
    
    //histogram->append(total_vehicles);
}

QString MainWindow::selection_report() const {
    if (m_selected_roundabout)  return report(m_selected_roundabout);
    if (m_selected_vehicle)     return report(m_selected_vehicle);

    return QString("No selection.");
}

QString MainWindow::simulation_informations() {
    QString information("<br/><b>Simulation</b><br/>"); 

    /*unsigned short
        hours   = (get_simulation_time())[0],
        minutes = (get_simulation_time())[1],
        seconds = (get_simulation_time())[2];

    information += "Time elapsed : " + QString::number(hours) + "<sup>h</sup>&nbsp;" + QString::number(minutes) + "<sup>m</sup>&nbsp;" + QString::number(seconds) + "<sup>s</sup><br/>";*/
    
    if (!m_delta_t) {
        //information += "FPS : " + QString::number(round(m_simulation_speed/m_delta_t)) + "<br/>";
        information += "&Delta;t (s) : " + QString::number(round(m_delta_t)) + "<br/>";
    }
    
    return information;
}

QString MainWindow::selected_roundabout_informations() {
    if (!m_selected_roundabout)     {m_is_spawning->setCheckable(false); return QString("No selection.");}
        
    
    QString information("");
    //information += "position : ("   + QString::number(m_selected_roundabout->x()) + "," + QString::number(m_selected_roundabout->y()) + ") <br/>";
    //information += "radius : "      + QString::number(m_selected_roundabout->radius()) + "<br/>";
    information += "vehicles : "    + QString::number(m_selected_roundabout->vehicles_count()) + "<br/>";
    information += "load : "        + QString::number(round(m_selected_roundabout->global_load())) + "<br/>";

    if (m_selected_roundabout->is_spawning())   information += "<b>Spawning mode</b><br/>";
    if (m_selected_roundabout->vehicles_count()) {
        unsigned short
            avg_waiting_time    = 0,
            i                   = 0;

        /*while (i < m_selected_roundabout->vehicles_count()) {
            avg_waiting_time += m_selected_roundabout->vehicle(i)->waiting_time_count() / (float)(m_selected_roundabout->vehicles_count());
            i++;
        }
        
        information += "<br/><b>Average waiting time</b> (s) : " + QString::number(round(avg_waiting_time)) + "<br/>";*/
    }
    
    if (!m_is_spawning->isCheckable()) {
        m_is_spawning->setCheckable(true);
        m_is_spawning->setChecked(m_selected_roundabout->is_spawning());
    }
    else    m_selected_roundabout->set_spawning(m_is_spawning->isChecked());

    return information;
}

/*QString MainWindow::selected_vehicle_informations() {
    QString information("");

    if (m_selected_vehicle != NULL) {
        Vehicle* vehicle = m_selected_vehicle;

        if (vehicle->is_dead()) {
            m_selected_vehicle = 0;
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
            information += "destination : " + QString::number(vehicle->destination()->name()) + " <br/>";

        if (vehicle->waiting())
            information += "<b>Waiting or braking</b><br/>";
    }

    return information;
}*/

//  Returns the time multiplied by the simulation speed
/*float MainWindow::clock() const {
    if (!time_last_counter)
        time_last_counter = time.clock()

    time_interval = time.clock() - time_last_counter
    time_static_counter += time_interval * simulation_speed
            
    time_last_counter = time.clock()
    
    return time_static_counter
}
    
//  Returns the simulation time (h, m, s)
void MainWindow::simulation_time() {
    m_timer = time_static_counter;
    
    hours   = int(m_timer / 3600.0) % 24
    minutes = int(m_timer / 60.0)   % 60
    seconds = int(m_timer)          % 60
    
    return hours, minutes, seconds
}*/
