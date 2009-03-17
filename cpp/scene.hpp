#ifndef SCENE
    #define SCENE

    //  Area where the scene will be drawn.
    class Scene : public QWidget
    {
        Q_OBJECT

        QWidget*    window;
        QPainter*   painter;

        Map*        map;
        
        public:
        Scene(const QWidget*);
        ~Scene();

        void paintEvent(QPaintEvent*);
        void draw();
        void draw(const Road&);
        void draw(const Lane&);
        void draw(const Vehicle&);
        void draw(const Roundabout&);
        void draw(const Road&, Extremity);
        void draw_selected_path();

        void mousePressEvent(QMouseEvent*);
    };
#endif

