#!/usr/bin/python3

from random import *
from math import sqrt
from square import square
import sys
import colored
import os
import objects
import mammoth

sys.setrecursionlimit(100000)
SIZE = 80
obj_big = 30
obj_small = 120
obj_large = 5
##Random Constants
WOOD_SIZE = [101, 152, 210, 253]
WoodSizeSmall = [91, 103, 95, 88, 127]
MountainSize = [102, 124, 187]
MeadleSize = [300, 176, 145]
SEA_SIZE = [37, 44, 24, 17]
SeaSizeSmall = [30, 8, 40, 54]
RiverSizeSmall = [27, 19, 17, 23]
RiverSize = [34, 49, 27, 40, 14, 121, 75, 97]
###
##World Constants
##amount##

# amount #
grass = '`'
swamp = ';'
meadle = ':'
simple = '"'
mountain = '^'
river = '~'
sea = '~'
tree = 'T'
moves = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, -1), (-1, 1), (-1, -1), (1, 1)]
types = ['`', '"',  "T", '~', 'S', "^", ':', ';']

# types #
height_constants = {}
height_constants[meadle] = [1000, 2000, 30]
height_constants[grass] = [200, 500, 150]
height_constants[swamp] = [-100, 100, 10]
height_constants[tree] = [-50, 150, 30]
##
chances = {}
chances["~"] = [0.6, 0.7, 0.3]
chances["^"] = [0.1, 0.2, 0.5]

chances["T"] = [0.9, 0.8, 0.86, 0.6]
#chances["^"] = 
chance = [ 0.3, 0.5, 0.8, 0.9, 1, 1.1, 1.2, 2.5, 1.5, 2, 1.75, 3.3]
chance = [0.3, 0.5, 0.8, 0.9, 1, 1.1, 1.2, 2.5, 1.5, 2, 1.75, 3.3]

##colors##
# colors #
color = {}
color["T"] = ["T",'', "black", 0, "green", 0, []]
color['"'] = ['"', '', "gray", 1, "yellow", 1, []]
color["S"] = ["S", '', "dark_blue", 1, "dark_blue", 0, []]
color["~"] = ["~", '', "dark_blue", 1, "light_blue", 0, []]
color[sea] = [sea, '', 'dark_blue', 1, "dark_blue", 0, []]
color[swamp] = [swamp, '', "purpur", 0, "green", 1, []]
color[meadle] = [meadle, '', "green", 0, "green", 1, ["light"]]
color[grass] = [grass, '', "yellow", 0, "green", 1, ["hard"]]
color['^'] = [mountain, '', 'black', 0, 'gray', 0, ["light"]]
##



def generate_sea_first(arr, i, j):
    SIZE = len(arr)

    if not (0 <= i < len(arr) and 0 <= j < len(arr[0])):
        return 0
    elif arr[i][j].c != '':
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


