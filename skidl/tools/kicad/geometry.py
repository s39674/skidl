# -*- coding: utf-8 -*-

# The MIT License (MIT) - Copyright (c) 2016-2021 Dave Vandenbout.

import math
from copy import copy, deepcopy

"""
Stuff for handling geometry, mostly points and bounding boxes.
"""


class Point:
    def __init__(self, x, y):
        """Create a Point with coords x,y."""
        self.x = x
        self.y = y

    def __add__(self, pt):
        """Add the x,y coords of pt to self and return the resulting Point."""
        if not isinstance(pt, Point):
            pt = Point(pt, pt)
        return Point(self.x + pt.x, self.y + pt.y)

    def __sub__(self, pt):
        """Subtract the x,y coords of pt from self and return the resulting Point."""
        if not isinstance(pt, Point):
            pt = Point(pt, pt)
        return Point(self.x - pt.x, self.y - pt.y)

    def __mul__(self, m):
        """Multiply the x,y coords by m."""
        return Point(m * self.x, m * self.y)

    def __neg__(self):
        """Negate both coords."""
        return Point(-self.x, -self.y)

    def __truediv__(self, d):
        """Divide the x,y coords by d."""
        return self * (1.0/d)

    def __round__(self, n):
        return Point(round(self.x, n), round(self.y, n))

    def round(self):
        """Round the x,y coords of the Point."""
        try:
            self.x = int(round(self.x))
            self.y = int(round(self.y))
        except OverflowError:
            # Point with coords set as math.inf.
            pass

    def min(self, pt):
        """Return a Point with coords that are the min x,y of both points."""
        return Point(min(self.x, pt.x), min(self.y, pt.y))

    def max(self, pt):
        """Return a Point with coords that are the max x,y of both points."""
        return Point(max(self.x, pt.x), max(self.y, pt.y))

    def __repr__(self):
        return "{self.__class__}({self.x}, {self.y})".format(self=self)

Vector = Point


class BBox:
    def __init__(self, *pts):
        """Create a bounding box surrounding the given points."""
        inf = float("inf")
        self.min = Point(inf, inf)
        self.max = Point(-inf, -inf)
        self.add(*pts)

    def add(self, *objs):
        """Update the bounding box size by adding Point/BBox objects."""
        for obj in objs:
            if isinstance(obj, Point):
                self.min = self.min.min(obj)
                self.max = self.max.max(obj)
            elif isinstance(obj, BBox):
                self.min = self.min.min(obj.min)
                self.max = self.max.max(obj.max)
            else:
                raise NotImplementedError

    def __round__(self, n):
        return BBox(round(self.min), round(self.max))

    def round(self):
        """Round the BBox min, max points."""
        self.min.round()
        self.max.round()

    def intersects(self, bbox):
        return (self.min.x < bbox.max.x) and (self.max.x > bbox.min.x) and (self.min.y < bbox.max.y) and (self.max.y > bbox.min.y)

    def move(self, vector):
        """Move the corner points of a bounding box."""
        self.min += vector
        self.max += vector

    def resize(self, vector):
        """Expand/contract the bounding box by applying vector to its corner points."""
        self.min -= vector
        self.max += vector

    @property
    def area(self):
        """Return area of bounding box."""
        return self.w * self.h

    @property
    def w(self):
        """Return the bounding box width."""
        return abs(self.max.x - self.min.x)

    @property
    def h(self):
        """Return the bounding box height."""
        return abs(self.max.y - self.min.y)

    @property
    def ctr(self):
        """Return center point of bounding box."""
        return (self.max + self.min) / 2

    @property
    def ll(self):
        """Return lower-left point of bounding box."""
        return Point(self.min.x, self.min.y)

    @property
    def lr(self):
        """Return lower-right point of bounding box."""
        return Point(self.max.x, self.min.y)

    @property
    def ul(self):
        """Return upper-left point of bounding box."""
        return Point(self.min.x, self.max.y)

    @property
    def ur(self):
        """Return upper-right point of bounding box."""
        return Point(self.max.x, self.max.y)

    def __repr__(self):
        return "{self.__class__}({self.min}, {self.max})".format(self=self)