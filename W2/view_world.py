#!/usr/bin/python3

import helpers
import pnglib
from generate_world import generate_world

pnglib.watch_terra(generate_world(int(input())))
