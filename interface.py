# -*- coding: utf-8 -*-
"""
File        :   interface.py
Description :   Manages the displays and main loop.
"""

import constants    as __constants__
import init     
from vector         import Vector

import sys
from PyQt4          import QtCore, QtGui
import pygame

screen = pygame.display.set_mode(__constants__.RESOLUTION)

def draw_roundabout(roundabout):
    """
    Draws a given roundabout on the screen.
        roundabout (Roundabout) : the aforementioned roundabout.
    
    Dessine un carrefour donné à l'écran.
        roundabout (Roundabout) : le carrefour sus-cité.
    """
    # TODO :
    #       · (DN1) draw the cars on the roundabout
    
    if not init.track.picture:
        pygame.draw.circle(screen, __constants__.ROUNDABOUT_COLOR, roundabout.position.ceil().get_tuple(), __constants__.ROUNDABOUT_WIDTH)
    
    if roundabout.cars:
        # There are cars on the roundabout, we may want to draw them
        # albeit we can't use draw_car here...
        
        #TEMPORARY : the number of cars on the roundabout is written
        position = Vector(roundabout.position.x + 10, roundabout.position.y + 10)
        draw_text(position, str(len(roundabout.cars)))
        pass

def draw_car(car):
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
    
    color = car.color
    # Draw the car 
    pygame.draw.polygon(screen, color, [point[i].get_tuple() for i in range(len(point))])
    draw_aapolygon(screen,  __constants__.BLACK, [point[i].get_tuple() for i in range(len(point))])
   
def draw_aapolygon(surface, color, points):
    """
    Draw an antialiased hollow polygon
    """
    for i in range(len(points)):
        pygame.draw.aaline(surface, color, points[i], points[(i + 1) % len(points)])

def draw_text(position = Vector(screen.get_rect().centerx, screen.get_rect().centery), message = '', text_color = __constants__.WHITE, back_color = __constants__.BLACK, font = None, anti_aliasing = True):
    """
    Draws text on the screen
        position    (Vector  :   position where the text is to be written
        message (str)        :   the message that is to be written
        text_color (list)    :   the color of the text to be written
        back_color (list)    :   the color on which the text is to be written
        font (pygame.font)   :   the font that will be used for the text to be written
        anti_aliasing (bool) :   whether we should antialias the text to be written
    """
    #   The (optional) pygame.font module is not supported : cannot draw text
    if not pygame.font:
        raise Exception("WARNING (in draw_text()) : the pygame.font module is not supported, cannot draw text.")
    else:
        #   No font is provided : use of a default font
        if not font:
            font = pygame.font.Font(None, 17)
            
        text = font.render(message, anti_aliasing, text_color, back_color)
        textRect = text.get_rect()
        textRect.x, textRect.y = position.x, position.y
        screen.blit(text, textRect)
        
def draw_traffic_light(position, road, gate):
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
            color = __constants__.LIGHT_GREEN
            width = 0
        elif (not state) and (i == 2):
            color = __constants__.LIGHT_RED
            width = 0
        else:
            color = __constants__.GRAY
            width = 1
        
        position = start_position + d_position * i
        pygame.draw.circle(screen, color, position.get_list(), TF_RADIUS, width)

def draw_road(road):
    """
    Draws a given road on the screen and all the cars on it.
        road (Road) : the aforementioned road.
            
    Dessine une route donnée à l'écran et toutes les voitures dessus.
        road (Road) : la route sus-citée.
    """
    
    (start_position, end_position) = (road.begin.position.ceil(), road.end.position.ceil())
   
    # This is not perfect... but it's ok for now I guess -- Sharayanan
    draw_traffic_light(end_position, road, __constants__.LEAVING_GATE)
     
    color = __constants__.GREEN
    key = 0
    if road.cars and __constants__.DISPLAY_DENSITY:
        occupation = 0
        for car in road.cars:
            occupation += car.length
            
        key = 2 * (float(occupation)/float(road.length)) * 255
        if key > 255: key = 255
        color = [key, 255 - key, 0]
    
    if not init.track.picture:
        pygame.draw.aaline(screen, color, start_position.get_tuple(), end_position.get_tuple()) # EXPERIMENTAL
    
    if road.cars and key < 200:
        # Do not draw cars when density exceeds ~80%
        for car in road.cars:
            draw_car(car)

