from random import *
import objects
import sys
Passable = {'ground', 'tree', 'mountain'}
Herds = []
all_directions = [(1,1),(0,1),(-1,1),(1,0),(-1,0),(1,-1),(0,-1),(-1, -1)]

class mammothHerd():
    
    def __init__(self):
        self.mammoths = []

class mammoth(objects.obj):
    
    def __init__(self, world, herdID, isLeader=False, age=0, hp=10, water=100, food=20):
        objects.obj.__init__(self, 'M', world)
        self.age, self.hp, self.water, self.food = age, hp, water, food
        self.last = ''
        self.busy = 0
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
            if self.move(direction, 0, Passable):
                return
        for direction in all_directions:
            if self.move(direction, 0, Passable):
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

    def eat(self):
        a = randint(min(5, self.world.area[self.x][self.y].attributes["M-food"]) \
        , min(10, self.world.area[self.x][self.y].attributes["M-food"]))
        self.world.area[self.x][self.y].attributes["M-food"] -= a
        self.food += int(a * 1.2)
    def drink(self):
        a = randint(min(self.world.area[self.x][self.y].attributes["water"], \
        5), min(10, self.world.area[self.x][self.y].attributes["water"]))
        self.world.area[self.x][self.y].attributes["water"] -= 1
        self.water += int(a * 1.2)
        
        
    def move_to_leader(self):
        self.get_direction(*self.getLeaderCoord())

    def followLeader(self):
       x, y = self.getLeaderCoord()
       d = self.dist(x, y)
       if self.getLeader().moving_somewhere or d > len(Herds[self.herdID].mammoths) // 3:
           self.move_to_leader()
       else:
           self.wanderAround()

    def isHungry(self):
        return self.food < 10
    def remove(self):
        self.world.area[self.x][self.y].obj = None
        arr = list(map(lambda x: (x.x, x.y), self.world.objects))
        self.world.objects.pop(arr.index((self.x, self.y)))
    def isThursty(self):
        return self.water < 30
    def turn(self, world):
        self.food -= randint(1, 3)
        self.water -= randint(1, 2)
        if self.food <= 0:
            self.world.log.append(("mammoth has died because he was hungry\n"))
            self.remove()
            return
        if self.water <= 0:
            self.world.log.append("mammoth has died because he was thursty\n")
            self.remove()
            return

        if self.isHungry():
            mx_food = world.area[self.x][self.y].attributes["M-food"]
            res = [0, 0]
            for dx, dy in all_directions:
                if world.area[self.x + dx][self.y + dy].obj == None and \
                   world.area[self.x + dx][self.y + dy].attributes["M-food"] > mx_food \
                   and world.area[self.x + dx][self.y + dy].t in Passable:
                    mx_food = world.area[self.x + dx][self.y + dy].attributes["M-food"]
                    res = dx, dy
            self.move(res[0], res[1], Passable)
            self.eat()
            self.last = "eat()"
            self.busy = 3
            return
        if self.isThursty():
            mx_water = world.area[self.x][self.y].attributes["water"]
            res = [0, 0]
            for dx, dy in all_directions:
                if world.area[self.x + dx][self.y + dy].obj == None and \
                   world.area[self.x + dx][self.y + dy].attributes["water"] > mx_water \
                   and world.area[self.x + dx][self.y + dy].t in Passable:
                    mx_water = world.area[self.x + dx][self.y + dy].attributes["water"]
                    res = dx, dy
            self.move(res[0], res[1], Passable)
            self.drink()
            self.last = "drink()"
            self.busy = 3
            return
        if self.busy != 0:
            exec("self." + self.last)
            self.busy -= 1
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

