# -*- coding: utf-8 -*-
"""
File        :   interface.py
Description :   Manages the displays and main loop.
"""

import lib
import sys

from constants      import *
import road         as __road__
import track        as __track__

from vector         import Vector
from PyQt4          import QtCore, QtGui, Qt

class Histogram(QtGui.QWidget):
    """
    Histogram handling & drawing 
    """
    
    def __init__(self, new_window, parent = None, 
                 span = HISTOGRAM_SPAN, color = HISTOGRAM_COLOR, 
                 width = HISTOGRAM_WIDTH, height = HISTOGRAM_HEIGHT):
        """
        Initializes histogram representation
            span : the period of time to be taken into account
            width, height : dimensions
        """
        QtGui.QWidget.__init__(self, parent)
        
        self.window  = new_window
        self.painter = None
        
        # Prepare an array of empty data
        self.data = [0.0 for instant in range(span)]
        self.max  = 0.0
        self.min  = 0.0
        
        # Colors
        self.color        = color
        self.border_color = GREY
        self.back_color   = BLACK
        
        # Keep track of time
        self.timer = 0
        
        self.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed))
        self.setMinimumSize(width, height)
        
    def append(self, value):
        """
        Appends an event to the histogram
        """
        # Shift data and replace the first element
        self.data = lib.shift_list(self.data)
        self.data[0] = value
        self.timer += 1
        
        # Keep track of the extremes
        if value > self.max: self.max = value
        if value < self.min: self.min = value

    def _draw_bars(self):
        """
        Draw the histobars
        """
        
        if self.max == 0:
            # Don't draw when there is no data to plot
            return None 
        
        # Keep 20% of free space
        extra_space = 0.2 * self.max
        
        # Height and width for a unit bar
        bar_width = self.width() / float(len(self.data))
        bar_height = self.height() / float(self.max + extra_space)

        self.painter.setPen(QtGui.QColor(*self.color))
        
        for position in range(len(self.data)):
            # Draw in reverse order
            bar_value = self.data[ - 1 - position ]
            
            # Points of the rectangle
            position_x1 = position * bar_width
            position_y1 = self.height()
            self.painter.drawRect(position_x1, position_y1 - bar_height * bar_value, bar_width, position_y1)
        
    def _draw_border(self):
        """
        Draws control border
        """
        
        corners = [[0, 0], [self.width()-1, 0], [self.width()-1, self.height()-1], [0, self.height()-1]]
        
        self.painter.setPen(QtGui.QColor(*self.border_color))
        
        for num_corner in range(len(corners)):
            self.painter.drawLine(corners[num_corner][0], corners[num_corner][1],
                                  corners[(num_corner + 1) % len(corners)][0], corners[(num_corner+ 1) % len(corners)][1])
        
    def _draw_scale(self):
        """
        Draws a scale for the histogram
        """
        # TODO : this method
        pass 
        
    def _draw_background(self):
        """
        Draws the control's background
        """
        
        separation_width = 8
        
        bar_width = self.width() / float(len(self.data))
        
        offset = (self.timer * bar_width) % separation_width
        num_lines = 1 + self.width() / separation_width
        
        self.painter.setPen(QtGui.QColor(*self.back_color))
        
        for i in range(num_lines):
            x1 = x2 = self.width() - offset - i * separation_width
            y1, y2 = 0, self.height()
            
            self.painter.drawLine(x1, y1, x2, y2)
        
    def draw(self):
        """
        Draws the histogram, duh !
        """
        
        self._draw_background()
        self._draw_bars()
        self._draw_scale()
        self._draw_border()
        
    def paintEvent(self, event):
        """
        /!\ Qt specific (please don't rename) : is triggered each time the update() method is called.
        Specifies how the control should draw itself.
        """
        self.painter = QtGui.QPainter(self)

        # Set antialiasing and draw
        self.painter.setRenderHint(QtGui.QPainter.Antialiasing, self.window.use_antialiasing.isChecked())
        self.draw()
        
        self.painter.end()
        
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

        # Set antialiasing
        self.painter.setRenderHint(QtGui.QPainter.Antialiasing, self.window.use_antialiasing.isChecked())
        
        # Draw background color and scene
        self.painter.fillRect(QtCore.QRectF(QtCore.QPointF(0, 0), QtCore.QPointF(self.width(), self.height())), QtGui.QColor(*BLACK))
        self.draw()
        
        self.painter.end()

    def draw(self):
        """
        Draws the complete scene on the screen.
        Dessine la scène entière à l'écran.
        """

        # Draw the roads
        for road in __track__.track.roads:
            self.draw_road(road)
            
        # Draw the roundabouts
        for roundabout in __track__.track.roundabouts:
            self.draw_roundabout(roundabout)

        # Manage selections
        self.draw_selected_path()
        
    def draw_road(self, road):
        """
        Draws a given road on the screen and all the cars on it.
            road (Road) : the aforementioned road.

        Dessine une route donnée à l'écran et toutes les voitures dessus.
            road (Road) : la route sus-citée.
        """
        (start_position, end_position) = (road.start.position.ceil(), road.end.position.ceil())
        
        #   Draw traffic lights (or not)
        if self.window.exit_lights.isChecked():
            self.draw_traffic_light(end_position, road, EXIT)
        if self.window.entrance_lights.isChecked():
            self.draw_traffic_light(start_position, road, ENTRANCE)
        
        # Draw a line to represent the road
        self.painter.setPen(QtGui.QColor(*ROAD_COLOR))
        self.painter.drawLine(start_position.x, start_position.y, end_position.x, end_position.y)
        
        # Draw lanes individually
        for lane in road.lanes:
            self.draw_lane(lane)

    def draw_selected_path(self):
        """
        When a car is selected, draw its path
        """
        selected_car = self.window.selected_car
        if selected_car is not None:
            if isinstance(selected_car.location, __road__.Lane):
                current_road        = selected_car.road
                car_position        = current_road.start.position + current_road.parallel * selected_car.length_covered
                
                self.painter.setPen(QtGui.QColor(*BLUE))
                self.painter.drawLine(car_position.x,              car_position.y,
                                      current_road.end.position.x, current_road.end.position.y)
            else:
                current_road = selected_car.location.incoming_roads[0]

            if not (selected_car.path is None):
                for next_way in selected_car.path:
                    if not (next_way is None):
                        current_road = current_road.end.leaving_roads[next_way]
                            
                        self.painter.drawLine(current_road.start.position.x, current_road.start.position.y,
                                              current_road.end.position.x,   current_road.end.position.y)
            
    def draw_lane(self, lane):
        """
        Draws a lane and all the cars on it
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

        if car.road is None:
            return None

        #   Get them once
        (r_width, r_length)    = (car.width, car.length)
        (parallel, orthogonal) = car.road.unit_vectors

        #   Coordinates for the center
        center_position = car.position

        # The cars are rectangles whose sides are parallel and perpendicular to the road
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
        
        #   Selected car : draw selection circle
        if self.window.selected_car == car:
            self.painter.setPen(QtGui.QColor(*ROUNDABOUT_COLOR))
            self.painter.setBrush(QtGui.QColor(*TRANSPARENT))
            self.painter.drawEllipse(car.position.x - car.length, car.position.y - car.length, 2*car.length, 2*car.length)

    def draw_roundabout(self, roundabout):
        """
        Draws a given roundabout on the screen.
            roundabout (Roundabout) : the aforementioned roundabout.

        Dessine un carrefour donné à l'écran.
            roundabout (Roundabout) : le carrefour sus-cité.
        """
        # TODO :
        #       · (DN1) draw the cars on the roundabout

        # Draw a red circle to represent a roundabout
        if not __track__.track.picture:
            self.painter.setBrush(QtGui.QColor(*RED))
            self.painter.setPen(QtGui.QColor(*TRANSPARENT))
            self.painter.drawEllipse(roundabout.position.x - roundabout.radius/4, roundabout.position.y - roundabout.radius/4, roundabout.radius/2, roundabout.radius/2)
            pass
        
        #   Selected roudabout : draw selection circle
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
            gate : EXIT (1) or ENTRANCE (1)
        """

        TF_RADIUS = 3 # Radius of a light bulb
        state     = road.traffic_lights[gate]

        (parallel, orthogonal)  = road.unit_vectors
        start_position          = position + orthogonal * 6 - parallel * 12
        d_position              = Vector(0, -1) * TF_RADIUS * 2
        
        colors = [BLACK for i in range(3)]
        
        if state:     colors[0] = GREEN
        if not state: colors[2] = RED
        # if ... : color[1] = ORANGE

        for i in range(3):
            self.painter.setBrush(QtGui.QColor(*colors[i]))

            position = start_position + d_position * i
            self.painter.setPen(QtGui.QColor(*GREY))
            self.painter.drawEllipse(position.x - TF_RADIUS, position.y - TF_RADIUS, 2 * TF_RADIUS, 2*TF_RADIUS)
            
    def mousePressEvent(self, event):
        """
        /!\ Qt specific (please don't rename)
        Manages what happens when a mouse button is pressed
        """
        # Experimental : select a roundabout or a car
        #
        # TODO : 
        #   · (mPE.1) : avoid double selections (car + roundabout)
        
        self.window.select_car(event.x(), event.y())
        self.window.select_roundabout(event.x(), event.y())

