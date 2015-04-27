#!/usr/bin/python3

from square import square
from random import randint, sample
from collections import deque
from math import sqrt


def generate_line(world):
    def good_index(i, j, n):
        return 0 <= i < n and 0 <= j < n
    
    def get_direction(i, j, scoast):
        d = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, -1))
        grounds = []
        coasts = []
        for dx, dy in d:
            if world.area[i + dx][j + dy].t == "ground":
                if (i + dx, j + dy) in scoast:
                    coasts.append((dx, dy))
                else:
                    grounds.append((dx, dy))
        if len(grounds):
            return sample(grounds, 1)[0]
        else:
            return sample(coasts, 1)[0]

    def add_direction(i, j, d):
        ds = ((-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1))
        for ind in range(len(ds)):
            if d[ind] == (i, j):
                d += 4 * [ds[ind]]
                d += 4 * [ds[(ind + 1) % len(ds)]]
                d += 4 * [ds[ind - 1]]
  
    n = len(world.area)
    
    coast = []
    d = ((-1, 0), (1, 0), (0, -1), (0, 1))
    for i in range(n):
        for j in range(n):
            if world.area[i][j].t == "ground":
                f = False
                for dx, dy in d:
                    if good_index(i + dx, j + dy, n) and world.area[i + dx][j + dy].t != "ground":
                        f = True
                if f:
                    coast.append((i, j))
    scoast = set(coast)

    x, y = sample(coast, 1)[0]
    ans = [[False for i in range(n)] for j in range(n)]
    d = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, -1)]
    dx, dy = get_direction(x, y, scoast)
    add_direction(dx, dy, d)
    cnt = 0
    bcnt = 0
    while ((x, y) not in scoast or (cnt < n and bcnt < 3)) and cnt < 10 * n:
        ans[x][y] = True
        dx, dy = sample(d, 1)[0]
        if good_index(x + dx, y + dy, n) and world.area[x + dx][y + dy].t == "ground":
            x += dx
            y += dy
            cnt += 1
        elif good_index(x + dx, y + dy, n) and world.area[x + dx][y + dy].t != "ground":
            d = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, -1)]
            dx, dy = get_direction(x, y, scoast)
            add_direction(dx, dy, d)
            bcnt += 1

    ans[x][y] = True

    return ans


def generate_mountains(world, stat_bar):
    n = len(world.area)
    k = (n + 199) // 200
    for i in range(k):
        ans = generate_line(world)
        for i in range(n):
            for j in range(n):
                if ans[i][j]:
                    world.area[i][j] = square('^')
        stat_bar.update(1 / k)
    stat_bar.finish()


def generate_mountains_bfs(world, stat_bar):
    def good_index(i, j, n):
        return 0 <= i < n and 0 <= j < n

    INF = 1791791791    

    def bfs(world, mts, should_add_coast=True):
        q = deque(mts)
        n = len(world.area)
        d = ((-1, 0), (1, 0), (0, -1), (0, 1))
        if should_add_coast:
            for i in range(n):
                for j in range(n):
                    f = False                
                    for dx, dy in d:
                        if good_index(i + dx, j + dy, n) and world.area[i + dx][j + dy].t == "water sea":
                            f = True
                    if f and world.area[i][j].t == "ground":
                        q.append((i, j))
        dist = [[INF for i in range(n)] for j in range(n)]
        for i, j in q:
            dist[i][j] = 0
        while len(q):
            i, j = q.popleft()
            for dx, dy in d:
                if good_index(i + dx, j + dy, n) and dist[i + dx][j + dy] == INF and world.area[i + dx][j + dy].t == "ground":
                    dist[i + dx][j + dy] = dist[i][j] + 1
                    q.append((i + dx, j + dy))
        return dist

    n = len(world.area)
    num = int(n // 10)

    mountains = []
    for i in range(num):
        dists = bfs(world, mountains)
        mxi, mxj = 0, 0
        for i in range(n):
            for j in range(n):
                if (dists[i][j] > dists[mxi][mxj] or dists[mxi][mxj] == INF) and dists[i][j] != INF:
                    mxi, mxj = i, j
        mountains.append((mxi, mxj))
        stat_bar.update(1 / num)
    
    mxdist = int(n * sqrt(n))
    possible_mts = [[] for i in range(mxdist)]
    dists = bfs(world, mountains)

    for i in range(n):
        for j in range(n):
            if 0 < dists[i][j] <= mxdist:
                possible_mts[dists[i][j] - 1].append((i, j))
    for dst in range(mxdist):
        mountains += sample(possible_mts[dst], min(len(possible_mts[dst]), num))

    for i, j in mountains:
        world.area[i][j] = square('^')

    stat_bar.finish()


