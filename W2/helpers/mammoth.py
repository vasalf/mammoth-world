from random import *
import objects

Passable = {'ground', 'tree', 'mountain'}
Herds = []
all_directions = [(1,1),(0,1),(-1,1),(1,0),(-1,0),(1,-1),(0,-1),(-1, -1)]

class mammothHerd():
    
    def __init__(self):
        self.mammoths = []

class mammoth(objects.obj):
    
    def __init__(self, SIZE, ID, isLeader=False, age=0, hp=10, water=100, food=100):
        objects.obj.__init__(self, 'M', SIZE)
        self.age, self.hp, self.water, self.food = age, hp, water, food
        self.ID = ID
        self.isLeader = isLeader
        if self.isLeader:
            self.moving_somewhere = False

    def wanderAround(self, world):
        dx, dy = choice(all_directions)
        self.move(world, dx, dy, Passable)

    def getLeaderCoord(self):
        xy = Herds[self.ID].mammoths[0]
        return xy.x, xy.y

    def getLeader(self):
        ans = Herds[self.ID].mammoths[0]
        return ans

    def dist(self, x, y):
        return abs(x - self.x) + abs(y - self.y)

    def try_to_go(self, world, directions):
        for direction in directions:
            if self.move(world, direction, Passable):
                return
        for direction in all_directions:
            if self.move(world, direction, Passable):
                return
        print("OMG I AM STUCK")
        return

    def get_direction(self, world, x, y):
        direction = []
        if x >= self.x and y >= self.y:
            direction.append((1, 1))
            if randint(0, 1) == 0:
                direction.append((1, 0))
                direction.append((0, 1))
            else:
                direction.append((0, 1))
                direction.append((1, 0))
        if x <= self.x and y >= self.y:
            direction.append((-1, 1))
            if randint(0, 1) == 0:
                direction.append((-1, 0))
                direction.append((0, 1))
            else:
                direction.append((0, 1))
                direction.append((-1, 0))
        if x >= self.x and y <= self.y:
            direction.append((1, -1))
            if randint(0, 1) == 0:
                direction.append((1, 0))
                direction.append((0, -1))
            else:
                direction.append((0, -1))
                direction.append((1, 0))
        if x <= self.x and y <= self.y:
            direction.append((-1, -1))
            if randint(0, 1) == 0:
                direction.append((-1, 0))
                direction.append((0, -1))
            else:
                direction.append((0, -1))
                direction.append((-1, 0))
        self.try_to_go(world, direction)

    
    def move_to_leader(self, world):
        self.get_direction(world, *self.getLeaderCoord())

    def followLeader(self, world):
       x, y = self.getLeaderCoord()
       d = self.dist(x, y)
       if self.getLeader().moving_somewhere or d > len(Herds[self.ID].mammoths) // 3:
           self.move_to_leader(world)
       else:
           self.wanderAround(world)

    def turn(self, world):
        if self.isLeader:
            self.wanderAround(world)
        else:
            self.followLeader(world)

def generate_mammoth_herds(SIZE, world):
    for ID in range(1):
        for new in generate_mammoth_herd(SIZE, world, 6, ID):
            yield new

def generate_mammoth_herd(SIZE, world, amount, ID):
    herd = mammothHerd()
    x, y = randrange(0, SIZE), randrange(0, SIZE)
    while world.area[x][y].t not in Passable:
        x, y = randrange(0, SIZE), randrange(0, SIZE)
    around = [(1,1),(0,1),(-1,1),(1,0),(-1,0),(1,-1),(0,-1),(-1, -1)]
    oldest = True
    created = 0
    canCreate = True
    x_new = x
    y_new = y
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
            if world.area[x + dx][y + dy].t in Passable:
                canCreate = True
                x_new, y_new = x + dx, y + dy
        x, y = x_new, y_new
        amount -= 1
    Herds.append(herd)
    #return herd

def create_mammoth(x, y, SIZE, ID, oldest):
    new = mammoth(SIZE, ID, True if oldest else False, randint(75, 95) if oldest else randint(0, 74))
    new.go_to(x, y)
    return new

