# -*- coding: utf-8 -*-
"""
File        :   interface.py
Description :   Manages the displays and main loop.
"""

import lib
import sys
import time

from constants      import *
import track        as __track__

from vector         import Vector
from PyQt4          import QtCore, QtGui, Qt

class Scene(QtGui.QWidget):
    """
    Area where the scene will be drawn.
    """

    def __init__(self, new_window, parent = None):
        """
        Builds the scene.
        """
        QtGui.QWidget.__init__(self, parent)

        self.painter    = None
        self.window     = new_window
        
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding))
        self.setMinimumSize(SCENE_WIDTH, SCENE_HEIGHT)

    def paintEvent(self, event):
        """
        /!\ Qt specific (please don't rename) : is triggered each time the update() method is called.
        Specifies how the control should draw itself.
        """
        self.painter = QtGui.QPainter(self)

        self.painter.setRenderHint(QtGui.QPainter.Antialiasing, self.window.use_antialiasing.isChecked())
        self.painter.fillRect(QtCore.QRectF(QtCore.QPointF(0, 0), QtCore.QPointF(self.width(), self.height())), QtGui.QColor(0, 0, 0))
        self.draw()
        
        self.painter.end()

    def draw(self):
        """
        Draws the complete scene on the screen.
        Dessine la scène entière à l'écran.
        """
        #if __track__.track.picture:
        #    self.screen.blit(__track__.track.picture, (0,0))

        for road in __track__.track.roads:
            self.draw_road(road)
        for roundabout in __track__.track.roundabouts:
            self.draw_roundabout(roundabout)

    def draw_road(self, road):
        """
        Draws a given road on the screen and all the cars on it.
            road (Road) : the aforementioned road.

        Dessine une route donnée à l'écran et toutes les voitures dessus.
            road (Road) : la route sus-citée.
        """
        (start_position, end_position) = (road.begin.position.ceil(), road.end.position.ceil())
        
        #   Draw traffic lights (or not)
        if self.window.exit_lights.isChecked():
            self.draw_traffic_light(end_position, road, EXIT)
        if self.window.entrance_lights.isChecked():
            self.draw_traffic_light(start_position, road, ENTRANCE)
        
        self.painter.setPen(QtGui.QColor(*ROAD_COLOR))
        self.painter.drawLine(start_position.x, start_position.y, end_position.x, end_position.y)
        
        for lane in road.lanes:
            self.draw_lane(lane)

    def draw_lane(self, lane):
        """
        """
        for car in lane.cars:
            self.draw_car(car)
            
    def draw_car(self, car):
        """
        Draws a given car on the screen.
            car (Car) : the aforementioned car.

        Dessine une voiture donnée à l'écran.
            car (Car) : la voiture sus-citée.
        """
        d_position = car.location.begin.position
        a_position = car.location.end.position
        direction  = (a_position - d_position)

        length_covered = float(int(car.position)) / float(int(car.location.parent.length))

        #   Get them once
        (r_width, r_length)    = (car.width, car.length)
        (parallel, orthogonal) = car.location.parent.unit_vectors

        #   Coordinates for the center
        center_position = d_position + direction * length_covered + orthogonal * car.location.width/2

        points = []
        points.append(center_position - parallel * r_length/2 - orthogonal * r_width/2)
        points.append(center_position + parallel * r_length/2 - orthogonal * r_width/2)
        points.append(center_position + parallel * r_length/2 + orthogonal * r_width/2)
        points.append(center_position - parallel * r_length/2 + orthogonal * r_width/2)
        
        polygon = []
        for i in range(len(points)):
            polygon.append(QtCore.QPointF(points[i].x, points[i].y))

        #   Draw the car
        self.painter.setBrush(QtGui.QColor(*car.color))
        self.painter.setPen(QtGui.QColor('black'))
        self.painter.drawPolygon(polygon[0], polygon[1], polygon[2], polygon[3])

    def draw_roundabout(self, roundabout):
        """
        Draws a given roundabout on the screen.
            roundabout (Roundabout) : the aforementioned roundabout.

        Dessine un carrefour donné à l'écran.
            roundabout (Roundabout) : le carrefour sus-cité.
        """
        # TODO :
        #       · (DN1) draw the cars on the roundabout

        if not __track__.track.picture:
            self.painter.setBrush(QtGui.QColor(255, 0, 0))
            self.painter.setPen(QtGui.QColor(*TRANSPARENT))
            self.painter.drawEllipse(roundabout.position.x - roundabout.radius/4, roundabout.position.y - roundabout.radius/4, roundabout.radius/2, roundabout.radius/2)
            pass
        
        #   Selected roudabout
        if self.window.selected_roundabout == roundabout:
            self.painter.setPen(QtGui.QColor(*ROUNDABOUT_COLOR))
            self.painter.setBrush(QtGui.QColor(*TRANSPARENT))
            self.painter.drawEllipse(roundabout.position.x - roundabout.radius, roundabout.position.y - roundabout.radius, 2 * roundabout.radius, 2 * roundabout.radius)

        if roundabout.cars:
            # There are cars on the roundabout, we may want to draw them
            # albeit we can't use draw_car here...

            #TEMPORARY : the number of cars on the roundabout is written
            position = Vector(roundabout.position.x + 10, roundabout.position.y + 10)
            self.painter.setPen(QtGui.QColor(*WHITE))
            self.painter.drawText(position.x, position.y, str(len(roundabout.cars)))
            pass        
        
    def draw_traffic_light(self, position, road, gate):
        """
        Draws a traffic light...
            x, y : coordinates
            road : the road
            gate : 1 or 0, the gate
        """

        TF_RADIUS = 3
        width     = 0
        state     = road.traffic_lights[gate]

        (parallel, orthogonal)  = road.unit_vectors
        start_position          = position + orthogonal * 6 - parallel * 12
        d_position              = Vector(0, -1) * TF_RADIUS * 2

        for i in range(3):
            if (state) and (i == 0):
                self.painter.setBrush(QtGui.QColor('green'))
            elif (not state) and (i == 2):
                self.painter.setBrush(QtGui.QColor('red'))
            else:
                self.painter.setBrush(QtGui.QColor('black'))

            position = start_position + d_position * i
            self.painter.setPen(QtGui.QColor(*GREY))
            self.painter.drawEllipse(position.x - TF_RADIUS, position.y - TF_RADIUS, 2 * TF_RADIUS, 2*TF_RADIUS)
            
    def mousePressEvent(self, event):
        """
        /!\ Qt specific (please don't rename)
        Manages what happens when a mouse button is pressed
        """
        # Experimental : select a roundabout or a car
        self.window.select_car(event.x(), event.y())
        self.window.select_roundabout(event.x(), event.y())