def draw_scene():
    """
    Draws the complete scene on the screen.
    Dessine la scène entière à l'écran.
    """  
    try:
        screen.fill(__constants__.BLACK)
    except pygame.error, exc:
        exit()
        
    # EXPERIMENTAL
    if init.track.picture:
        screen.blit(init.track.picture, (0,0))
    
    for road in init.track.roads:
        draw_road(road)
    for roundabout in init.track.roundabouts:
        draw_roundabout(roundabout)
        
    pygame.display.flip()
    pygame.display.update()
    
def halt():
    """
    Closes properly the simulation.
    Quitte correctement la simulation.
    """
    pygame.quit()
  
class ThereIsNoRush(QtGui.QMainWindow):
    def __init__(self, parent = None):
        #   Call parent constructor
        QtGui.QWidget.__init__(self, parent)
        
        #   Set the window
        #self.resize(__constants__.PANEL_WIDTH, __constants__.PANEL_HEIGHT) # (width, height)
        #self.center()
        self.setWindowTitle(__constants__.REVISION_NAME + ' - r' + str(__constants__.REVISION_NUMBER))
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
        
        #   Fields
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

        #   Set the display grid
        grid = QtGui.QGridLayout()
        #grid.setSpacing(10)
        
        grid.addWidget(lbl_total_roundabouts, 0, 0)
        grid.addWidget(self.total_roundabouts, 0, 1)
        
        grid.addWidget(lbl_total_roads, 1, 0)
        grid.addWidget(self.total_roads, 1, 1)
        
        grid.addWidget(lbl_total_cars, 2, 0)
        grid.addWidget(self.total_cars, 2, 1)

        grid.addWidget(lbl_cars_on_roundabouts, 3, 0)
        grid.addWidget(self.cars_on_roundabouts, 3, 1)

        grid.addWidget(lbl_cars_on_roads, 4, 0)
        grid.addWidget(self.cars_on_roads, 4, 1)
        
        grid.addWidget(lbl_cars_waiting, 5, 0)
        grid.addWidget(self.cars_waiting, 5, 1)

        central_widget = QtGui.QWidget()
        central_widget.setLayout(grid)
        self.setCentralWidget(central_widget)
        
        #   Timer
        timer = QtCore.QTimer(self)
        self.connect(timer, QtCore.SIGNAL("timeout()"), self.update)
        timer.start(__constants__.delta_t * 100.0)


    def closeEvent(self, event):
        """
        Specifies what has to be done when exiting the application ; this function is automatically called by Qt as soon as the user clicks on the close button (at the top right of the window), that's why you mustn't change its name !
        """
        reply = QtGui.QMessageBox.question(self, 'Confirm', "Do you really want to exit ?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

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
            self.close()

    def update(self):
        """
        Updates the simulation.
        """
        #   Run the simulation for delta_t
        for road in init.track.roads:
            road.update()
        for roundabout in init.track.roundabouts:
            roundabout.update()
        
        #   Update the scene
        draw_scene()
        
        #   Update the information
        self.total_roads.setValue(len(init.track.roads))
        self.total_roundabouts.setValue(len(init.track.roundabouts))

        self.cars_on_roads.setValue(0)
        self.cars_on_roundabouts.setValue(0)
        self.cars_waiting.setValue(0)
        
        for road in init.track.roads:
            self.cars_on_roads.setValue(self.cars_on_roads.value() + len(road.cars))
            self.cars_waiting.setValue(self.cars_waiting.value() + road.total_waiting_cars)
        for roundabout in init.track.roundabouts:
            self.cars_on_roundabouts.setValue(self.cars_on_roundabouts.value() + len(roundabout.cars))
        
        self.total_cars.setValue(self.cars_on_roads.value() + self.cars_on_roundabouts.value())

# Bootstrap
if __name__ == "__main__":
    # Before simulation instructions
    pygame.init()
    pygame.display.set_caption(__constants__.REVISION_NAME + ' - r' + str(__constants__.REVISION_NUMBER))
    
    application = QtGui.QApplication(sys.argv)

    panel = ThereIsNoRush()
    panel.show()
    
    #   Main loop
    sys.exit(application.exec_())
    
# Don't write anything after that !
