#ifndef MAIN_WINDOW
    #define MAIN_WINDOW

    //  The main window that encapsulates the scene and controls
    class MainWindow : public QMainWindow
    {
        Q_OBJECT

        QBasicTimer timer;
        QCheckBox*
            entrance_lights,
            exit_lights,
            antialiasing,
            density,
            spawning;
        Scene*      scene;
        Vehicle*    selected_vehicle;
        Roundabout* selected_roundabout;
        unsigned float
            delta_t,
            last_update;


        public:
        MainWindow();
        ~MainWindow();

        void    setup_interface();
        void    play();
        void    pause();
        void    reset();
        void    fastforward();

        void    select_roundabout(unsigned short, unsigned short);
        void    select_vehicle(unsigned short, unsigned short);

        void    update_simulation();
        void    update_stats();

        QString simulation_informations();
        QString selected_roundabout_informations();
        QString selected_vehicle_informations();

        void    closeEvent(QCloseEvent*);
        void    keyPressEvent(QKeyEvent*);
        void    timerEvent(QTimerEvent*);
    };
#endif

