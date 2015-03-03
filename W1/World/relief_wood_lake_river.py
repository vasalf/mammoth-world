#!/usr/bin/python3
from random import *
from math import sqrt
import sys

sys.setrecursionlimit(100000)
SIZE = 120
obj_big = 30
obj_small = 120
obj_large = 5
WOOD_SIZE = [101, 152, 210, 253]
WoodSizeSmall = [24, 13, 18, 26]
MuntainSize = [102, 124, 87]
SEA_SIZE = [37, 64, 144, 179]
SeaSizeSmall = [30, 68, 40, 54]
RiverSizeSmall = [27, 19, 17, 23]
RiverSize = [34, 49, 27, 40]
##amount##
grass = '`'
swamp = ';'
meadle = ':'
simple = '"'

sea = 'S'
moves = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, -1), (-1, 1), (-1, -1), (1, 1)]
types = ['`', '"', '"', '"', '"', '"', '"', '"',  "S", "T", '~', 'S', '~', "^"]
##types##
chances = {}
chances["~"] = [0.6, 0.7, 0.3]
chances["^"] = [0.1, 0.2, 0.5]
chances["T"] = [0.9, 0.8, 0.86, 0.6]
#chances["^"] = 
chance = [ 0.3, 0.5, 0.8, 0.9, 1, 1.1, 1.2, 2.5, 1.5, 2, 1.75, 3.3]
class square:
    def __init__(self, typ):
        self.c = typ if typ != 0 else  ''
        self.t = 'ground'

        if typ == 'T':
            self.t = 'tree'
        elif typ == 'S':
            self.t = "water lake"
        elif typ == '~':
            self.t = "water river"
        elif typ == 'O':
            self.t = "ice-berg"
    def __str__(self):
        return str(self.c)
##colors##
color = {}
color["T"] = '42'
color['"'] = '57;103'
color["S"] = '5;34;104'
color["~"] = '5;94;44'
color[swamp] = '2;32;40'
color[meadle] = '7;92'
color[grass] = '1;30;102'
##
def generate_sea_first(arr, i, j):
    if not (0 <= i < len(arr) and 0 <= j < len(arr[0])):
        return 0
    elif arr[i][j].c != '':
        return 0
    arr[i][j] = square(sea)
    temp =  2 * SIZE / sqrt(min(i + 1, SIZE - i) * min(j + 1, SIZE - j))
    if randint(1, SIZE) <=  choice(chance) * temp:
        generate_sea_first(arr, i - 1, j)
    else:
        if random() < 0.1 and i > 0 and  arr[i - 1][j].c == '':
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

def generate(arr, i, j, t, am=0):
    if not(0 <= i < SIZE and 0 <= j < SIZE):
        return 0
        
    if t.t == 'tree' or t.t == 'ground':
        q = [(i, j)]
        index = 0
        if t.t == 'tree':
            if am == 0:
                size = choice(WOOD_SIZE)
        
            else:
                size = choice(WoodSizeSmall)
        else:
             size = randint(SIZE * 12, SIZE * 25)

        print(size)
        while index < size and index < len(q):
            i, j = q[index]
            arr[i][j] = t
            for dx, dy in moves:
                if (0 <= i + dx < SIZE and 0 <= j + dy < SIZE) and random() < 0.76 and arr[i + dx][j + dy].c == '"':
                    q.append((i + dx, j + dy))
                if index % 7 == 0:
                    shuffle(q)
            index += 1
    elif t.t == 'water lake':

        q = [(i, j)]
        index = 0
        if am == 0:
            size = choice(SEA_SIZE)
        else:
            size = choice(SeaSizeSmall)
        print(size)
        while index < size and index < len(q):
            i, j = q[index]
            arr[i][j] = t
            for dx, dy in moves:
                if (0 <= i + dx < SIZE and 0 <= j + dy < SIZE) and random() < 0.76:
                    q.append((i + dx, j + dy))
                    if index % 7 == 0:
                        shuffle(q)
            index += 1
    elif t.t == 'water river':
        index = 0
        q = [(i, j)]
        if am == 0:
            
            size = choice(RiverSize)
        else:
            size = choice(RiverSizeSmall)
        c_moves = moves[:]
        if i < SIZE // 2 and j < SIZE // 2:
            c_moves.extend([(0, -1), (-1, 0), (0, -1), (-1, 0)] * 5)
        elif i < SIZE // 2:
            c_moves.extend([(1, 0), (0, -1), (1, 0), (0, -1)] * 5)
        elif j < SIZE // 2:
            c_moves.extend([(-1, 0), (0, 1), (-1, 0), (0, 1)] * 5)
        else:
            c_moves.extend([(1, 0), (0, 1), (1, 0), (0, 1)]* 5)


        while index < size and index < len(q):
            i, j = q[index]
            arr[i][j] = square('~')
            dx, dy = choice(c_moves)
             
            if (0 <= i + dx < SIZE and 0 <= j + dy < SIZE):
                q.append((i + dx, j + dy))
            if (arr[q[-1][0]][q[-1][1]].t == 'water lake'):
                return 0

            if index % 29 == 0:
                shuffle(q)
            index += 1
class terra:
    def __init__(self):
        self.area = [[square(0)] * SIZE for i in range(SIZE)]
        self.t = 25
        for i in range(SIZE):
            for j in range(SIZE):
                if self.area[i][j].c == "" and sqrt(min(i, SIZE - i) * min(j, SIZE - j)) < SIZE / 9:
                    generate_sea_first(self.area, i, j)
        for i in range(SIZE):
            for j in range(SIZE):
                if self.area[i][j].c == '':
                    self.area[i][j] = square('"')
        for i in range(obj_large):
            i, j = randint(0, SIZE - 1), randint(0, SIZE - 1)
            generate(self.area, i, j, square(choice([swamp, meadle, grass])))
        for i in range(obj_big):
            i, j = randint(10, SIZE - 10), randint(10, SIZE - 10)
            generate(self.area, i, j, square(choice(['S', '~', 'T'])))
        for i in range(obj_small):
            i, j = randint(10, SIZE - 10), randint(10, SIZE - 10)
            generate(self.area, i, j, square(choice(['S', '~', 'T'])), 1)
    def __str__(self):
        for i in range(SIZE):
            for j in range(SIZE):
#                print(str(self.area[i][j]), end='')
                print("\033[" + color[str(self.area[i][j])] + "m" + str(self.area[i][j]) + "\033[0m", end='')
            print()
        return '\n'
            
world = terra()
print(world)
