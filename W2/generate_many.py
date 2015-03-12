#!/usr/bin/python3

import helpers
import pnglib
import generate_world

n = int(input())
a, b = map(int, input().split())

for i in range(a, b + 1):
    pnglib.save_picture(generate_world.generate_world(n, i * i), "./saved/%d_%d.png" % (n, i * i))
