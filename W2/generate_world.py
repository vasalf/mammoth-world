#!/usr/bin/python3

import helpers
import relief
from generate_mountains import generate_mountains
from square import square
from random import randint, sample
from polygons import random_polygon, is_point_in_polygon
from statusbar import statusbar


def point_triangle(p):
    return [p, (p[0] + 1, p[1]), (p[0], p[1] + 1)]


def generate_continent(n):
    res = [[square('~') for i in range(n)] for j in range(n)]
    stat_bar = statusbar([
        ("Generating world shape", "Finished generating world shape"),
        ("Making world map", "Finished making world map")],
        clock_enabled=True)
    stat_bar.Print()
    # Continent shape generation
    lu_pt = randint(n // 8, n // 4), randint(n // 8, n // 4)
    lu_tr = point_triangle(lu_pt)
    ru_pt = randint(n // 8, n // 4), \
            randint(3 * n // 4, 7 * n // 8)
    ru_tr = point_triangle(ru_pt)
    ld_pt = randint(3 * n // 4, 7 * n // 8), \
            randint(n // 8, n // 4)
    ld_tr = point_triangle(ld_pt)
    rd_pt = randint(3 * n // 4, 7 * n // 8), \
            randint(3 * n // 4, 7 * n // 8)
    rd_tr = point_triangle(rd_pt)
    continent = random_polygon(None, borders=((0, 0), (n - 1, n - 1)), 
        must_be_in=sample([lu_tr, ru_tr, ld_tr, rd_tr], 3),
        stat_bar=stat_bar)
    # World map generation
    for i in range(n):
        for j in range(n):
            if is_point_in_polygon((i + 0.5, j + 0.5), continent):
                res[i][j] = square('"')
        stat_bar.update(1 / n)
    stat_bar.finish()
    return res


def generate_world(n):
    res = [[square('~') for i in range(n)] for j in range(n)]
    t1 = generate_continent(n)
    t2 = generate_continent(n)
    for i in range(n):
        for j in range(n):
            if t1[i][j].t == "ground" or t2[i][j].t == "ground":
                res[i][j] = square('"')
    return relief.terra(res)
