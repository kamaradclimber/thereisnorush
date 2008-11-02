# -*- coding: utf-8 -*-
"""
File        :   interface.py
Description :   Manages the displays and main loop.
"""

import lib
import sys
import time

import constants
import track        as __track__

from vector         import Vector
from PyQt4          import QtCore, QtGui, Qt

class Scene(QtGui.QWidget):
    """
    Area where the scene will be drawn.
    """

    def __init__(self, new_window, parent = None):
        QtGui.QWidget.__init__(self, parent)

        self.painter    = None
        self.window     = new_window
        
        self.setSizePolicy(QtGui.QSizePolicy())
        self.setMinimumSize(constants.SCENE_WIDTH, constants.SCENE_HEIGHT)
        
        lib.Delta_t = 0
        self.last_update = time.clock()

    def paintEvent(self, event):
        """
        /!\ Qt specific (please don't rename)
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
            self.draw_traffic_light(end_position, road, constants.EXIT)
        if self.window.entrance_lights.isChecked():
            self.draw_traffic_light(start_position, road, constants.ENTRANCE)
        
        self.painter.setPen(QtGui.QColor(*constants.ROAD_COLOR))
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
            self.painter.setPen(QtGui.QColor(*constants.TRANSPARENT))
            self.painter.drawEllipse(roundabout.position.x - roundabout.radius/4, roundabout.position.y - roundabout.radius/4, roundabout.radius/2, roundabout.radius/2)
            pass
        
        #   Selected roudabout
        if self.window.selected_roundabout == roundabout:
            self.painter.setPen(QtGui.QColor(*constants.ROUNDABOUT_COLOR))
            self.painter.setBrush(QtGui.QColor(*constants.TRANSPARENT))
            self.painter.drawEllipse(roundabout.position.x - roundabout.radius, roundabout.position.y - roundabout.radius, 2 * roundabout.radius, 2 * roundabout.radius)

        if roundabout.cars:
            # There are cars on the roundabout, we may want to draw them
            # albeit we can't use draw_car here...

            #TEMPORARY : the number of cars on the roundabout is written
            position = Vector(roundabout.position.x + 10, roundabout.position.y + 10)
            self.painter.setPen(QtGui.QColor(*constants.WHITE))
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
            self.painter.setPen(QtGui.QColor(*constants.GREY))
            self.painter.drawEllipse(position.x - TF_RADIUS, position.y - TF_RADIUS, 2 * TF_RADIUS, 2*TF_RADIUS)
            
    def mousePressEvent(self, event):
        """
        /!\ Qt specific (please don't rename)
        Manages what happens when a mouse button is pressed
        """
        # Experimental : select a roundabout
        self.window.select_roundabout(event.x(), event.y())

class MainWindow(QtGui.QMainWindow):
    """
    
    """

    def __init__(self, parent = None):
        """
        Creates the main window
        """
        QtGui.QMainWindow.__init__(self, parent)

        self.setup_interface()
        
        self.timer = QtCore.QBasicTimer()
        self.timer.start(10, self)
        
        self.selected_roundabout = None

    def setup_interface(self):
        """
        Sets up the Qt interface, layout, slots & properties
        """
        #   Window settings
        self.setObjectName('MainWindow')
        self.setWindowTitle(constants.REVISION_NAME + ' - r' + str(constants.REVISION_NUMBER))
        self.setWindowIcon(QtGui.QIcon('icons/tinr_logo.png'))

        self.setCentralWidget(QtGui.QWidget())
        
        #   Scene
        self.scene = Scene(self)
        self.scene.setObjectName('scene')
        
        #   Commands tab
        self.entrance_lights = QtGui.QCheckBox('Display entrance traffic lights')
        self.entrance_lights.setObjectName('entrance_lights')
        self.entrance_lights.setChecked(False)
        
        self.exit_lights = QtGui.QCheckBox('Display exit traffic lights')
        self.exit_lights.setObjectName('exit_lights')
        self.exit_lights.setChecked(True)
        
        self.use_antialiasing = QtGui.QCheckBox('Use antialiasing')
        self.use_antialiasing.setObjectName('use_antialiasing')
        self.use_antialiasing.setChecked(True)

        lay_commands = QtGui.QVBoxLayout()
        lay_commands.addWidget(self.entrance_lights)
        lay_commands.addWidget(self.exit_lights)
        lay_commands.addWidget(self.use_antialiasing)
        
        self.tab_commands = QtGui.QWidget()
        self.tab_commands.setObjectName('tab_commands')
        self.tab_commands.setLayout(lay_commands)

        #   Information tab
        self.lbl_info = QtGui.QLabel('<i>Information</i>')
        self.lbl_info.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.lbl_info.setWordWrap(True)
        self.lbl_info.setObjectName('lbl_info')
        
        lay_info = QtGui.QVBoxLayout()
        lay_info.addWidget(self.lbl_info)

        self.tab_info = QtGui.QWidget()
        self.tab_info.setObjectName('tab_info')
        self.tab_info.setLayout(lay_info)        
        
        #   Control panel
        self.control_panel = QtGui.QTabWidget()
        self.control_panel.setObjectName('control_panel')
        self.control_panel.resize(constants.PANEL_WIDTH, constants.PANEL_HEIGHT)
        self.control_panel.setTabPosition(QtGui.QTabWidget.East)
        self.control_panel.addTab(self.tab_info, 'Informations')
        self.control_panel.addTab(self.tab_commands, 'Commands')
        self.control_panel.setCurrentIndex(0)
        
        QtCore.QMetaObject.connectSlotsByName(self)

        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.control_panel.setSizePolicy(size_policy)
        
        #   Display
        lay_window = QtGui.QGridLayout()
        lay_window.addWidget(self.scene, 0, 0)
        lay_window.addWidget(self.control_panel, 0, 1)

        self.centralWidget().setLayout(lay_window)

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
        
    def timerEvent(self, event):
        """
        /!\ Qt specific (please don't rename)
        Passes or uses timer events to update the simulation
        """
        if event.timerId() == self.timer.timerId():
            self.update_simulation()
            self.update_information()
            self.scene.update()
            
            lib.Delta_t = time.clock() - self.scene.last_update
            self.scene.last_update = time.clock()
        else:
            QtGui.QFrame.timerEvent(self, event)

    def update_simulation(self):
        """
        Updates the simulation.
        """
        #   Run the simulation for delta_t
        for road in __track__.track.roads:
            road.update()
        for roundabout in __track__.track.roundabouts:
            #oui deux boucles séparées sinon linfo est pas en temps réél (enfin ca serait pas un drame non plus vu l'échelle de delta_t ! )
            # Weird : selfish_load is a property, hence it is not callable !
            dummy = roundabout.selfish_load
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
        information += '(waiting) : '           + str(cars_waiting)
        
        if self.selected_roundabout is not None:
            information += '<br/><br/><b>Selected roundabout :</b><br/>'
            information += 'position : (' + str(self.selected_roundabout.position.x) + ',' + str(self.selected_roundabout.position.y) + ') <br/>'
            information += 'radius : ' + str(self.selected_roundabout.radius) + '<br/>'
            information += 'cars : ' + str(len(self.selected_roundabout.cars)) + '<br/>'
            information += 'load : ' + str(self.selected_roundabout.load) + '<br/>'
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
