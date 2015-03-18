#!/usr/bin/python3

"""This is a library that provides geometry classes and functions

             It is a part of mammoth-world project
           (https://github.com/vasalf/mammoth-world)

"""

from random import *
from math import log

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
        if cross_product(vector(self.__first, self),
                         vector(self.__first, other)) == 0:
            return sq_point_distance(self.__first, self) < \
                   sq_point_distance(self.__first, other)
        else:
            return cross_product(vector(self.__first, self),
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


"""Here are some geometry helper functions

"""


def is_point_in_segment(p, a, b):
    return cross_product(vector(p, a), vector(p, b)) == 0 and \
           dot_product(vector(p, a), vector(p, b)) <= 0


def do_segments_intersect(a, b, c, d):
    if cross_product(vector(a, b), vector(c, d)) == 0:
        return is_point_in_segment(a, c, d) or \
               is_point_in_segment(b, c, d) or \
               is_point_in_segment(c, a, b) or \
               is_point_in_segment(d, a, b)
    else:
        return cross_product(vector(a, c), vector(a, b)) * \
               cross_product(vector(a, b), vector(a, d)) >= 0 and \
               cross_product(vector(c, a), vector(c, d)) * \
               cross_product(vector(c, d), vector(c, b)) >= 0


def do_segments_strongly_intersect(a, b, c, d):
    if not do_segments_intersect(a, b, c, d):
        return False
    if cross_product(vector(a, b), vector(c, d)) == 0:
        if a == c:
            return not is_point_in_segment(d, a, b) and \
                   not is_point_in_segment(b, c, d)
        if a == d:
            return not is_point_in_segment(c, a, b) and \
                   not is_point_in_segment(b, c, d)
        if b == c:
            return not is_point_in_segment(d, a, b) and \
                   not is_point_in_segment(a, c, d)
        if c == d:
            return not is_point_in_segment(c, a, b) and \
                   not is_point_in_segment(a, c, d)
    return not is_point_in_segment(a, c, d) and \
        not is_point_in_segment(b, c, d) and \
        not is_point_in_segment(c, a, b) and \
        not is_point_in_segment(d, a, b)


def signum(a):
    if a < 0:
        return -1
    elif a == 0:
        return 0
    else:
        return 1


def do_segment_and_hor_ray_intersect(p, a, b):
    q = p[0] + 1, p[1]
    if b[1] == p[1]:
        return False
    return signum(cross_product(vector(p, q), vector(p, a))) != \
        signum(cross_product(vector(p, q), vector(p, b))) and \
        cross_product(vector(p, a), vector(p, b)) > 0


def is_point_in_polygon(p, lst):
    num = 0
    for i in range(len(lst)):
        if is_point_in_segment(p, lst[i - 1], lst[i]):
            return True
        if lst[i][1] == lst[i - 1][1]:
            continue
        if lst[i - 1][1] > lst[i][1] and \
           do_segment_and_hor_ray_intersect(p, lst[i], lst[i - 1]):
            num += 1
        elif lst[i - 1][1] < lst[i][1] and \
                do_segment_and_hor_ray_intersect(p, lst[i - 1], lst[i]):
            num += 1
    return (num & 1) == 1


def middle(a, b):
    return (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
