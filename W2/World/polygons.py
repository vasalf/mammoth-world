#!/usr/bin/python3

"""This is a library that provides classes to work with random polygons.

              It is a part of mammoth-world project
            (https://github.com/vasalf/mammoth-world)

"""

from random import *

"""A place to import modules is up to that comment.

"""

__author__ = "vasalf"


def cross_product(a, b):
    return a[0] * b[1] - b[0] * a[1]


def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1]


def sq_point_distance(a, b):
    x = a[0] - b[0]
    y = a[1] - b[1]
    return x * x + y * y

def vector(a, b):
    return (b[0] - a[0], b[1] - a[1])


class __sorted_by_polar_angle_point:
    """This is a helper class to convex

    """
    def __init__(self, p, first):
        self.__pt = p[:]
        self.__first = first[:]

    def __getitem__(self, i):
        return self.__pt[i]

    def __lt__(self, other):
        if cross_product(vector(self.__first, self), \
                         vector(self.__first, other)) == 0:
            return sq_point_distance(self.__first, self) < \
                   sq_point_distance(self.__first, other)
        else:
            return cross_product(vector(self.__first, self), \
                                 vector(self.__first, other)) > 0

        def __tuple__(self):
            return self.__pt


def convex(point_set):
    """That functions builds the convex of a point_set.
       It uses Graham algotirhm.

    """
    start = min(point_set)
    set_copy = []
    for p in point_set:
        set_copy.append(__sorted_by_polar_angle_point(p, start))
    set_copy.sort()
    set_copy.append(start)
    res = set_copy[:2]
    for p in set_copy[2:]:
        while len(res) >= 2 and \
              cross_product(vector(res[-1], res[-2]), vector(res[-1], p)) >= 0:
            res.pop()
        res.append(p)
    return list(map(tuple, res[:-1]))


def unite(lst):
    res = []
    for pol in lst:
        for p in pol:
            res.append(p)
    return res


class random_polygon:
    """Constructor args:
       self: no comments
       arg: if list -> list of vertex, if int -> number of vertex to generate
       borders: a tuple of points (tuples of numbers). Generated polygon will
                lie in rectangle with left corner in first and right corner
                in second
       must_be_in: an iterable object of random polygons that must be into the
                   generated polygon

    """
    def __init__(self, arg, borders=None, must_be_in=None):
        if isinstance(arg, list):
            # Then just make a polygon from list
            self.__points = arg[:]
        elif isinstance(arg, random_polygon):
            # Then just make a COPY of polygon
            self.__points = arg.__points[:]
        else:
            # Then generate arg points
            assert isinstance(arg, int)
            assert arg > 0
            assert borders is not None
            assert isinstance(must_be_in, list)
            ld, ru = borders

            res = convex(unite(must_be_in))
            self.__points = res[:]

    def __getitem__(self, i):
        return self.__points[i]

    def __iter__(self):
        return iter(self.__points)

    def __str__(self):
        return "\n".join(map(str, self))


n = int(input())
inner = []
for i in range(n):
    k = int(input())
    poly = []
    for i in range(k):
        poly.append(tuple(map(int, input().split())))
    inner.append(random_polygon(poly))

print(random_polygon(1, ((0, 0), (1, 1)), inner))