def generate(arr, i, j, t, flag=0):
    SIZE = len(arr)
    if not(0 <= i < SIZE and 0 <= j < SIZE):
        return 0

    if t.t == 'tree' or t.t == 'ground':
        height = randint(*height_constants[t.c][:2])
        height_delta = height_constants[t.c][2]
        q = [(i, j)]
        index = 0
        if t.t == 'tree':
            if flag == 0:
                size = choice(WOOD_SIZE)
            else:
                size = choice(WoodSizeSmall)
        else:
            size = randint(SIZE * 2, SIZE * 5)


        while index < size and index < len(q):
            i, j = q[index]
            arr[i][j] = square(t.c)
            arr[i][j].height = height
            height += randint(-height_delta, height_delta)
            for dx, dy in moves:
                if 0 <= i + dx < SIZE and 0 <= j + dy < SIZE:
                    if random() < 0.76 and arr[i + dx][j + dy].t == "ground":
                        q.append((i + dx, j + dy))
                if index % 7 == 0:
                    shuffle(q)
            index += 1
    elif t.t == 'water lake':

        q = [(i, j)]
        index = 0
        if flag == 0:
            size = choice(SEA_SIZE)
        else:
            size = choice(SeaSizeSmall)
 
        while index < size and index < len(q):
            i, j = q[index]
            arr[i][j] = t
            for dx, dy in moves:
                if 0 <= i + dx < SIZE and 0 <= j + dy < SIZE:
                    if random() < 0.76 and arr[i + dx][j + dy].t == "ground":
                        q.append((i + dx, j + dy))
            if index % 7 == 0:
                shuffle(q)
            index += 1
    elif t.t == 'water river' or t.t == 'mountain':
        index = 0
        q = [(i, j)]
        height = randint(2000, 4000)
        if t.t == 'water river':
            
            if flag == 0:
                size = choice(RiverSize)
            else:
                size = choice(RiverSizeSmall)
        else:
            size = choice(MountainSize)
        c_moves = moves[:]
        if i < SIZE // 2 and j < SIZE // 2:
            c_moves.extend([(0, -1), (-1, 0), (0, -1), (-1, 0)] * 5)
        elif i < SIZE // 2:
            c_moves.extend([(1, 0), (0, -1), (1, 0), (0, -1)] * 5)
        elif j < SIZE // 2:
            c_moves.extend([(-1, 0), (0, 1), (-1, 0), (0, 1)] * 5)
        else:
            c_moves.extend([(1, 0), (0, 1), (1, 0), (0, 1)] * 5)
        while index < size and index < len(q):
            i, j = q[index]
            arr[i][j] = square(t.c)
            dx, dy = choice(c_moves)
            if t.t == "water river":
                height -= randint(300, 400)
            else:
                height -= randint(-400, 400)
            arr[i][j].height = height
            if (0 <= i + dx < SIZE and 0 <= j + dy < SIZE) and arr[i + dx][j + dy].t == "ground":
                q.append((i + dx, j + dy))
            else:
                dx, dy = choice(c_moves)
                if (0 <= i + dx < SIZE and 0 <= j + dy < SIZE) and arr[i + dx][j + dy].t == "ground":
                    q.append((i + dx, j + dy))
                
            for idx in range(len(moves)):
                if (0 <= i + moves[idx][0] < SIZE) and (0 <= j + moves[idx][1] < SIZE) and \
                (arr[i + moves[idx][0]][j + moves[idx][1]].t == "water lake" or\
                arr[i + moves[idx][0]][j + moves[idx][1]].t == "sea water"):
                    print(1)
                    return 0
            if (arr[q[-1][0]][q[-1][1]].t == 'water lake'):
                return 0

            if index % 29 == 0:
                shuffle(q)
            index += 1
        return q

