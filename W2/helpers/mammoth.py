from random import *
import objects

Passable = {'ground', 'tree', 'mountain'}
Herds = []
all_directions = [(1,1),(0,1),(-1,1),(1,0),(-1,0),(1,-1),(0,-1),(-1, -1)]

class mammothHerd():
    
    def __init__(self):
        self.mammoths = []

class mammoth(objects.obj):
    
    def __init__(self, world, herdID, isLeader=False, age=0, hp=10, water=100, food=100):
        objects.obj.__init__(self, 'M', world)
        self.age, self.hp, self.water, self.food = age, hp, water, food
        self.herdID = herdID
        self.isLeader = isLeader
        if self.isLeader:
            self.moving_somewhere = False
        self.world.area[self.x][self.y].obj = self

    def wanderAround(self):
        dx, dy = choice(all_directions)
        self.move(dx, dy, Passable)

    def getLeaderCoord(self):
        xy = Herds[self.herdID].mammoths[0]
        return xy.x, xy.y

    def getLeader(self):
        ans = Herds[self.herdID].mammoths[0]
        return ans

    def dist(self, x, y):
        return abs(x - self.x) + abs(y - self.y)

    def try_to_go(self, directions):
        for direction in directions:
            if self.move(direction, Passable):
                return
        for direction in all_directions:
            if self.move(direction, Passable):
                return
        print("OMG I AM STUCK")
        return

    def get_direction(self, x, y):
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
        self.try_to_go(direction)

    
    def move_to_leader(self):
        self.get_direction(*self.getLeaderCoord())

    def followLeader(self):
       x, y = self.getLeaderCoord()
       d = self.dist(x, y)
       if self.getLeader().moving_somewhere or d > len(Herds[self.herdID].mammoths) // 3:
           self.move_to_leader()
       else:
           self.wanderAround()

    def turn(self, world):
        if self.isLeader:
            self.wanderAround()
        else:
            self.followLeader()

def generate_mammoth_herds(world):
    for herdID in range(1):
        for new in generate_mammoth_herd(world, 6, herdID):
            yield new

def generate_mammoth_herd(world, amount, herdID):
    herd = mammothHerd()
    x, y = randrange(0, world.size), randrange(0, world.size)
    while world.area[x][y].t not in Passable:
        x, y = randrange(0, world.size), randrange(0, world.size)
    around = [(1,1),(0,1),(-1,1),(1,0),(-1,0),(1,-1),(0,-1),(-1, -1)]
    oldest = True
    created = 0
    canCreate = True
    x_new = x
    y_new = y
    while canCreate and amount > 0:
        if oldest:
            new = create_mammoth(world, x, y, herdID, True)
            oldest = False
        else:
            new = create_mammoth(world, x, y, herdID, False)
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

def create_mammoth(world, x, y, herdID, oldest):
    new = mammoth(world, herdID, True if oldest else False, randint(75, 95) if oldest else randint(0, 74))
    new.go_to(x, y)
    return new

