from random import *
import objects

class mammothHerd():
    
    def __init__(self):
        self.mammoths = []

class mammoth(objects.obj):
    
    def __init__(self, SIZE, ID, isLeader=False, age=0, hp=10, water=100, food=100):
        objects.obj.__init__(self, 'M', SIZE)
        self.age, self.hp, self.water, self.food = age, hp, water, food
        self.ID = ID
        self.isLeader = isLeader

    def wanderAround(self):
        dx = choice([-1, 0, 1])
        dy = choice([-1, 0, 1])
        self.move(dx, dy)

    def getLeaderCoord():
        xy = Herds[herdID]
        return xy.x, xy.y

    def dist(x, y):
        return abs(x - self.x) + abs(y - self.y)

    def followLeader():
       x, y = self.getLeader()
       d = self.dist(x, y)
       if d > len(Herd[herdID].mammoths) // 2:
           self.move_to_leader()
       else:
            self.wanderAround()

    def turn(self):
        if self.isLeader:
            self.wanderAround()
        else:
            self.followLeader()

def generate_mammoth_herds(SIZE):
    for ID in range(1):
        Herds.append(generate_mammoth_herd(SIZE, 6, ID))

def generate_mammoth_herd(SIZE, amount, ID):
    herd = mammothHerd()
    good_terrain = ['ground', 'tree', 'mountain']
    x, y = randrange(0, SIZE), randrange(0, SIZE)
    while world.area[x][y].t not in good_terrain:
        x, y = randrange(0, SIZE), randrange(0, SIZE)
    around = [(1,1),(0,1),(-1,1),(1,0),(0,0),(-1,0),(1,-1),(0,-1),(-1, -1)]
    oldest = True
    created = 0
    canCreate = True
    while canCreate and amount > 0:
        if oldest:
            new = create_mammoth(x, y, SIZE, ID, True)
            oldest = False
        else:
            new = create_mammoth(x, y, SIZE, ID, False)
        herd.mammoths.append(new)
        yield new
        canCreate = False
        for dx, dy in around:
            if world.area[x + dx][y + dy].t in good_terrain:
                canCreate = True
                x_new, y_new = x + dx, y + dy
        x, y = x_new, y_new
    return herd

def create_mammoth(x, y, SIZE, ID, oldest):
    new = mammoth(SIZE, ID, True if oldest else False, randint(75, 95) if oldest else randint(0, 74))
    new.go_to(x, y)
    return new

