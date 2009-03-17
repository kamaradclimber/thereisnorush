#ifndef HISTOGRAM
    #define HISTOGRAM
    
    class Histogram : public QWidget
    {
        Q_OBJECT
        
        QWidget*    window;
        QPainter*   painter;
        QColor
            color,
            col_border,
            col_background;
        
        vector<unsigned float> data;

        unsigned int timer;
        unsigned float
            max,
            min;
        
        public:
        Histogram(const QWidget*, unsigned short span = HISTOGRAM_SPAN, QColor& color = HISTOGRAM_COLOR, unsigned short width = HISTOGRAM_WIDTH, unsigned short height = HISTOGRAM_HEIGHT);
        ~Histogram();

        void append(unsigned float);
        void draw_bars()                const;
        void draw_borders()             const;
        void draw_scale()               const;
        void draw_background()          const;
        void draw()                     const;

        void paintEvent(QPaintEvent*);
    };
#endif

