# -*- coding: utf-8 -*-
"""
File        :   interface.py
Description :   Manages the displays and main loop.
"""

import constants    as __constants__
import init         as init
from vector         import Vector

import sys
from PyQt4          import QtCore, QtGui, Qt

class win_control(QtGui.QMainWindow):
    def __init__(self, parent = None):
        #   Call parent constructor
        QtGui.QWidget.__init__(self, parent)
        
        #   Set the window
        #self.resize(__constants__.PANEL_WIDTH, __constants__.PANEL_HEIGHT) # (width, height)
        #self.center()
        self.setWindowTitle('Contrôle')
        self.setWindowIcon(QtGui.QIcon('icons/window.png'))
        
        #   Exit action
        self.act_exit = QtGui.QAction(QtGui.QIcon('icons/exit.png'), 'Exit', self)
        self.act_exit.setShortcut('Ctrl+Q')
        self.act_exit.setStatusTip('Exit application')
        self.connect(self.act_exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        
        #   Status bar
        self.statusBar().showMessage('Ready')

        #   Menu bar
        menu_bar = self.menuBar()
        file = menu_bar.addMenu('&File')
        file.addAction(self.act_exit)
        
        #   Toolbar
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(self.act_exit)

        #   Labels
        lbl_total_roundabouts   = QtGui.QLabel('Total roundabouts :')
        lbl_total_roads         = QtGui.QLabel('Total roads :')
        lbl_total_cars          = QtGui.QLabel('Total cars :')
        lbl_cars_on_roads       = QtGui.QLabel('Cars on roads :')
        lbl_cars_on_roundabouts = QtGui.QLabel('Cars on roundabouts :')
        lbl_cars_waiting        = QtGui.QLabel("Cars waiting :")

        #   Statistics fields
        self.total_roundabouts      = QtGui.QSpinBox()
        self.total_roundabouts.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        
        self.total_roads            = QtGui.QSpinBox()
        self.total_roads.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)

        self.total_cars             = QtGui.QSpinBox()
        self.total_cars.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)

        self.cars_on_roundabouts    = QtGui.QSpinBox()
        self.cars_on_roundabouts.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)

        self.cars_on_roads          = QtGui.QSpinBox()
        self.cars_on_roads.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)

        self.cars_waiting           = QtGui.QSpinBox()
        self.cars_waiting.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)

        #   Options boxes
        self.entrance_lights        = QtGui.QCheckBox("Display entrance lights")
        #self.entrance_lights.setCheckState(QtGui.QCheckBox.Unchecked)

        self.exit_lights            = QtGui.QCheckBox("Display exit lights")
        self.exit_lights.setCheckState(2)

        self.roundabouts_indices    = QtGui.QCheckBox("Display roundabouts indices")
        #self.roundabouts_indices.setCheckState(QtGui.QCheckBox.Unchecked)
        
        #   Statistics panel
        lay_stats = QtGui.QGridLayout()
        
        lay_stats.addWidget(lbl_total_roundabouts, 0, 0)
        lay_stats.addWidget(self.total_roundabouts, 0, 1)
        
        lay_stats.addWidget(lbl_total_roads, 1, 0)
        lay_stats.addWidget(self.total_roads, 1, 1)
        
        lay_stats.addWidget(lbl_total_cars, 2, 0)
        lay_stats.addWidget(self.total_cars, 2, 1)

        lay_stats.addWidget(lbl_cars_on_roundabouts, 3, 0)
        lay_stats.addWidget(self.cars_on_roundabouts, 3, 1)

        lay_stats.addWidget(lbl_cars_on_roads, 4, 0)
        lay_stats.addWidget(self.cars_on_roads, 4, 1)
        
        lay_stats.addWidget(lbl_cars_waiting, 5, 0)
        lay_stats.addWidget(self.cars_waiting, 5, 1)
        
        stats = QtGui.QGroupBox("Statistics", self)
        stats.setLayout(lay_stats)
        
        #   Options panel
        lay_options = QtGui.QVBoxLayout()
        
        lay_options.addWidget(self.entrance_lights)
        lay_options.addWidget(self.exit_lights)
        lay_options.addWidget(self.roundabouts_indices)

        options = QtGui.QGroupBox("Options", self)
        options.setLayout(lay_options)

        #   Main grid
        grid = QtGui.QGridLayout()
        grid.addWidget(stats, 0, 0)
        grid.addWidget(options, 1, 0)

        central_widget = QtGui.QWidget()
        central_widget.setLayout(grid)
        self.setCentralWidget(central_widget)
        
    def center(self):
        """
        Centers the window in the screen.
        """
        screen  = QtGui.QDesktopWidget().screenGeometry()
        size    =  self.geometry()
        self.move((screen.width() - size.width())/2, (screen.height() - size.height())/2)

    def keyPressEvent(self, event):
        """
        Manages the keyboard events ; the name of the function is set by Qt, so don't change it.
        """
        if event.key() == QtCore.Qt.Key_Escape:
            exit()

    def draw_roundabout(self, roundabout):
        """
        Draws a given roundabout on the screen.
            roundabout (Roundabout) : the aforementioned roundabout.

        Dessine un carrefour donné à l'écran.
            roundabout (Roundabout) : le carrefour sus-cité.
        """
        # TODO :
        #       · (DN1) draw the cars on the roundabout

