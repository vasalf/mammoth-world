#!/usr/bin/python3

"""This is a library that provides classes to work with random polygons.

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
    def __is_point_in_borders(self, p, res=None):
        if res is None:
            res = self
        for i in range(len(res)):
            if is_point_in_segment(p, res[i], res[i - 1]):
                return True
        return False

    def is_point_strongly_in(self, p, res=None):
        if res is None:
            res = self
        return is_point_in_polygon(p, res) and \
            not self.__is_point_in_borders(p, res)

    def __is_segment_strongly_intersecting_borders(self, a, b, res=None):
        if res is None:
            res = self
        for i in range(len(res)):
            if do_segments_strongly_intersect(a, b, res[i], res[i - 1]):
                return True
        return False

    def __is_segment_intersecting_borders(self, a, b, res=None):
        if res is None:
            res = self
        for i in range(len(res)):
            if do_segments_intersect(a, b, res[i], res[i - 1]):
                return True
        return False

    def __does_segment_contain_a_vertice(self, a, b, res=None):
        if res is None:
            res = self
        for p in res:
            if is_point_in_segment(p, a, b):
                return True
        return False

    def __is_intersecting(self, p, a, b, i=None):
        if self.__is_segment_strongly_intersecting_borders(a, b, p):
            return True
        if self.__is_point_in_borders(a, p) and \
           self.__is_point_in_borders(b, p):
            return self.__does_segment_contain_a_vertice(a, b, p) or \
                   self.is_point_strongly_in(middle(a, b), p)
        if self.is_point_strongly_in(a, p) or \
           self.is_point_strongly_in(b, p):
            return True
        return False

    def __is_intersecting_system(self, a, b, system, res=None):
        if res is None:
            res = self
        i = 0
        for p in system:
            if self.__is_intersecting(p, a, b, i):
                return True
            i += 1
        return False

    def __is_in_borders(self, ld, ru, p):
        return ld[0] <= p[0] <= ru[0] and ld[1] <= p[1] <= ru[1]

    def __init__(self, arg, borders=None, must_be_in=None, stat_bar=None, random_par=16):
        if isinstance(arg, list):
            # Then just make a polygon from list
            self.__points = arg[:]
        elif isinstance(arg, random_polygon):
            # Then just make a COPY of polygon
            self.__points = arg.__points[:]
        else:
            # Then generate random points
            assert arg is None
            assert borders is not None
            assert isinstance(must_be_in, list)
            ld, ru = borders
            size = ru[0] - ld[0]

            res = convex(unite(must_be_in))
            mem = res[:]

            k = 0
            trial = 0
            cur_t = 0
            while k < len(res):
                if sq_point_distance(res[k], res[k - 1]) <= random_par:
                    k += 1
                    trial = 0
                    if k < len(res) and mem[(cur_t + 1) % len(mem)] == res[k]:
                        cur_t += 1
                        if stat_bar is not None:
                            stat_bar.update(1 / len(mem))
                    continue
                mn_x = min(res[k][0], res[k - 1][0])
                mx_x = max(res[k][0], res[k - 1][0])
                mn_y = min(res[k][1], res[k - 1][1])
                mx_y = max(res[k][1], res[k - 1][1])
                if mx_x - mn_x < 3:
                    x = randint(mn_x - (ru[0] - ld[0] + 9) // 20,
                                mn_x + (ru[0] - ld[0] + 9) // 20)
                else:
                    x = randint(mn_x, mx_x)
                if mx_y - mn_y < 3:
                    y = randint(mn_y - (ru[1] - ld[1] + 9) // 20,
                                mn_y + (ru[1] - ld[1] + 9) // 20)
                else:
                    y = randint(mn_y, mx_y)

                p = (x, y)

                if (p != res[k]) and (p != res[k - 1]) and \
                    (not self.__is_intersecting_system(res[k], p,
                    must_be_in)) and \
                    (not self.__is_intersecting_system(p, res[k - 1],
                    must_be_in)) and \
                    (not self.__is_segment_strongly_intersecting_borders(
                    res[k], p, res)) and \
                    (not self.__is_segment_strongly_intersecting_borders(
                    res[k - 1], p, res)) and \
                    self.__is_in_borders(ld, ru, p) and \
                    not self.__is_point_in_borders(p, res):
                    # #
                    res = res[:k] + [p] + res[k:]
                trial += 1
                if trial == 100:
                    trial = 0
                    k += 1
                    if k < len(res) and mem[(cur_t + 1) % len(mem)] == res[k]:
                        cur_t += 1
                        if stat_bar is not None:
                            stat_bar.update(1 / len(mem))

            self.__points = res
            if stat_bar is not None:
                stat_bar.finish()

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
