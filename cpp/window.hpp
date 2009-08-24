#ifndef __WINDOW__
    #define __WINDOW__

    #include <QtGui>

    #define SPAWN_DELAY 4
    #define TITLE       "There Is No Rush -- C++ version"

    class Map;
    class Roundabout;
    class Scene;
    class Vehicle;


    //  The main window that encapsulates the scene and controls
    class MainWindow : public QMainWindow {
        Q_OBJECT

        QBasicTimer m_timer;
        /*QCheckBox*  m_entrance_lights;
        QCheckBox*  m_exit_lights;*/
        QCheckBox*  m_display_semaphores;
        QCheckBox*  m_display_vehicles;
        QCheckBox*  m_antialiasing;
        QCheckBox*  m_density;
        QCheckBox*  m_is_spawning;
        QLabel*     lbl_info;
        QLabel*     lbl_selection;
        QSpinBox*   m_spawn_delay;
        QSpinBox*   m_simulation_speed;
        QWidget*    m_central_widget;
        Scene*      m_scene;
        Vehicle*    m_selected_vehicle;
        Roundabout* m_selected_roundabout;
        float       m_delta_t;
        float       m_last_update;

        public:
        MainWindow();
        ~MainWindow();

        bool        antialiasing()          const;
        bool        display_semaphores()    const;
        bool        display_vehicles()      const;
        Map*        map()                   const;
        Roundabout* selected_roundabout()   const;
        Vehicle*    selected_vehicle()      const;

        void    setup_interface();

        void    select_roundabout(unsigned short, unsigned short);
        void    select_vehicle(unsigned short, unsigned short);

        void    update_simulation(float);
        void    update_panel();

        QString simulation_informations();
        QString selected_roundabout_informations();
        QString selected_vehicle_informations();

        void    closeEvent(QCloseEvent*);
        void    keyPressEvent(QKeyEvent*);
        void    timerEvent(QTimerEvent*);
        void    update();

        public slots:
        void    fastforward();
        void    pause();
        void    play();
        void    reset();
    };
#endif

