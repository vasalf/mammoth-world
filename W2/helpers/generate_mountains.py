#!/usr/bin/python3

"""This is a file that provides function that generates random mauntain massives

                    It is a part of mammoth-world project
                  (https://github.com/vasalf/mammoth-world)

"""

import sys
from random import *
import copy

"""A place to import modules is up to thar comment

"""
__author__ = "vasalf"

sys.setrecursionlimit(100000)

"""That function generates a massif

- amount is number of mountains in the massif
- wmap is a reference to two-dimensional boolean list - a world map
- x, y are coordinates to begin
- directions is a choice of available directions

"""

def generate_massif(amount, wmap, x, y, directions):
    if amount == 0:
        return 0
    to_go = copy.copy(directions)
    while len(to_go):
        next_direction = sample(to_go, 1)[0]
        new_x = x + next_direction[0]
        new_y = y + next_direction[1]
        if new_x >= 0 and new_y >= 0 and new_x < len(wmap) and \
          new_y < len(wmap) and not wmap[new_x][new_y]:
            wmap[new_x][new_y] = True
            return 1 + generate_massif(amount - 1, wmap, new_x, new_y, 
                directions)
        else:
            to_go.remove(next_direction)
    return 0

"""That function generates some massifes on a world map

- size is a world size
- amount is number of mountains to create

return value is a two-dimensional boolean list

"""

def generate_mountains(size, amount):
    res = [[False for i in range(size)] for j in range(size)]
    while amount > 0:
        to_create = max(6 * int(random() * amount) // size, 1)
        x = randint(0, size - 1)
        y = randint(0, size - 1)
        direction = [0, 0]
        if x > size - x:
            direction[0] = 1
        else:
            direction[0] = -1
        if y > size - y:
            direction[1] = 1
        else:
            direction[1] = -1
        direction = tuple(direction)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), \
                      (1, 1), (1, -1), (-1, 1), (-1, -1)]
        directions += 5 * [direction]
        directions += 5 * [(direction[0], 0)]
        directions += 5 * [(0, direction[1])]
        amount -= generate_massif(to_create, res, x, y, directions)
    return res