class MainWindow(QtGui.QMainWindow):
    """
    The main window that encapsulates the scene and controls
    """

    def __init__(self, parent = None):
        """
        Builds the main window.
        """
        QtGui.QMainWindow.__init__(self, parent)

        #   Set parameters
        lib.delta_t                 = 0
        self.last_update            = lib.clock()
        self.selected_car           = None
        self.selected_roundabout    = None
        
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
        
        #   Fast forward action
        act_fastforward = QtGui.QAction(QtGui.QIcon('icons/forward.png'), 'Fast forward', self)
        act_fastforward.setStatusTip('Fast forward simulation (x2 - x4 - x8)')
        self.connect(act_fastforward, QtCore.SIGNAL('triggered()'), self.fastforward_simulation)

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
        simulation.addAction(act_fastforward)
        simulation.addAction(act_reset)

        #   Toolbar
        main_toolbar = self.addToolBar('Main toolbar')
        main_toolbar.addAction(act_play)
        main_toolbar.addAction(act_pause)
        main_toolbar.addAction(act_fastforward)
        main_toolbar.addAction(act_reset)
        
        #   Scene
        self.scene = Scene(self)
        self.scene.setObjectName('scene')     
        
        # Histogram
        self.histogram = Histogram(self)
        self.histogram.setObjectName('histogram')

        #   Information box
        self.lbl_info = QtGui.QLabel('<i>Information</i>')
        self.lbl_info.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.lbl_info.setWordWrap(True)
        self.lbl_info.setObjectName('lbl_info')
        
        lay_info = QtGui.QVBoxLayout()
        lay_info.addWidget(self.lbl_info)
        lay_info.addWidget(self.histogram)

        self.box_info = QtGui.QGroupBox('Informations')
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
        lib.set_speed (1.0)

    def pause_simulation(self):
        """

        """
        lib.set_speed(0.0)

    def reset_simulation(self):
        """

        """
        pass
        
    def fastforward_simulation(self):
        """
        Plays the simulation at 2, 4 or 8×
        """
        sim_speed = lib.get_speed()
        
        if sim_speed == 2:
            lib.set_speed(4)
        elif sim_speed == 4:
            lib.set_speed(8)
        elif sim_speed == 8:
            lib.set_speed(1)
        else:
            lib.set_speed(2)

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
        click_position   = Vector(x, y)
        selection_radius = 20

        self.selected_car = None

        for road in __track__.track.roads:
            for lane in road.lanes:
                for car in lane.cars:
                    car_position = road.start.position  + road.parallel * car.length_covered
                    if abs(car_position - click_position) < selection_radius:
                        self.selected_car = car
                        break

    def timerEvent(self, event):
        """
        /!\ Qt specific (please don't rename)
        Passes or uses timer events to update the simulation
        """
        if event.timerId() == self.timer.timerId():
            # Manage internal time events
            lib.delta_t = lib.clock() - self.last_update
            self.last_update = lib.clock()
            
            # Update the simulation and informations
            self.update_simulation()
            self.update_information()
            self.histogram.update()
            self.scene.update()
            
        else:
            QtGui.QFrame.timerEvent(self, event)

    def update_simulation(self):
        """
        Updates the simulation.
        """
        # Update the roads (and the cars)
        for road in __track__.track.roads:
            road.update()
            
        # Get informations from the roundabouts (separate loop)
        for roundabout in __track__.track.roundabouts:
            roundabout.get_local_load()
            
        # Update the roundabouts
        for roundabout in __track__.track.roundabouts:
            roundabout.update()
        
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
        information += '(waiting) : '           + str(cars_waiting)         + '<br/>'
        
        information += self.selected_roundabout_informations()
        information += self.selected_car_informations()
        information += self.simulation_informations()         
        
        self.lbl_info.setText(information)
        self.histogram.append(total_cars)

    def simulation_informations(self):
        """
        """
        information = '<br/><b>Simulation</b><br/>'        
        
        hours, minutes, seconds = lib.get_simulation_time()
        
        information += 'Time elapsed : ' + str(hours) + '<sup>h</sup>&nbsp;' + str(minutes) + '<sup>m</sup>&nbsp;' + str(seconds) + '<sup>s</sup><br/>'
        information += 'Speed : &times;' + str(lib.round(lib.get_speed(), 2))   + '<br/>'
        
        if lib.delta_t != 0:
            information += 'FPS : ' + str(lib.round(lib.get_speed()/lib.delta_t, 2)) + '<br/>'
            information += '&Delta;t (s) : ' + str(lib.round(lib.delta_t, 2)) + '<br/>'
            
        return information
        
    def selected_roundabout_informations(self):
        """
        """
        information = ''
        
        if self.selected_roundabout is not None:
            information += '<br/><b>Selected roundabout :</b><br/>'
            information += 'position : (' + str(self.selected_roundabout.position.x) + ',' + str(self.selected_roundabout.position.y) + ') <br/>'
            information += 'radius : ' + str(self.selected_roundabout.radius) + '<br/>'
            information += 'cars : ' + str(len(self.selected_roundabout.cars)) + '<br/>'
            information += 'load : ' + str(lib.round(self.selected_roundabout.global_load, 2)) + '<br/>'
            if self.selected_roundabout.spawning:
                information += '<b>Spawning mode</b><br/>'
            if len(self.selected_roundabout.leaving_roads) == 0:
                information += '<b>Destroying mode</b><br/>'
            if self.selected_roundabout.cars:
                avg_waiting_time = 0
                for car in self.selected_roundabout.cars:
                    avg_waiting_time += car.total_waiting_time / float(len(self.selected_roundabout.cars))
                information += '<br/><b>Average waiting time</b> (s) : ' + str(lib.round(avg_waiting_time,2)) + '<br/>'        
        
        return information
        
    def selected_car_informations(self):
        """
        """
        information = ''
        
        if self.selected_car is not None:
        
            car = self.selected_car
            
            if car.dead:
                self.selected_car = None
                return information
        
            information += '<br/><b>Selected vehicle :</b><br/>'
            if car.position is not None:
                information += 'position : (' + str(lib.round(car.position.x, 2)) + ', ' + str(lib.round(car.position.y, 2)) + ') <br/>'
            information += 'length, width : ' + str(car.length) + ', ' +  str(car.width) +'<br/>'
            information += 'speed : ' + str(lib.round(car.speed, 2)) + '<br/>'
            information += 'waiting time : ' + str(lib.round(car.total_waiting_time, 2)) + '<br/>'
            
            if car.destination is not None:
                information += 'destination : ' + str(car.destination.name) + ' <br/>'
                
            if car.is_waiting:
                information += '<b>Waiting or braking</b><br/>'
                
        return information
def main(args):
    """
    Main procedure : prepares and launches the main loop
    """
    lib.time_last_counter = 0.0

    app = QtGui.QApplication(args)
    
    main_window = MainWindow()
    main_window.showMaximized()

    sys.exit(app.exec_())
        
# Bootstrap
if __name__ == "__main__":
    main(sys.argv)

# Don't write anything after that !