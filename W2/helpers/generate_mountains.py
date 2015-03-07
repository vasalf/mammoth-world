#!/usr/bin/python3

"""This is a file that provides function that generates random mauntain massives

                    It is a part of mammoth-world project
                  (https://github.com/vasalf/mammoth-world)

"""

import sys
from random import *

"""A place to import modules is up to thar comment

"""
__author__ = "vasalf"

sys.setrecursionlimit(100000)

"""That function generates a massif

- amount is number of mountains in the massif
- wmap is a reference to two-dimensional boolean list - a world map
- x, y are coordinates to begin
- last is last choice of direction

"""

def generate_massif(amount, wmap, x, y, last = (-1, 0)):
    if amount == 0:
        return 0
    directions = set([(-1, 0), (1, 0), (0, -1), (0, 1)])
    while len(directions):
        next_direction = last
        if last not in directions or random() * 10 > 4:
            next_direction = sample(directions, 1)[0]
        new_x = x + next_direction[0]
        new_y = y + next_direction[1]
        if new_x >= 0 and new_y >= 0 and new_x < len(wmap) and \
          new_y < len(wmap) and not wmap[new_x][new_y]:
            wmap[new_x][new_y] = True
            return 1 + generate_massif(amount - 1, wmap, new_x, new_y)
        else:
            directions.remove(next_direction)
    return 0

"""That function generates some massifes on a world map

- size is a world size
- amount is number of mountains to create

return value is a two-simensional boolean list

"""

def generate_mountains(size, amount):
    res = [[False for i in range(size)] for j in range(size)]
    while amount > 0:
        to_create = (random() ** 10) * amount
        x = randint(0, size - 1)
        y = randint(0, size - 1)
        amount -= generate_massif(to_create, res, x, y)
    return res
