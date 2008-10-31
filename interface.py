# -*- coding: utf-8 -*-
"""
File        :   interface.py
Description :   Manages the displays and main loop.
"""

import lib
import sys

import constants    as __constants__
import track        as __track__

from vector         import Vector
from PyQt4          import QtCore, QtGui, Qt

class Scene(QtGui.QTabWidget):
    """
    Area where the scene will be drawn.
    """

    def __init__(self, parent, new_window):
        QtGui.QWidget.__init__(self, parent)

        self.painter    = None
        self.window     = new_window
        
        self.resize(__constants__.SCENE_WIDTH, __constants__.SCENE_HEIGHT)
#        size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
#        self.setSizePolicy(size_policy)
        

    def paintEvent(self, event):
        """
        Specifies how the control should draw itself.
        """
        
        self.painter = QtGui.QPainter(self)

        self.painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
#        self.painter.fillRect(QtCore.QRectF(QtCore.QPointF(0, 0), QtCore.QPointF(self.width(), self.height())), QtGui.QColor(0, 0, 0))
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
            self.draw_traffic_light(end_position, road, __constants__.LEAVING_GATE)
        if self.window.entrance_lights.isChecked():
            self.draw_traffic_light(start_position, road, __constants__.INCOMING_GATE)

        color = __constants__.GREEN
        key = 0
        if road.cars and __constants__.DISPLAY_DENSITY:
            occupation = 0
            for car in road.cars:
                occupation += car.length

            key = 2 * (float(occupation)/float(road.length)) * 255
            if key > 255: key = 255
            color = [key, 255 - key, 0]

#        if not __track__.track.picture:
        self.painter.drawLine(start_position.x, start_position.y, end_position.x, end_position.y)

        #   Do not draw cars when density exceeds ~80%
        if road.cars and key < 200:
            for car in road.cars:
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

        length_covered = float(int(car.position)) / float(int(car.location.length))

        #   Get them once
        (r_width, r_length)    = (car.width, car.length)
        (parallel, orthogonal) = car.location.unit_vectors

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
            #pygame.draw.circle(self.screen, __constants__.ROUNDABOUT_COLOR, roundabout.position.ceil().get_tuple(), __constants__.ROUNDABOUT_WIDTH)
            pass
        
        #   Selected roudabout
        if self.window.selected_roundabout == roundabout:
            self.painter.setPen(QtGui.QColor(*__constants__.ROUNDABOUT_COLOR))
            self.painter.setBrush(QtGui.QColor(*__constants__.TRANSPARENT))
            self.painter.drawEllipse(roundabout.position.x - roundabout.radius, roundabout.position.y - roundabout.radius, 2 * roundabout.radius, 2 * roundabout.radius)

        if roundabout.cars:
            # There are cars on the roundabout, we may want to draw them
            # albeit we can't use draw_car here...

            #TEMPORARY : the number of cars on the roundabout is written
            position = Vector(roundabout.position.x + 10, roundabout.position.y + 10)
            self.painter.setPen(QtGui.QColor('black'))
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
        state     = road.gates[gate]

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
            self.painter.drawEllipse(position.x - TF_RADIUS, position.y - TF_RADIUS, 2 * TF_RADIUS, 2*TF_RADIUS)
            
    def mousePressEvent(self, event):
        """
        Manages what happens when a mouse button is pressed
        """
        # Experimental : select a roundabout
        self.window.select_roundabout(event.x(), event.y())


class MainWindow(QtGui.QMainWindow):
    """
    
    """

    def __init__(self, parent = None):
        """

        """
        QtGui.QMainWindow.__init__(self, parent)

        self.setup_interface()
        
        self.timer = QtCore.QBasicTimer()
        self.timer.start(10, self)
        
        self.selected_roundabout = None

    def setup_interface(self):
        """
    
        """
        #   Window settings
        self.setObjectName('MainWindow')
        self.setWindowTitle(__constants__.REVISION_NAME + ' - r' + str(__constants__.REVISION_NUMBER))
        self.setWindowIcon(QtGui.QIcon('icons/tinr_logo.png'))

        self.setCentralWidget(QtGui.QWidget())
        
        #   Scene
        self.scene = Scene(None, self)
        
        #   Commands tab
        self.entrance_lights = QtGui.QCheckBox('Display entrance traffic lights')
        self.entrance_lights.setObjectName('entrance_lights')
        self.entrance_lights.setChecked(False)
        
        self.exit_lights = QtGui.QCheckBox('Display exit traffic lights')
        self.exit_lights.setObjectName('exit_lights')
        self.exit_lights.setChecked(True)

        lay_commands = QtGui.QVBoxLayout()
        lay_commands.addWidget(self.entrance_lights)
        lay_commands.addWidget(self.exit_lights)
        
        self.tab_commands = QtGui.QWidget()
        self.tab_commands.setObjectName('Commands tab')
        self.tab_commands.setLayout(lay_commands)

        #   Information tab
        self.lbl_info = QtGui.QLabel('<i>Information</i>')
        self.lbl_info.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.lbl_info.setWordWrap(True)
        self.lbl_info.setObjectName('Information text')
        
        lay_info = QtGui.QVBoxLayout()
        lay_info.addWidget(self.lbl_info)

        self.tab_info = QtGui.QWidget()
        self.tab_info.setObjectName('Information tab')
        self.tab_info.setLayout(lay_info)        
        
        #   Control panel
        self.control_panel = QtGui.QTabWidget()
        self.control_panel.setObjectName('Control panel')
        self.control_panel.resize(__constants__.PANEL_WIDTH, __constants__.PANEL_HEIGHT)
        self.control_panel.setTabPosition(QtGui.QTabWidget.East)
        self.control_panel.addTab(self.tab_info, 'Information')
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
        Specifies what has to be done when exiting the application.
        This function is automatically called by Qt when the user clicks on the close button : don't change its name !
        """
        event.accept()
        exit()
    
    def keyPressEvent(self, event):
        """
        Manages the keyboard events ; the name of the function is set by Qt, so don't change it.
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
        Passes or uses timer events to update the simulation
        """
        if event.timerId() == self.timer.timerId():
            self.update_simulation()
            self.update_information()
            self.scene.update()
            self.update()
        else:
            QtGui.QFrame.timerEvent(self, event)

    def update_simulation(self):
        """
        Updates the simulation.
        """
        #   Run the simulation for delta_t
        for road in __track__.track.roads:
            road.update()
#        for roundabout in __track__.track.roundabouts:
            #oui deux boucles séparées sinon linfo est pas en temps réél (enfin ca serait pas un drame non plus vu l'échelle de delta_t ! )
#            roundabout.selfish_load()
        for roundabout in __track__.track.roundabouts:
            roundabout.update()
        
    def update_information(self):
        """
        """
        information = ''
        
        information += '<b>Roads : </b>'        + str(len(__track__.track.roads))       + '<br/>'
        information += '<b>Roundabouts : </b>'  + str(len(__track__.track.roundabouts)) + '<br/>'

        cars_on_roads = 0
        cars_waiting  = 0
        cars_on_roundabouts = 0
        
        for road in __track__.track.roads:
            cars_on_roads += len(road.cars)
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
            if self.selected_roundabout.spawning:
                information += '<b>Spawning node<b>'
        
        self.lbl_info.setText(information)

def main(args):
    app = QtGui.QApplication(args)
    
    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())
        
# Bootstrap
if __name__ == "__main__":
    main(sys.argv)

# Don't write anything after that !
