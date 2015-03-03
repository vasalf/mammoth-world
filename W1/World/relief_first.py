#!/usr/bin/python3
from random import *
from math import sqrt
import sys

sys.setrecursionlimit(100000)
SIZE = 100
simple = '0'
sea = 's'
types = ['0', '0', '0', '0', '0', '0', '0', '0', "s", "T"]
symbols = {}
chances = {}
chances["s"] = [0.6, 0.7, 0.3]
chances["^"] = [0.1, 0.2, 0.5]
chances["T"] = [0.9, 0.8, 0.86, 0.6]
symbols["T"] = "T"
symbols[0] = ''
symbols['0'] = '"'
symbols['^'] = '^'
chance = [0.3, 0.5, 0.8, 0.9, 1, 1.1, 1.2, 2.5, 1.5, 2, 1.75, 3.3]
symbols[sea] = '~'


class square:
    def __init__(self, typ):
        self.c = symbols[typ]

    def __str__(self):
        return self.c


color = {}
color["T"] = '5;42'
color['"'] = '32;103'
color["~"] = '34;104'


def generate_sea_first(arr, i, j):
    if not (0 <= i < len(arr) and 0 <= j < len(arr[0])):
        return 0
    elif arr[i][j].c != "":
        return 0
    arr[i][j] = square(sea)
    temp = 2 * SIZE / sqrt(min(i + 1, SIZE - i) * min(j + 1, SIZE - j))
    if randint(1, SIZE) <= choice(chance) * temp:
        generate_sea_first(arr, i - 1, j)
    else:
        if random() < 0.1 and i > 0 and arr[i - 1][j].c == '':
            arr[i - 1][j] = square(simple)
    if randint(1, SIZE) <= choice(chance) * temp:
        generate_sea_first(arr, i, j - 1)
    else:
        if random() < 0.1 and j > 0 and arr[i][j - 1].c == '':
            arr[i][j - 1] = square(simple)
    if randint(1, SIZE) <= choice(chance) * temp:
        generate_sea_first(arr, i, j + 1)
    else:
        if random() < 0.1 and j < SIZE - 1 and arr[i][1 + j].c == '':
            arr[i][j + 1] = square(simple)
    if randint(1, SIZE) <= choice(chance) * temp:
        generate_sea_first(arr, i + 1, j)
    else:
        if random() < 0.1 and i < SIZE - 1 and arr[i + 1][j].c == '':
            arr[i + 1][j] = square(simple)


def generate(arr, i, j, t):
    if 0 <= i < SIZE and 0 <= j < SIZE:
        return 0
    if random() < choice(chances[t]):
        generate(arr, i, j + 1, t)
    if random() < choice(chances[t]):
        generate(arr, i - 1, j, t)
    if random() < choice(chances[t]):
        generate(arr, i + 1, j, t)
    if random() < choice(chances[t]):
        generate(arr, i, j - 1, t)


class terra:
    def __init__(self):
        self.area = [[square(0)] * SIZE for i in range(SIZE)]
        self.t = 25
        for i in range(SIZE):
            for j in range(SIZE):
                if self.area[i][j].c == "":
                    if min(i, SIZE - i) * min(j, SIZE - j) < (SIZE / 9) ** 2:
                        generate_sea_first(self.area, i, j)
        for i in range(SIZE):
            for j in range(SIZE):
                if self.area[i][j].c == '':
                    self.area[i][j] = square(choice(list(types)))

    def __str__(self):
        for i in range(SIZE):
            for j in range(SIZE):
                print("\033[" + color[str(self.area[i][j])] + "m" +
                      str(self.area[i][j]) + "\033[0m", end='')
            print()
        return '\n'


world = terra()
print(world)
