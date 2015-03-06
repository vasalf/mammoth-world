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


class terra:
    def __init__(self, lst):
        point = objects.obj('X', SIZE)
        self.area = lst
        self.objects = [point]
        self.size = len(lst)
        self.t = 25

    def go_to(self, x, y):
        self.objects[0].go_to(x, y)

    def look(self, obj=0):
        if obj == 0:
            obj = self.objects[0]
        arr = list(map(lambda a: (a.x, a.y), self.objects))
        i = 1
        while i < len(arr):
            if (obj.x, obj.y) == arr[i]:
                self.area[obj.x][obj.y].attributes.append(self.objects[i])
            i += 1
        print("Here ", obj.x, obj.y, "There is", end = ' ')
        colored.colored_print(\
        self.area[obj.x][obj.y].info(), '\n', "dark_blue", 0, "gray", 1, [])
        print("Height = ", end = ' ')
        colored.colored_print(str(self.area[obj.x][obj.y].height),'\n',  "green", 0, "gray", 1, [])
        self.area[obj.x][obj.y].attributes = []
                
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


def interact_with_user(terra_generator):
    print("\033[31mType Size of the World\033[0m\n")
    world = terra_generator(int(input()))
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

