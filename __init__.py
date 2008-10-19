# -*- coding: utf-8 -*-
"""
File        :   __init__.py
Description :   defines the constants
"""

try:
    CONSTANTS_IMPORTED
except NameError:
    CONSTANTS_IMPORTED = True

    #   Colors constants
    BLACK       = (  0,   0,   0)
    RED         = (255,   0,   0)
    GREEN       = (  0, 255,   0)
    BLUE        = (  0,   0, 255)
    WHITE       = (255, 255, 255)
    GRAY        = (190, 190, 190)
    
    LIGHT_RED   = (255,  64,  64)
    LIGHT_GREEN = ( 64, 255,  64)
    LIGHT_BLUE  = ( 64,  64, 255)

    #   Car constants
    CAR_DEFAULT_LENGTH  = 5
    CAR_DEFAULT_WIDTH   = 4
    CAR_DEFAULT_HEADWAY = CAR_DEFAULT_LENGTH    # marge de sécurité
    CAR_DEFAULT_SPEED   = 0
    CAR_DEFAULT_ACCEL   = 50
    CAR_DEFAULT_COLOR   = (255, 255, 255) #( 64,  64, 255)
    
    #   Roundabout constants
    ROUNDABOUT_WIDTH                    = 3
    ROUNDABOUT_HEIGHT                   = 3
    ROUNDABOUT_COLOR                    = RED
    ROUNDABOUT_RADIUS_DEFAULT           = 10
    ROUNDABOUT_DEFAULT_ROTATION_SPEED   = 10
    
    #   Road constants
    ROAD_COLOR              = WHITE
    ROAD_DEFAULT_MAX_SPEED  = 50
    ROAD_DEFAULT_LENGTH     = 100
    ROAD_DEFAULT_WIDTH      = 5

    #   Other constants
    RESOLUTION  = (WINDOW_WIDTH, WINDOW_HEIGHT) = (800, 600)
    delta_t = 0.1

    DISPLAY_DENSITY = False # You may de-activate per-density coloring (+ fps)
    
    REVISION_NUMBER = 98

    LEAVING_GATE    = 1
    INCOMING_GATE   = 0
    SPAWN_TIME      = 1000
