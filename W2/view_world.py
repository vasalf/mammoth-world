#!/usr/bin/python3

import helpers
import pnglib
from generate_world import generate_world


print("Type the Size of the World")
pnglib.watch_terra(generate_world(int(input())))
