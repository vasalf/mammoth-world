from random import *
from square import square
am = 0
import sys
sys.setrecursionlimit(1000)
max_depth = 100
moves = [[0, 1], [1, 0], [0, -1], [-1, 0]]
def gradient(arr, height, i, j):
    if am > max_depth:
        return
    if not (0 <= i < len(arr) and 0 <= j < len(arr)):
        return
    height -= randint(-300, 700)
    arr[i][j].height = height
    for dx, dy in moves:
        global am
        am += 1
        gradient(arr, height, i + dx, j + dy)



types = [[0, ';'], [100, 'T'], [200, ':'],  [1000, '`'], [5000, '^']]
size = int(input())
arr = [[square(0) for i in range(size)] for i in range(size)]
for i in range(randint(3, 5)):
    gradient(arr, randint(2000, 3000), randint(0, size - 1), randint(0, size - 1))
    am = 0
for i in range(size):
    for j in range(size):
        k = 1
        while k < len(types) - 1 and types[k][0] < arr[i][j].height:
            k += 1
        k -= 1
        h = arr[i][j].height
        arr[i][j] = square(types[k + 1][1])
        arr[i][j].height = h


for i in range(size):
    for j in range(size):
        print(arr[i][j].c, end = '')
    print()