#        if not init.track.picture:
#            pygame.draw.circle(self.screen, __constants__.ROUNDABOUT_COLOR, roundabout.position.ceil().get_tuple(), __constants__.ROUNDABOUT_WIDTH)

        if roundabout.cars:
            # There are cars on the roundabout, we may want to draw them
            # albeit we can't use draw_car here...

            #TEMPORARY : the number of cars on the roundabout is written
            position = Vector(roundabout.position.x + 10, roundabout.position.y + 10)
            self.draw_text(position, str(len(roundabout.cars)))
            pass

    def closeEvent(self, event):
        """
        Specifies what has to be done when exiting the application ; this function is automatically called by Qt as soon as the user clicks on the close button (at the top right of the window), that's why you mustn't change its name !
        """
        event.ignore()
    
class win_draw_surface(QtGui.QMainWindow):
    def __init__(self, control_panel = None, parent = None):
        QtGui.QWidget.__init__(self, parent)

        self.resize(__constants__.WINDOW_WIDTH,__constants__.WINDOW_HEIGHT)
        self.setWindowTitle(__constants__.REVISION_NAME + ' - r' + str(__constants__.REVISION_NUMBER))
        self.setWindowIcon(QtGui.QIcon('icons/tinr_logo.png'))

        self.cpanel = control_panel       
        self.cpanel.show()
        
        self.timer = QtCore.QBasicTimer()
        self.timer.start(10, self)

    def closeEvent(self, event):
        """
        Specifies what has to be done when exiting the application ; this function is automatically called by Qt as soon as the user clicks on the close button (at the top right of the window), that's why you mustn't change its name !
        """
        event.accept()
        exit()
    
    def keyPressEvent(self, event):
        """
        Manages the keyboard events ; the name of the function is set by Qt, so don't change it.
        """
        if event.key() == QtCore.Qt.Key_Escape:
            exit()
        
    def paintEvent(self, event):
        """
        Specifies how the control should draw itself
        """
        
        painter = QtGui.QPainter(self)
        
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        self.draw_scene(painter)
        
        painter.end()

    def draw_scene(self, painter):
        """
        Draws the complete scene on the screen.
        Dessine la scène entière à l'écran.
        """

        #if init.track.picture:
        #    self.screen.blit(init.track.picture, (0,0))

        for road in init.track.roads:
            self.draw_road(painter, road)
        #for roundabout in init.track.roundabouts:
            #self.draw_roundabout(painter, roundabout)

    def draw_road(self, painter, road):
        """
        Draws a given road on the screen and all the cars on it.
            road (Road) : the aforementioned road.

        Dessine une route donnée à l'écran et toutes les voitures dessus.
            road (Road) : la route sus-citée.
        """

        (start_position, end_position) = (road.begin.position.ceil(), road.end.position.ceil())

        # This is not perfect... but it's ok for now I guess -- Sharayanan
        if self.cpanel.exit_lights.isChecked():
            self.draw_traffic_light(painter, end_position, road, __constants__.LEAVING_GATE)
        if self.cpanel.entrance_lights.isChecked():
            self.draw_traffic_light(painter, start_position, road, __constants__.INCOMING_GATE)

        color = __constants__.GREEN
        key = 0
        if road.cars and __constants__.DISPLAY_DENSITY:
            occupation = 0
            for car in road.cars:
                occupation += car.length

            key = 2 * (float(occupation)/float(road.length)) * 255
            if key > 255: key = 255
            color = [key, 255 - key, 0]

