#ifndef __SCENE__
    #define __SCENE__

    #include <QtGui>

    #include "map.hpp"

    #define SCENE_WIDTH     800
    #define SCENE_HEIGHT    600
    #define TF_RADIUS       3

    class Lane;
    class Road;
    class Roundabout;
    class Vehicle;
    class MainWindow;

    //  Area where the scene will be drawn.
    class Scene : public QWidget {
        Q_OBJECT

        MainWindow*     m_window;
        QPainter*       m_painter;

        Map             m_map;
        
        public:
        Scene(MainWindow*);
        ~Scene();

        Map* map();

        void paintEvent(QPaintEvent*);
        void draw();
        void draw(Road*);
        void draw(Lane*);
        void draw(Vehicle*);
        void draw(Roundabout*);
        void draw_semaphore(Lane*);
        void draw_selected_path();

        void mousePressEvent(QMouseEvent*);
    };
#endif

