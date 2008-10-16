# -*- coding: utf-8 -*-
"""
File        :   vector.py
Description :   a simple physics 2D vector class

Licence: Public Domain
Author: Chris Wood (http://grace.2ya.com)
    20 September 2002

Any game involving 2D physics could do with a class similar to this one. This
class is as fast as possible while still providing all the functionality you
would commonly need.

Note that storing the vector as cartesian coordinates (rather than polar or
both) makes for faster for vector addition. It is assumed that you won't often
need the polar coordinates.
"""

from math import sin, cos, atan, hypot

# The quick way to know how big the pie is
PI = 3.141592653589793238462643383
TwoPI = PI * 2.0
HalfPI = PI * 0.5
OneAndHalfPI = PI * 1.5

# new math function
def direction(x, y):
    """Return the direction component of a vector (in radians), given
    cartesian coordinates.
    """
    if x > 0:
        if y >= 0:
            return atan(y / x)
        else:
            return atan(y / x) + TwoPI
    elif x == 0:
        if y > 0:
            return HalfPI
        elif y == 0:
            return 0
        else:
            return OneAndHalfPI
    else:
        return atan(y / x) + PI


class Vector:
    """Store a vector in cartesian coordinates."""
    
    def __init__(self, f = 0.0, mag = 0.0):
        """Create a Vector, given polar coordinates."""
        # Calculate cartesian coordinates
        self.x = mag * cos(f)
        self.y = mag * sin(f)
    
    def __init__(self, x = 0.0, y = 0.0):
        """Create a Vector, given cartesian coordinates."""
        self.x = x
        self.y = y
    
    def normalize(self):
        dist = float(abs(self))
        if dist > 0:
            self.x = float(self.x)/dist
            self.y = float(self.y)/dist
        else:
            self.x, self.y = 0.0, 0.0
        return self 
    
    def get_orthogonal(self):
        if (self.x or self.y):
            return Vector(-self.y, self.x)
    
    def get_list(self):
        return [self.x, self.y]
    
    def get_tuple(self):
        return (self.x, self.y)
    
    def ceil(self):
        return Vector(int(self.x), int(self.y))
    
    #   Operators
    def __add__(self, vector):
        return Vector(self.x + vector.x, self.y + vector.y)
    
    def __neg__(self):
        return Vector(-self.x, -self.y)
    
    def __sub__(self, vector):
        return Vector(self.x - vector.x, self.y - vector.y)
    
    #   Be careful about the order : you may not write "<scale> * <vector>", but "<vector> * <scale>" !
    def __mul__(self, scale):
        return Vector(scale*self.x, scale*self.y)
    
    def __div__(self, scale):
        return Vector(self.x/scale, self.y/scale)
    
    def __eq__(self, vector):
        return (self.x == vector.x) and (self.y == vector.y)
    
    def __abs__(self):
        return hypot(self.x, self.y)
    
    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'
    
    def heading(self):
        """Return the direction of the Vector in radians."""
        return direction(self.x, self.y)
