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


def is_point_in_segment(p, a, b):
    return cross_product(vector(p, a), vector(p, b)) == 0 and \
           dot_product(vector(p, a), vector(p, b)) < 0


def do_segments_intersect(a, b, c, d):
    if cross_product(vector(a, b), vector(c, d)) == 0:
        return is_point_in_segment(a, c, d) or \
               is_point_in_segment(b, c ,d) or \
               is_point_in_segment(c, a, b) or \
               is_point_in_segment(d, a, b)
    else:
        return cross_product(vector(a, c), vector(a, b)) * \
               cross_product(vector(a, b), vector(a, d)) > 0 and \
               cross_product(vector(c, a), vector(c, d)) * \
               cross_product(vector(c, d), vector(c, b)) > 0


def do_segment_and_hor_ray_intersect(p, a, b):
    q = p[0] + 1, p[1]
    if dot_product(vector(p, q), vector(p, a)) < 0 and \
       dot_product(vector(p, q), vector(p, b)) < 0:
        return False
    if


def is_point_in_polygon(p, lst):
    


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
    def __is_intersecting(self, polys, a, b):
        for p in polys:
            k = list(p) + [p[0]]
            for i in range(len(p)):
                if do_segments_intersect(k[i], k[i + 1], a, b):
                    if k[i] not in [a, b] and k[i + 1] not in [a, b]:
                        return True
        return False

    def __is_in_borders(self, p, ld, ru):
        return ld[0] <= p[0] <= ru[0] and ld[1] <= p[0] <= ru[1]

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
            NUM = 2 * (ru[0] - ld[0] + ru[1] - ld[1])
            for i in range(NUM):
                print(i, NUM)
                trial = 0
                generated = False
                while not generated and trial < 100:
                    k = randint(0, len(res) - 1)
                    mn_x = min(res[k][0], res[k - 1][0])
                    mx_x = max(res[k][0], res[k - 1][0])
                    mn_y = min(res[k][1], res[k - 1][1])
                    mx_y = max(res[k][1], res[k - 1][1])
                    if mn_x == mx_x:
                        x = randint(mn_x - (ru[0] - ld[0] + 9) // 10, \
                                    mn_x + (ru[0] - ld[0] + 9) // 10)
                    else:
                        x = randint(mn_x, mx_x)
                    if mn_y == mx_y:
                        y = randint(mn_y - (ru[1] - ld[1] + 9) // 10, \
                                    mn_y + (ru[1] - ld[1] + 9) // 10)
                    else:
                        y = randint(mn_y, mx_y)
                    
                    p = (x, y)
                    if p != res[k] and p != res[k - 1] and \
                       self.__is_in_borders(p, ld, ru) and \
                       not self.__is_intersecting(must_be_in, res[k - 1], \
                       p) and \
                       not self.__is_intersecting(must_be_in, p, res[k]) and \
                       not self.__is_intersecting([res], p, res[k]) and \
                       not self.__is_intersecting([res], p, res[k]) and \
                       not is_point_in_segment(p, res[k - 1], res[k]):
                       generated = True
                       res = res[:k] + [p] + res[k:]
                    trial += 1
            self.__points = res

    def __len__(self):
        return len(self.__points)

    def __getitem__(self, i):
        return self.__points[i]

    def __iter__(self):
        return iter(self.__points)

    def __str__(self):
        return "\n".join(map(str, self))

    def __list__(self):
        return self.__points


n = int(input())
inner = []
for i in range(n):
    k = int(input())
    poly = []
    for i in range(k):
        poly.append(tuple(map(int, input().split())))
    inner.append(random_polygon(poly))

print(random_polygon(1, ((0, 0), (30, 30)), inner))
