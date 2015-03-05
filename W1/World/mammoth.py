from random import *
#import objects
import objects

class mammoth(objects.obj):
    
    def __init__(self, SIZE):
        objects.obj.__init__(self, 'M', SIZE)

    def turn(self):
        dx = choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        dx, dy = dx
        self.move(dx, dy)

def generate_mammoth_herds(SIZE):
    #for i in range(5):
    yield create_mammoth(randrange(0, SIZE), randrange(0, SIZE), SIZE)

def create_mammoth(x, y, SIZE):
    new = mammoth(SIZE)
    new.go_to(x, y)
    return new