class MainWindow(QtGui.QMainWindow):
    """
    
    """

    def __init__(self, parent = None):
        """
        Builds the main window.
        """
        QtGui.QMainWindow.__init__(self, parent)

        #   Set parameters
        self.elapsed_time           = 0
        self.last_update            = time.clock()
        self.selected_car           = None
        self.selected_roundabout    = None
        self.is_playing             = True
        
        #   Set the interface
        self.setup_interface()
        
        #   Start the timer
        self.timer = QtCore.QBasicTimer()
        self.timer.start(10, self)

    def setup_interface(self):
        """
        Sets up the Qt interface, layout, slots & properties
        """
        #   Window settings
        self.setObjectName('MainWindow')

        screen = QtGui.QDesktopWidget().screenGeometry()
        self.resize(screen.width(), screen.height())

        self.setWindowTitle(REVISION_NAME + ' - r' + str(REVISION_NUMBER))
        self.setWindowIcon(QtGui.QIcon('icons/tinr_logo.png'))
        self.statusBar().showMessage('Ready')

        self.setCentralWidget(QtGui.QWidget())
        
        #   Exit action
        act_exit = QtGui.QAction(QtGui.QIcon('icons/exit.png'), 'Exit', self)
        act_exit.setShortcut('Ctrl+Q')
        act_exit.setStatusTip('Exit application')
        self.connect(act_exit, QtCore.SIGNAL('triggered()'), QtCore.SLOT('close()'))
        
        #   Play action
        act_play = QtGui.QAction(QtGui.QIcon('icons/play.png'), 'Play', self)
        #act_play.setShortcut('Ctrl+P')
        act_play.setStatusTip('Play simulation')
        self.connect(act_play, QtCore.SIGNAL('triggered()'), self.play_simulation)

        #   Pause action
        act_pause = QtGui.QAction(QtGui.QIcon('icons/pause.png'), 'Pause', self)
        #act_pause.setShortcut('Ctrl+P')
        act_pause.setStatusTip('Pause simulation')
        self.connect(act_pause, QtCore.SIGNAL('triggered()'), self.pause_simulation)

        #   Reset action
        act_reset = QtGui.QAction(QtGui.QIcon('icons/reset.png'), 'Reset', self)
        #act_reset.setShortcut('Ctrl+R')
        act_reset.setStatusTip('Reset simulation')
        self.connect(act_reset, QtCore.SIGNAL('triggered()'), self.reset_simulation)

        #   Menu
        menu_bar = self.menuBar()
        
        #   File menu
        file = menu_bar.addMenu('&File')
        file.addAction(act_exit)

        #   Simulation menu
        simulation = menu_bar.addMenu('&Simulation')
        simulation.addAction(act_play)
        simulation.addAction(act_pause)
        simulation.addAction(act_reset)

        #   Toolbar
        main_toolbar = self.addToolBar('Main toolbar')
        main_toolbar.addAction(act_play)
        main_toolbar.addAction(act_pause)
        main_toolbar.addAction(act_reset)

        #   Scene
        self.scene = Scene(self)
        self.scene.setObjectName('scene')     

        #   Information box
        self.lbl_info = QtGui.QLabel('<i>Information</i>')
        self.lbl_info.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.lbl_info.setWordWrap(True)
        self.lbl_info.setObjectName('lbl_info')
        
        lay_info = QtGui.QVBoxLayout()
        lay_info.addWidget(self.lbl_info)

        self.box_info = QtGui.QGroupBox('Information')
        self.box_info.setObjectName('box_info')
        self.box_info.setLayout(lay_info)        
    
        #   Commands box
        self.entrance_lights = QtGui.QCheckBox('Display entrance traffic lights')
        self.entrance_lights.setObjectName('entrance_lights')
        self.entrance_lights.setChecked(False)
        
        self.exit_lights = QtGui.QCheckBox('Display exit traffic lights')
        self.exit_lights.setObjectName('exit_lights')
        self.exit_lights.setChecked(True)
        
        self.use_antialiasing = QtGui.QCheckBox('Use antialiasing')
        self.use_antialiasing.setObjectName('use_antialiasing')
        self.use_antialiasing.setChecked(False)

        self.display_density = QtGui.QCheckBox('Display density')
        self.display_density.setObjectName('display_density')
        self.display_density.setChecked(False)

        lbl_spawn_delay = QtGui.QLabel('Spawn delay')
        self.spawn_delay = QtGui.QSpinBox()
        self.spawn_delay.setSingleStep(100)
        self.spawn_delay.setRange(1000, 30000)
        self.spawn_delay.setSuffix('ms')
        self.spawn_delay.setValue(SPAWN_TIME * 1000.0)

        lay_commands = QtGui.QGridLayout()
        lay_commands.addWidget(self.entrance_lights, 0, 0, 1, 2)
        lay_commands.addWidget(self.exit_lights, 1, 0, 1, 2)
        lay_commands.addWidget(self.use_antialiasing, 2, 0, 1, 2)
        lay_commands.addWidget(self.display_density, 3, 0, 1, 2)
        lay_commands.addWidget(lbl_spawn_delay, 4, 0)
        lay_commands.addWidget(self.spawn_delay, 4, 1)
        
        self.box_commands = QtGui.QGroupBox('Commands')
        self.box_commands.setObjectName('box_commands')
        self.box_commands.setLayout(lay_commands)
        
        #   Control panel
        lay_panel = QtGui.QVBoxLayout()
        lay_panel.addWidget(self.box_info)
        lay_panel.addStretch(1)
        lay_panel.addWidget(self.box_commands)
        
        self.panel = QtGui.QFrame()
        self.panel.setObjectName('panel')
        self.panel.setLayout(lay_panel)

        #self.control_panel.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Expanding))
        #self.control_panel.setMinimumSize(PANEL_WIDTH, PANEL_HEIGHT)
        #self.control_panel.setTabPosition(QtGui.QTabWidget.East)
        #self.control_panel.addTab(self.tab_info, 'Informations')
        #self.control_panel.addTab(self.tab_commands, 'Commands')
        #self.control_panel.setCurrentIndex(0)
        
        QtCore.QMetaObject.connectSlotsByName(self)

        #   Display
        lay_window = QtGui.QGridLayout()
        lay_window.addWidget(self.scene, 0, 0)
        lay_window.addWidget(self.panel, 0, 1)

        self.centralWidget().setLayout(lay_window)
    
    #   If you find another way to implement the equivalent of the following 2 slots, please just change it ! -- Ch@hine
    def play_simulation(self):
        """

        """
        self.is_playing = True

    def pause_simulation(self):
        """

        """
        self.is_playing = False

    def reset_simulation(self):
        """

        """
        pass

    def closeEvent(self, event):
        """
        /!\ Qt specific (please don't rename)
        Specifies what has to be done when exiting the application.
        """
        event.accept()
        exit()
    
    def keyPressEvent(self, event):
        """
        /!\ Qt specific (please don't rename)
        Manages keyboard events
        """
        if event.key() == QtCore.Qt.Key_Escape:
            exit()
            
    def select_roundabout(self, x, y):
        """
        Selects the roundabout placed on x, y
        Deselects if there is none
        """
        click_position = Vector(x, y)
        
        self.selected_roundabout = None
        
        for roundabout in __track__.track.roundabouts:
            if abs(roundabout.position - click_position) < roundabout.radius:
                self.selected_roundabout = roundabout
                break
    
    def select_car(self, x, y):
        """
        Selects the car placed on x, y.
        Deselects if there is none.
        """
        click_position = Vector(x, y)

        self.selected_car = None

        for road in __track__.track.roads:
            for lane in road.lanes:
                for car in lane.cars:
                    car_position = road.begin.position + (road.end.position - road.begin.position).normalize() * car.position
                    if abs(car_position - click_position) < 20:
                        self.selected_car = car
                        break

    def timerEvent(self, event):
        """
        /!\ Qt specific (please don't rename)
        Passes or uses timer events to update the simulation
        """
        if event.timerId() == self.timer.timerId():
            self.elapsed_time = time.clock() - self.last_update
            self.last_update = time.clock()
            
            if self.is_playing:
                self.update_simulation()
                self.update_information()
                self.scene.update()
            
        else:
            QtGui.QFrame.timerEvent(self, event)

    def update_simulation(self):
        """
        Updates the simulation.
        """
        #   Run the simulation for delta_t
        for road in __track__.track.roads:
            road.update(self.elapsed_time)
        for roundabout in __track__.track.roundabouts:
            #oui deux boucles séparées sinon linfo est pas en temps réél (enfin ca serait pas un drame non plus vu l'échelle de delta_t ! )
            roundabout.get_local_load()
        for roundabout in __track__.track.roundabouts:
            roundabout.update(self.elapsed_time)
        
    def update_information(self):
        """
        Displays informations on the simulation and selected objects
        """
        information = ''
        
        information += '<b>Roads : </b>'        + str(len(__track__.track.roads))       + '<br/>'
        information += '<b>Roundabouts : </b>'  + str(len(__track__.track.roundabouts)) + '<br/>'

        cars_on_roads = 0
        cars_waiting  = 0
        cars_on_roundabouts = 0
        
        for road in __track__.track.roads:
            cars_on_roads += road.total_cars
            cars_waiting  += road.total_waiting_cars
        for roundabout in __track__.track.roundabouts:
            cars_on_roundabouts += len(roundabout.cars)

        total_cars = cars_on_roads + cars_on_roundabouts
        
        information += '<b>Cars</b> (total) : ' + str(total_cars)           + '<br/>'
        information += '(on roads) : '          + str(cars_on_roads)        + '<br/>'
        information += '(on roundabouts) : '    + str(cars_on_roundabouts)  + '<br/>'
        information += '(waiting) : '           + str(cars_waiting)
        
        if self.selected_roundabout is not None:
            information += '<br/><br/><b>Selected roundabout :</b><br/>'
            information += 'position : (' + str(self.selected_roundabout.position.x) + ',' + str(self.selected_roundabout.position.y) + ') <br/>'
            information += 'radius : ' + str(self.selected_roundabout.radius) + '<br/>'
            information += 'cars : ' + str(len(self.selected_roundabout.cars)) + '<br/>'
            information += 'load : ' + str(lib.round(self.selected_roundabout.global_load, 2)) + '<br/>'
            if self.selected_roundabout.spawning:
                information += '<b>Spawning mode<b><br/>'
            if len(self.selected_roundabout.leaving_roads) == 0:
                information += '<b>Destroying mode<b><br/>'
            if self.selected_roundabout.cars:
                avg_waiting_time = 0
                for car in self.selected_roundabout.cars:
                    avg_waiting_time += car.total_waiting_time / float(len(self.selected_roundabout.cars))
                information += '<br/><b>Average waiting time</b> (s) : ' + str(lib.round(avg_waiting_time,2)) + '<br/>'
        
        if lib.Delta_t != 0:
            information += '<br/><b>Simulation</b><br/>'
            information += 'FPS : ' + str(lib.round(1/lib.Delta_t, 2)) + '<br/>'
            information += '&Delta;t (s): ' + str(lib.round(lib.Delta_t, 2)) + '<br/>'
        
        self.lbl_info.setText(information)

def main(args):

    app = QtGui.QApplication(args)
    
    main_window = MainWindow()
    main_window.showMaximized()

    sys.exit(app.exec_())
        
# Bootstrap
if __name__ == "__main__":
    main(sys.argv)

# Don't write anything after that !
