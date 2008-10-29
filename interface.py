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

class main_window_inherit(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
    
class main_window_class(QtGui.QMainWindow):
    def __init__(self, inherit_class = None):
        QtGui.QWidget.__init__(self, None)

        self.setup_interface()
        
        self.inherit = inherit_class
        self.inherit.show()
        
        self.timer = QtCore.QBasicTimer()
        self.timer.start(10, self)

    def setup_interface(self):
    
        width  = __constants__.PANEL_WIDTH
        height = __constants__.PANEL_HEIGHT
    
        self.resize(__constants__.WINDOW_WIDTH,__constants__.WINDOW_HEIGHT)
        
        # Main window's content
        self.setObjectName('main_window_class')
        self.centralWidget = QtGui.QWidget(self)
        self.centralWidget.setObjectName('central_widget')

        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        
        # Dockable control window
        self.control_panel = QtGui.QMainWindow(self) #QtGui.QDockWidget(self)
        self.control_panel.setSizePolicy(size_policy)
        self.control_panel.setObjectName('control_panel')
        self.panel_contents = QtGui.QWidget(self.control_panel)
        self.panel_contents.setObjectName('panel_contents')
        
        self.control_panel.resize(width, height)
        size_policy.setHeightForWidth(self.control_panel.sizePolicy().hasHeightForWidth())
        
        # Tab system
        self.tab_controls = QtGui.QTabWidget(self.panel_contents)
        self.tab_controls.setGeometry(QtCore.QRect(4, 4, width - 8, height - 8))
        self.tab_controls.setTabPosition(QtGui.QTabWidget.East)
        self.tab_controls.setObjectName('tab_controls')
        
        # Tab in tabs
        self.tab_infos = QtGui.QWidget()
        self.tab_commands = QtGui.QWidget()
        self.tab_infos.setObjectName('tab_infos')
        self.tab_commands.setObjectName('tab_commands')
        
        self.tab_controls.addTab(self.tab_infos, '')
        self.tab_controls.addTab(self.tab_commands, '')
        self.tab_controls.setCurrentIndex(0)
        
        # Information label
        self.lbl_infos = QtGui.QLabel(self.tab_infos)
        self.lbl_infos.setGeometry(QtCore.QRect(4,4,width - 8 - 8, height - 8 - 8))
        self.lbl_infos.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.lbl_infos.setWordWrap(True)
        self.lbl_infos.setObjectName('lbl_infos')
        
        # Option boxes
        self.entrance_lights = QtGui.QCheckBox(self.tab_commands)
        self.exit_lights     = QtGui.QCheckBox(self.tab_commands)
        
        self.entrance_lights.setObjectName('entrance_lights')
        self.exit_lights.setObjectName('exit_lights')
        
        self.entrance_lights.move(4,4)
        self.exit_lights.move(4, 23 + 4)
        
        # Default values
        self.entrance_lights.setChecked(False)
        self.exit_lights.setChecked(True)
        
        # Encapsulation
        self.control_panel.setCentralWidget(self.panel_contents)
        
        # Captions, icons…
        self.setWindowTitle(__constants__.REVISION_NAME + ' - r' + str(__constants__.REVISION_NUMBER))
        self.control_panel.setWindowTitle('Controls')
        self.lbl_infos.setText('<i>Informations</i>')
        
        self.tab_controls.setTabText(0, 'Informations')
        self.tab_controls.setTabText(1, 'Commands')
        self.entrance_lights.setText('Incoming traffic lights')
        self.exit_lights.setText('Leaving traffic lights')
        
        self.setWindowIcon(QtGui.QIcon('icons/tinr_logo.png'))
        self.control_panel.setWindowIcon(QtGui.QIcon('icons/window.png'))
        
        QtCore.QMetaObject.connectSlotsByName(self)
        
        self.control_panel.show()
        
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
        for roundabout in init.track.roundabouts:
            self.draw_roundabout(painter, roundabout)

    def draw_road(self, painter, road):
        """
        Draws a given road on the screen and all the cars on it.
            road (Road) : the aforementioned road.

        Dessine une route donnée à l'écran et toutes les voitures dessus.
            road (Road) : la route sus-citée.
        """

        (start_position, end_position) = (road.begin.position.ceil(), road.end.position.ceil())

        # This is not perfect... but it's ok for now I guess -- Sharayanan
        if self.exit_lights.isChecked():
            self.draw_traffic_light(painter, end_position, road, __constants__.LEAVING_GATE)
        if self.entrance_lights.isChecked():
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

    def draw_roundabout(self, painter, roundabout):
        """
        Draws a given roundabout on the screen.
            roundabout (Roundabout) : the aforementioned roundabout.

        Dessine un carrefour donné à l'écran.
            roundabout (Roundabout) : le carrefour sus-cité.
        """
        # TODO :
        #       · (DN1) draw the cars on the roundabout

        if not init.track.picture:
            #pygame.draw.circle(self.screen, __constants__.ROUNDABOUT_COLOR, roundabout.position.ceil().get_tuple(), __constants__.ROUNDABOUT_WIDTH)
            pass

        if roundabout.cars:
            # There are cars on the roundabout, we may want to draw them
            # albeit we can't use draw_car here...

            #TEMPORARY : the number of cars on the roundabout is written
            position = Vector(roundabout.position.x + 10, roundabout.position.y + 10)
            painter.drawText(position.x, position.y, str(len(roundabout.cars)))
            pass        
        
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
            self.update_information()
            self.update()
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
        
    def update_information(self):
        """
        """
        information = ''
        
        information += '<b>Roads : </b>' + str(len(init.track.roads)) + '<br/>'
        information += '<b>Roundabouts : </b>' + str(len(init.track.roundabouts)) + '<br/>'

        cars_on_roads = 0
        cars_waiting  = 0
        cars_on_roundabouts = 0
        
        for road in init.track.roads:
            cars_on_roads += len(road.cars)
            cars_waiting  += road.total_waiting_cars
        for roundabout in init.track.roundabouts:
            cars_on_roundabouts += len(roundabout.cars)

        total_cars = cars_on_roads + cars_on_roundabouts
        
        information += '<b>Cars</b> (total) : ' + str(total_cars) + '<br/>'
        information += '(on roads) : '          + str(cars_on_roads) + '<br/>'
        information += '(on rdabt) : '          + str(cars_on_roundabouts) + '<br/>'
        information += '(waiting) : '           + str(cars_waiting)
        
        self.lbl_infos.setText(information)
        
        if not self.control_panel.isVisible():
            # The control panel has been closed: exit
            exit()

def main(args):
    app = QtGui.QApplication(args)
    
    inherit_class = main_window_inherit()
    main_window = main_window_class(inherit_class)
    main_window.show() 

    sys.exit(app.exec_())
        
# Bootstrap
if __name__ == "__main__":
    main(sys.argv)
# Don't write anything after that !