class terra:
    def __init__(self, SIZE):
    ##  
        self.coord = [0, 0]
        if type(SIZE) == list:
            self.area = SIZE
            return 
   ##
        self.size = SIZE
        global obj_small
        obj_small = int(SIZE ** (1.5) // 10)
        global obj_big
        obj_big = SIZE // 5
        global obj_large
        obj_large = int(SIZE ** 0.5 / 2)
        self.area = [[square(0)] * SIZE for i in range(SIZE)]
        point = objects.obj('X', SIZE)
        self.objects = [point]
        self.t = 25
        for i in range(SIZE):
            for j in range(SIZE):
                if self.area[i][j].c == "":
                    if sqrt(min(i, SIZE - i) * min(j, SIZE - j)) < SIZE / 9:
                        generate_sea_first(self.area, i, j)
        for i in range(SIZE):
            for j in range(SIZE):
                if self.area[i][j].c == '':
                    self.area[i][j] = square('"')
        mountain_amount = randrange(3, 7)
        for i in range(mountain_amount):
            k, j = randint(0, int(SIZE * 0.8)), randint(10, int(SIZE * 0.8))
            curr_mount = generate(self.area, k, j, square(mountain))
            #self.Print(50, 50)
            for i in range(2):
                k, j = choice(curr_mount)
                generate(self.area, k, j, square(meadle))
            for i in range(2):
                k, j = choice(curr_mount)

                generate(self.area, k, j, square(river))
        for i in range(obj_big):
            i, j = randint(10, int(SIZE * 0.8)), randint(10, int(SIZE * 0.8))
            generate(self.area, i, j, square(choice(['S', 'T'])))
        for i in range(obj_large):
            
            i, j = randint(0, SIZE - 1), randint(0, SIZE - 1)
            generate(self.area, i, j, square(choice([swamp, grass])))
        for i in range(obj_small):
            i, j = randint(10, int(SIZE * 0.8)), randint(10, int(SIZE * 0.8))
            generate(self.area, i, j, square(choice(['S', 'T'])), 1)
    def go_to(self, x, y):
        self.objects[0].go_to(x, y)
    def look(self, obj=0):
        if obj == 0:
            obj = self.objects[0]
        arr = list(map(lambda a: (a.x, a.y), self.objects))
        i = 1
        while i < len(arr):
            if (obj.x, obj.y) == arr[i]:
                world.area[obj.x][obj.y].attributes.append(self.objects[i])
            i += 1
        print("Here ", obj.x, obj.y, "There is", end = ' ')
        colored.colored_print(\
        world.area[obj.x][obj.y].info(), '\n', "dark_blue", 0, "gray", 1, [])
        print("Height = ", end = ' ')
        colored.colored_print(str(world.area[obj.x][obj.y].height),'\n',  "green", 0, "gray", 1, [])
        world.area[obj.x][obj.y].attributes = []
            
   
    
    def Print(self, obj):
        os.system("clear")
        x, y = obj.x, obj.y
        x1 = max(x - 15, 0)
        x2 = min(x + 15, self.size)
        y1 = max(y - 50, 0)
        y2 = min(y + 50, self.size)
        arr = list(map(lambda a: (a.x, a.y), self.objects))
        print(arr[1:])
        for i in range(x1, x2):
            for j in range(y1, y2):
#                print(str(self.area[i][j]), end='')
                if (i, j) in arr:
                    curr_arr = self.objects[arr.index((i, j))].color_args()
                    colored.colored_print(curr_arr[0], curr_arr[1],
                    curr_arr[2], curr_arr[3], color[str(self.area[i][j])][4],
                    color[str(self.area[i][j])][5], curr_arr[6])
                else:
                    colored.colored_print(*color[str(self.area[i][j])])
            colored.colored_print(str(i), '\n', 'red' if i == self.objects[0].x else "black", 0, "gray", 0, [])
        print(y1)
        return '\n'
            
print("\033[31mType Size of the World\033[0m\n")
world = terra(int(input()))
print("New World is created\n")
#==================
#MAMMOTH GENERATION
for new_mammoth in mammoth.generate_mammoth_herds(SIZE, world):
    world.objects.append(new_mammoth)
    #world.area[new_mammoth.x][new_mammoth.y].obj = world.objects[-1]
print("Mammoths generated\n")
#==================
while True:
    s = input()
    if s == 'go_to':
        a, b = map(int, input().split())
        world.go_to(a, b)
        world.Print(world.objects[0])
    if s == 'up':
        print(world.objects[0].move(world, -1, 0))
        world.Print(world.objects[0]) 
        world.look()
    elif s == 'left':
        print(world.objects[0].move(world, 0, -1))
        world.Print(world.objects[0]) 
        world.look()
    elif s == 'right':
        print(world.objects[0].move(world, 0, 1))
        world.Print(world.objects[0]) 
        world.look()
    elif s == 'down':
        print(world.objects[0].move(world, 1, 0))
        world.Print(world.objects[0]) 
        world.look()
    elif s == 'look':
        world.look()
    elif s == "new":
        s = input().split()
        world.objects.append(objects.obj(s[0], world.size))
        world.objects[-1].go_to(int(s[1]), int(s[2]))

    elif s == "print":
        world.Print(world.objects[0])
    elif s == "turn":
        for obj in world.objects[1:]:
            obj.turn(world)
        world.Print(world.objects[0])