#        if not init.track.picture:
        painter.drawLine(start_position.x, start_position.y, end_position.x, end_position.y)

        if road.cars and key < 200:
            # Do not draw cars when density exceeds ~80%
            for car in road.cars:
                self.draw_car(painter, car)

    def draw_car(self, painter, car):
        """
        Draws a given car on the screen.
            car (Car) : the aforementioned car.

        Dessine une voiture donnée à l'écran.
            car (Car) : la voiture sus-citée.
        """
        d_position = car.location.begin.position
        a_position = car.location.end.position
        direction  = (a_position - d_position)

        length_covered = float(int(car.position)) / float(int(car.location.length))

        # Get them once
        (r_width, r_length)    = (car.width, car.length)
        (parallel, orthogonal) = car.location.unit_vectors

        # Coordinates for the center
        center_position = d_position + direction * length_covered + orthogonal * car.location.width/2

        point = []
        point.append(center_position - parallel * r_length/2 - orthogonal * r_width/2)
        point.append(center_position + parallel * r_length/2 - orthogonal * r_width/2)
        point.append(center_position + parallel * r_length/2 + orthogonal * r_width/2)
        point.append(center_position - parallel * r_length/2 + orthogonal * r_width/2)
        
        polygon = []
        for i in range(len(point)):
            polygon.append(QtCore.QPointF(point[i].x, point[i].y))

        color = car.color
        # Draw the car
        painter.setBrush(QtGui.QColor('blue'))
        painter.setPen(  QtGui.QColor('black'))
        painter.drawPolygon(polygon[0], polygon[1], polygon[2], polygon[3])

    def draw_traffic_light(self, painter, position, road, gate):
        """
        Draws a traffic light...
            x, y : coordinates
            road : the road
            gate : 1 or 0, the gate
        """

        TF_RADIUS = 3
        width     = 0
        state     = road.gates[gate]

        (parallel, orthogonal) = road.unit_vectors
        start_position  = position + orthogonal * 6 - parallel * 12
        d_position      = Vector(0, -1) * TF_RADIUS * 2

        for i in range(3):
            if (state) and (i == 0):
                painter.setBrush(QtGui.QColor('green'))
            elif (not state) and (i == 2):
                painter.setBrush(QtGui.QColor('red'))
            else:
                painter.setBrush(QtGui.QColor('black'))

            position = start_position + d_position * i
            painter.drawEllipse(position.x - TF_RADIUS, position.y - TF_RADIUS, 2 * TF_RADIUS, 2*TF_RADIUS)
        
    def timerEvent(self, event):
        """
        Passes or uses timer events to update the simulation
        """
        if event.timerId() == self.timer.timerId():
            self.update_simulation()
            self.update()
            self.cpanel.update()
        else:
            QtGui.QFrame.timerEvent(self, event)

    def update_simulation(self):
        """
        Updates the simulation.
        """
        
        #   Run the simulation for delta_t
        for road in init.track.roads:
            road.update()
        for roundabout in init.track.roundabouts:
            roundabout.update()

        #   Update the information
        self.cpanel.total_roads.setValue(len(init.track.roads))
        self.cpanel.total_roundabouts.setValue(len(init.track.roundabouts))

        self.cpanel.cars_on_roads.setValue(0)
        self.cpanel.cars_on_roundabouts.setValue(0)
        self.cpanel.cars_waiting.setValue(0)

        for road in init.track.roads:
            self.cpanel.cars_on_roads.setValue(self.cpanel.cars_on_roads.value() + len(road.cars))
            self.cpanel.cars_waiting.setValue(self.cpanel.cars_waiting.value() + road.total_waiting_cars)
        for roundabout in init.track.roundabouts:
            self.cpanel.cars_on_roundabouts.setValue(self.cpanel.cars_on_roundabouts.value() + len(roundabout.cars))

        self.cpanel.total_cars.setValue(self.cpanel.cars_on_roads.value() + self.cpanel.cars_on_roundabouts.value())            

def main(args):
    app = QtGui.QApplication(args)
    
    panel = win_control()
    draw_surface = win_draw_surface(panel)
    draw_surface.show() 

    sys.exit(app.exec_())
        
# Bootstrap
if __name__ == "__main__":
    main(sys.argv)
# Don't write anything after that !