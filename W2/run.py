#!/usr/bin/python3

import helpers
import relief
from generate_mountains import generate_mountains
from square import square
from random import randint


def gen(n):
    res = [[square('"') for i in range(n)] for j in range(n)]
    # Mountains generation
    mountains = generate_mountains(3 * n // 4, 3 * n // 4)
    x_plus = randint(2, n // 4)
    y_plus = randint(2, n // 4)
    for i in range(3 * n // 4):
        for j in range(3 * n // 4):
            if mountains[i][j]:
                res[i + x_plus][j + y_plus] = square('^')
    return relief.terra(res)


relief.interact_with_user(gen)
