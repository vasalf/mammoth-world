#!/usr/bin/python3

import helpers
import relief
from generate_mountains import generate_mountains
from square import square
from random import randint
from polygons import random_polygon, is_point_in_polygon


def point_triangle(p):
    return [p, (p[0] + 1, p[1]), (p[0], p[1] + 1)]


def generate_world(n):
    res = [[square('~') for i in range(n)] for j in range(n)]
    # Mountains generation
    mountains = generate_mountains(n, 3 * n ** 2 // 64)
    for i in range(n):
        for j in range(n):
            if mountains[i][j]:
                res[i][j] = square('^')
    mountains_array = []
    for i in range(n):
        for j in range(n):
            if str(res[i][j]) == str(square('^')):
                mountains_array.append((i, j))
                mountains_array.append((i + 1, j))
                mountains_array.append((i, j + 1))
                mountains_array.append((i + 1, j + 1))
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
        must_be_in=[mountains_array, lu_tr, ru_tr, ld_tr, rd_tr])
    for i in range(n):
        for j in range(n):
            if is_point_in_polygon((i + 0.5, j + 0.5), continent):
                if str(res[i][j]) != str(square('^')):
                    res[i][j] = square('"')
    return relief.terra(res)
