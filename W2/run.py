#!/usr/bin/python3

import helpers
import relief
from square import square

def gen(n):
    return relief.terra([[square('"') for i in range(n)] for j in range(n)])

relief.interact_with_user(gen)
