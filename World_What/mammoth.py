from random import *
import objects
import sys
from collections import defaultdict
Passable = {'ground', 'tree', 'mountain'}
Herds = []
all_directions = [(1,1),(0,1),(-1,1),(1,0),(-1,0),(1,-1),(0,-1),(-1, -1)]

class mammothHerd():
    
    def __init__(self):
        self.mammoths = []

class mammoth(objects.obj):
    
    def __init__(self, world, herdID, isLeader=False, age=0, hp=10, water=100, food=50):
        objects.obj.__init__(self, 'M', world)
        self.age, self.hp, self.water, self.food = age, hp, water, food
        self.last = [] 
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
    def info(self):
        print("in point", self.x, self.y)
        print("f = ", self.food, "w = " + str(self.water))
        print(' '.join(map(str, self.last)))
    def dist(self, x, y):
        return abs(x - self.x) + abs(y - self.y) - min(abs(x - self.x), abs(y - self.y)) // 2

    def try_to_go(self, directions):
        for direction in directions:
            if self.move(direction, 0, Passable):
                return
        for direction in all_directions:
            if self.move(direction, 0, Passable):
                return
        print("OMG I AM STUCK")
        return

    def move_to(self, x, y):
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

    def eat(self):
        a = randint(min(5, self.world.area[self.x][self.y].attributes["M-food"]) \
        , min(10, self.world.area[self.x][self.y].attributes["M-food"]))
        self.world.area[self.x][self.y].attributes["M-food"] -= a
        self.food += int(a * 1.5)
    def drink(self):
        a = randint(min(self.world.area[self.x][self.y].attributes["water"], \
        5), min(10, self.world.area[self.x][self.y].attributes["water"]))
        self.world.area[self.x][self.y].attributes["water"] -= 1
        self.water += int(a * 1.5)
        
        
    def move_to_leader(self):
        self.move_to(*self.getLeaderCoord())

    def followLeader(self):
       x, y = self.getLeaderCoord()
       d = self.dist(x, y)
       if self.getLeader().moving_somewhere or d > len(Herds[self.herdID].mammoths) // 3:
           self.move_to_leader()
       else:
           self.wanderAround()

    def isHungry(self):
        return self.food < 30
    def Search(self, rad, obj):
        x, y = self.x, self.y
        used = defaultdict(int)
        used[(x, y)] = 0
        q = [(x, y)]
        mx = self.world.area[x][y].attributes[obj]
        res = (x, y)
        for u in q:
            if used[u] > rad:
                continue
            i, j = u
            if self.world.area[i][j].attributes[obj] > mx and self.world.area[i][j].t in Passable:
                res = (i, j)
                mx = self.world.area[i][j].attributes[obj]
            for dx, dy in all_directions:
                if 0 <= i + dx < self.world.size and 0 <= j + dy < self.world.size and \
                not used[(i + dx, j + dy)] == -1:
                   used[(i + dx, j + dy)] = used[(i, j)] + 1
                   q.append((i + dx, j + dy))
        return res, used[res]

    def remove(self):
        self.world.area[self.x][self.y].obj = None
        arr = list(map(lambda x: (x.x, x.y), self.world.objects))
        self.world.objects.pop(arr.index((self.x, self.y)))
    def isThirsty(self):
        return self.water < 30
    def turn(self, world):
        self.food -= randint(1, 2)
        self.water -= randint(1, 2)
        if self.hp <= 0:
            self.world.log.append("mammoth has died\n")
            self.remove()

        if self.food <= 0:
            self.hp -= randint(1, 2)
        if self.water <= 0:
            self.hp -= randint(1, 2)
        if len(self.last) != 0:
            
            exec("self." + self.last[-1][0])

            self.last[-1][1] -= 1
            if self.last[-1][1] == 0:
                self.last.pop()
            return 
        if len(self.last) != 0:
            exec("self." + self.last[-1][0])
            self.last[-1][1] -= 1
            if self.last[-1][1] == 0:
                self.last.pop()
            return 

        if self.isHungry():
            mx_food = world.area[self.x][self.y].attributes["M-food"]
            res = [0, 0]
            res, dist = self.Search(min(5, (self.food - 10) / 2), "M-food")
            self.move_to(res[0], res[1])
            self.last.append(["eat()", 2])
            self.last.append(["move_to(" + str(res[0]) + "," + str(res[1]) + ")", dist - 1])
            return
        if self.isThirsty():
            res, dist = self.Search(min(5, (self.water - 10) / 2), "water") 
            self.move_to(res[0], res[1])
#            mx_water = world.area[self.x][self.y].attributes["water"]
            self.last.append(["drink()", 2])
            self.last.append(["move_to(" + str(res[0]) + "," + str(res[1]) + ")", dist - 1])
            return
        if len(self.last) != 0:
            exec("self." + self.last[-1][0])
            self.last[-1][1] -= 1
            if self.last[-1][1] == 0:
                self.last.pop()
            return 
        
        if self.isLeader:
            self.wanderAround()
        else:
            self.followLeader()

def generate_mammoth_herds(world):
    for herdID in range(2):
        for new in generate_mammoth_herd(world, 10, herdID):
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
    hasCreated = True
    while canCreate and amount > 0:
        if oldest:
            new, hasCreated = create_mammoth(world, x, y, herdID, True)
            oldest = False
        else:
            new, hasCreated = create_mammoth(world, x, y, herdID, False)
        if hasCreated:
            herd.mammoths.append(new)
            yield new
            amount -= 1
        canCreate = False
        while not canCreate:
            dx, dy = choice(around)
            if world.area[x + dx][y + dy].t in Passable:
                canCreate = True
                x_new, y_new = x + dx, y + dy
        x, y = x_new, y_new
    Herds.append(herd)
    #return herd

def create_mammoth(world, x, y, herdID, oldest):
    if (world.area[x][y].obj != None):
        return 0, False
        
    new = mammoth(world, herdID, True if oldest else False, randint(75, 95) if oldest else randint(0, 74))

    new.go_to(x, y)

    return new, True

