#include "histogram.hpp"

/*
    Initializes histogram representation
        span : the period of time to be taken into account
        width, height : dimensions
*/
Histogram::Histogram(const QWidget* new_window, unsigned short span, const QColor& new_color, unsigned short width, unsigned short height) : window(new_window), painter(NULL), data(span, 0.0), max(0.0), min(0.0), color(new_color), col_border(QColor(Qt::grey)), col_background(QColor(Qt::black)), timer(0) 
{
    setSizePolicy(QtGui::QSizePolicy(QtGui::QSizePolicy::Fixed, QtGui::QSizePolicy::Fixed));
    setMinimumSize(width, height);
}

//  Appends an event to the histogram
void Histogram::append(unsigned float value)
{    
    //  Shift data and replace the first element
    data    = shift(data);
    data[0] = value;
    
    timer++;

    //  Keep track of the extremes
    if (value > max)
    {
        max = value;
    }

    else if (value < min)
    {
        min = value;
    }
}


//  Draw the histobars
void Histogram::draw_bars() const
{
    //  No data to plot
    if (!max)
    {
        return void;
    } 

    //  Keep 20% of free space
    unsigned float extra_space = 0.2 * max;

    // Height and width for a unit bar
    unsigned float
        bar_width   = width() / (float)(data.size()),
        bar_height  = height() / (float)(max + extra_space);

    painter.setPen(color);

    unsigned short i = 0;
    unsigned float bar_value;
    Vector
        position_x1,
        position_y1;
    
    while (i < data.size())
    {
        // Draw in reverse order
        bar_value = data[data.size() - 1 - i];

        // Points of the rectangle
        position_x1 = position * bar_width,
        position_y1 = height();

        painter.drawRect(position_x1, position_y1 - bar_height * bar_value, bar_width, position_y1);
        i++;
    }
}

//  Draws control border
void Histogram::draw_border() const
{
    unsigned float* corners[4] = {{0, 0}, {width()-1, 0}, {width()-1, height()-1}, {0, height()-1}};

    painter.setPen(col_border);
    
    unsigned short i = 0;

    while (i < 4)
    {
        painter.drawLine(corners[i][0], corners[i][1], corners[(i + 1) % 4][0], corners[(i+ 1) % 4][1]);
        i++;
    }
}

//  Draws a scale for the histogram
void Histogram::draw_scale() const
{
    // TODO : this method
} 

//  Draws the control's background
void Histogram::draw_background() const
{
    unsigned float
        bar_width = width() / (float)(data.size()),
        x1,
        x2,
        y1,
        y2;
    unsigned short
        separation_width    = 8,
        offset              = (timer * bar_width) % separation_width,
        num_lines           = 1 + width() / separation_width,
        i                   = 0;

    painter.setPen(col_background);
    
    while (i < num_lines)
    {
        x1 = x2 = width() - offset - i * separation_width;
        y1 = 0;
        y2 = height();

        painter.drawLine(x1, y1, x2, y2);

        i++;
    }
}


//  Draws the histogram, duh !
void Histogram::draw() const
{
    draw_background();
    draw_bars();
    draw_scale();
    draw_border();
}

//  /!\ Qt specific (please don't rename) : is triggered each time the update() method is called.
//  Specifies how the control should draw it
void Histogram::paintEvent(QPaintEvent* event)
{
    painter = QPainter();
    
    // Set antialiasing and draw
    painter.setRenderHint(QPainter::Antialiasing, window->use_antialiasing->isChecked());
    draw();

    painter.end();
}

