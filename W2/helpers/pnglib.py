#!/usr/bin/python3

import os
os.system("cat helpers/necessary/png_warning.txt")
import png
import helpers
from relief import terra

png_viewer = "sxiv"


def str_to_pix(s):
    res = []
    for i in range(0, len(s), 2):
        res.append(int(s[i:i + 2], 16))
    return res


# Color constants
width = 5
sea_bg = str_to_pix("0033CC")
sea = [sea_bg * width] * width
plain_bg = str_to_pix("FFCC00")
plain = [plain_bg * width] * width
mountain_bg = str_to_pix("FFFFFF")
mountain = [mountain_bg * width] * width


def pixmap_to_pixlist(pixmap):
    h, w = len(pixmap) * width, len(pixmap[0]) * width
    res = [[0 for i in range(3 * w)] for j in range(h)]
    for i in range(len(pixmap)):
        for j in range(len(pixmap[0])):
            for k in range(width):
                for t in range(3 * width):
                    res[i * width + k][j * 3 * width + t] = pixmap[i][j][k][t]
    return res


def terra_to_pixmap(world):
    res = [[sea for i in range(world.size)] for j in range(world.size)]
    for i in range(world.size):
        for j in range(world.size):
            if world.area[i][j].t == "sea water":
                res[i][j] = sea
            elif world.area[i][j].t == "ground":
                res[i][j] = plain
            elif world.area[i][j].t == "mountain":
                res[i][j] = mountain
    return res


def write_pixlist(pixlist, filename):
    f = open(filename, "wb")
    w = png.Writer(len(pixlist), len(pixlist))
    w.write(f, pixlist)
    f.close()


def watch_terra(world):
    pixlist = pixmap_to_pixlist(terra_to_pixmap(world))
    write_pixlist(pixlist, "/tmp/world.png")
    os.system(png_viewer + " /tmp/world.png")

