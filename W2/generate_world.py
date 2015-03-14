#!/usr/bin/python3

import helpers
import relief
from generate_mountains import generate_mountains
from square import square
from random import randint, sample
from polygons import random_polygon, is_point_in_polygon
from polygons import do_segments_intersect
from statusbar import statusbar


def point_triangle(p):
    return [p, (p[0] + 1, p[1]), (p[0], p[1] + 1)]


def gen_precalc(n, continent, stat_bar):
    precalc = [[0 for i in range(n)] for j in range(n)]
    for k in range(len(continent)):
        if continent[k - 1][0] < continent[k][0]:
            bl = continent[k - 1][0]
            br = continent[k][0]
            d = 0.5
        else:
            bl = continent[k][0]
            br = continent[k - 1][0]
            d = 0.5
        for i in range(bl, br, 1):
            x = i + d
            lt, rt = 0, n
            while lt < rt - 1:
                mid = (rt + lt) // 2
                if do_segments_intersect((x, mid + 0.5), (x, n), continent[k - 1], continent[k]):
                    lt = mid
                else:
                    rt = mid
            precalc[i][rt] += 1
        stat_bar.update(1 / len(continent))
    stat_bar.finish()
    return precalc


def generate_continent(n, random_par=16):
    res = [[square('~') for i in range(n)] for j in range(n)]
    stat_bar = statusbar([
        ("Generating world shape", "Finished generating world shape"),
        ("Preparing to make world map", "Prepared to make world map"),
        ("Making world map", "Finished making world map")],
        clock_enabled=True,
        task_length = 30)
    stat_bar.Print()
    # Continent shape generation
    lu_pt = randint(n // 8, n // 4), randint(n // 8, n // 4)
    lu_tr = point_triangle(lu_pt)
    ru_pt = randint(n // 8, n // 4), \
            randint(3 * n // 4, 7 * n // 8)
    ru_tr = point_triangle(ru_pt)
    ld_pt = randint(3 * n // 4, 7 * n // 8), \
            randint(n // 8, n // 4)
    ld_tr = point_triangle(ld_pt)
    rd_pt = randint(3 * n // 4, 7 * n // 8), \
            randint(3 * n // 4, 7 * n // 8)
    rd_tr = point_triangle(rd_pt)
    continent = random_polygon(None, borders=((0, 0), (n - 1, n - 1)), 
        must_be_in=sample([lu_tr, ru_tr, ld_tr, rd_tr], 3),
        stat_bar=stat_bar,
        random_par=random_par)
    # Preparing to make world map
    precalc = gen_precalc(n, continent, stat_bar)
    # World map generation
    for i in range(n):
        cur = 0
        for j in range(n):
            cur += precalc[i][j]
            if cur % 2:
                res[i][j] = square('"')
        stat_bar.update(1 / n)
    stat_bar.finish()
    return res


def generate_world(n, random_par=16):
    res = [[square('~') for i in range(n)] for j in range(n)]
    t1 = generate_continent(n, random_par)
    t2 = generate_continent(n, random_par)
    for i in range(n):
        for j in range(n):
            if t1[i][j].t == "ground" or t2[i][j].t == "ground":
                res[i][j] = square('"')
    return relief.terra(res)
