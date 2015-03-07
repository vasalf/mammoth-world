#!/usr/bin/python3

import helpers
import relief
from generate_mountains import generate_mountains
from square import square
from random import randint
from polygons import random_polygon, is_point_in_polygon


def gen(n):
    res = [[square('~') for i in range(n)] for j in range(n)]
    # Mountains generation
    mountains = generate_mountains(3 * n // 4, 3 * n // 4)
    x_plus = randint(2, n // 4)
    y_plus = randint(2, n // 4)
    for i in range(3 * n // 4):
        for j in range(3 * n // 4):
            if mountains[i][j]:
                res[i + x_plus][j + y_plus] = square('^')
    mountains_array = []
    for i in range(n):
        for j in range(n):
            if str(res[i][j]) == str(square('^')):
                mountains_array.append((i, j))
                mountains_array.append((i + 1, j))
                mountains_array.append((i, j + 1))
                mountains_array.append((i + 1, j + 1))
    # Continent shape generation
    continent = random_polygon(None, borders=((0, 0), (n - 1, n - 1)), 
        must_be_in=[mountains_array])
    for i in range(n):
        for j in range(n):
            if is_point_in_polygon((i + 0.5, j + 0.5), continent):
                if str(res[i][j]) != str(square('^')):
                    res[i][j] = square('"')
    return relief.terra(res)


relief.interact_with_user(gen)
