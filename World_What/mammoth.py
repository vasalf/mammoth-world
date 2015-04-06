from random import *
import objects
import sys
from collections import defaultdict
Passable = {'meadle', 'coast', 'grass', 'swamp', 'ground', 'tree', ""}
Herds = []
all_directions = [(0,1),(1,0),(-1,0),(0,-1)]
max_hp = 10
class mammothHerd():
    
    def __init__(self):
        self.mammoths = []

class mammoth(objects.obj):
    
    def __init__(self, world, herdID, isLeader=False, age=0, hp=10, water=70, food=50):
        objects.obj.__init__(self, 'M', world)
        self.name = "mammoth"
        self.age, self.hp, self.water, self.food = age, hp, water, food
        self.last = [] 
        self.herd = []
        self.herdID = herdID
        self.isLeader = isLeader
        self.moving_somewhere = True
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
    def  info(self):
        print("in point", self.x, self.y)
        print("f = %d, w = %d, health = %d"%(self.food, self.water, self.hp))
        print(' '.join(map(str, self.last)))


    def try_to_go(self, directions):
        for direction in directions:
            if self.move(direction, 0, Passable):
                return True
        for direction in all_directions:
            if self.move(direction, 0, Passable):
                return True
        print("OMG I AM STUCK")
        return False

    def move_to(self, x, y):
        direction = []
#        if self.world.area[x][y].obj != None:
 #           return False

        if x >= self.x and y >= self.y:
            #direction.append((1, 1))
            if randint(0, 1) == 0:
                direction.append((1, 0))
                direction.append((0, 1))
            else:
                direction.append((0, 1))
                direction.append((1, 0))
        if x <= self.x and y >= self.y:
            #direction.append((-1, 1))
            if randint(0, 1) == 0:
                direction.append((-1, 0))
                direction.append((0, 1))
            else:
                direction.append((0, 1))
                direction.append((-1, 0))
        if x >= self.x and y <= self.y:
            #direction.append((1, -1))
            if randint(0, 1) == 0:
                direction.append((1, 0))
                direction.append((0, -1))
            else:
                direction.append((0, -1))
                direction.append((1, 0))
        if x <= self.x and y <= self.y:
            #direction.append((-1, -1))
            if randint(0, 1) == 0:
                direction.append((-1, 0))
                direction.append((0, -1))
            else:
                direction.append((0, -1))
                direction.append((-1, 0))
        return self.try_to_go(direction)

    def eat(self):
        const = self.get_amount(self.x, self.y, "M-food")
        a = randint(min(5, const), min(10, const))
        self.world.area[self.x][self.y].attributes["M-food"] = const - a 

        self.food += (a)
        return a != 0
    def eatNdrink(self):
        const1 = self.get_amount(self.x, self.y, "M-food")
        const2 = self.get_amount(self.x, self.y, "water")
        a = min(const1, const2)
        self.world.area[self.x][self.y].attributes["M-food"] = const1 - a
        self.world.area[self.x][self.y].attributes["water"] -= const2 - a

        self.food += int(a * 0.7)
        self.water += int(a * 0.7)
        return a != 0

    def drink(self):
        const = self.get_amount(self.x, self.y, "water")
        a = randint(min(5, const), min(10, const))
        self.world.area[self.x][self.y].attributes["water"] = const - a 
        self.water += int(a)
        return a != 0
        
        
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
        used = dict()
        used[(x, y)] = 0
        q = [(x, y)]
        mx = self.world.area[x][y].attributes[obj]
        res = (x, y)
        for u in q:
            if used[u] > rad:
                continue
            i, j = u
            if self.get_amount(i, j, obj) > mx and self.world.area[i][j].t in Passable:
                res = (i, j)
                mx = self.world.area[i][j].attributes[obj] - 1.5 * used[u]
            for dx, dy in all_directions:
                if 0 <= i + dx < self.world.size and 0 <= j + dy < self.world.size and \
                used.get((i + dx, j + dy), -1) == -1:
                   used[(i + dx, j + dy)] = used[(i, j)] + 1
                   q.append((i + dx, j + dy))
        return res, used[res]

    def run_away(self, coords):
        x, y = coords
        self.move_to(self.x-x, self.y-y)

    def objects_search(self, rad, obj):
        x, y = self.x, self.y
        used = dict()
        used[(x, y)] = 0
        q = [(x, y)]
        for u in q:
            if used[u] > rad:
                return (False, (0, 0))
            i, j = u
            if self.world.area[i][j].obj != None and self.world.area[i][j].obj.name != obj and\
            self.world.area[i][j].obj.name != "SideOfGod":
                return (True, (i, j))
            for dx, dy in all_directions:
                if 0 <= i  + dx < self.world.size and 0 <= j + dy < self.world.size and \
                used.get((i + dx, j + dy), -1) == -1:
                    used[(i + dx, j + dy)] = used[(i, j)] + 1
                    q.append((i + dx, j + dy))

    def remove(self):
        self.world.area[self.x][self.y].remove()
        arr = list(map(lambda x: (x.x, x.y), self.world.objects))
        self.world.objects.pop(arr.index((self.x, self.y)))
#        self.world.area[self.x][self.y].obj = Non
    def isThirsty(self):
        return self.water < 30
    def turn(self):
        self.food -= randint(1, 2)
        self.water -= randint(1, 2)
        if self.hp <= 0:
            self.world.log.append("mammoth has died in (%d, %d) at %d turn\n"%(self.x, self.y, self.world.turn))
            self.remove()

        if self.food <= 0:
            self.hp -= 1
        if self.water <= 0:
            self.hp -= 1
        if self.food >= 25 and self.water >= 25:
            self.hp += 1
            self.hp = min(self.hp, max_hp)
        if self.food <= 6 and self.water <= 6:
            mx = 0
            res = [0, 0]
            for dx, dy in all_directions:
                if self.world.area[self.x + dx][self.y + dy].attributes["M-food"] + \
                self.world.area[self.x + dx][self.y + dy].attributes["water"] > mx + 5 and \
                self.world.area[self.x + dx][self.y + dy].t in Passable:
                    res = dx, dy
                    mx = self.world.area[self.x + dx][self.y + dy].attributes["M-food"] + \
                    self.world.area[self.x + dx][self.y + dy].attributes["water"] 
            self.move(res[0], res[1], Passable)
            self.eatNdrink()
        
       
        if self.isLeader:
            res, coords = self.objects_search(6, "mammoth")
            if res:
                self.last.append(("run_away((%d, %d))"%coords, 2))
                for i in range(1, len(self.herd)):
                    self.herd[i].last.append(("followLeader()", 2))
            else:
                coords, res = self.Search(6, "M-food")
                x, y = coords
                if res > 3: 
                    self.move_to(*coords)
                    for i in range(1, len(self.herd)):
                        self.herd[i].last.append(("followLeader()", 2))
        while len(self.last) != 0 and self.last[-1][1] <= 0:
            self.last.pop()
        if len(self.last) != 0:
            
            while len(self.last) != 0 and not eval("self." + self.last[-1][0]):
                self.last.pop()
            else:
                if len(self.last) != 0:
                    self.last[-1][1] -= 1
                    if self.last[-1][1] <= 0:
                        self.last.pop()
            return 
                    

        if self.isHungry() or self.isThirsty():
            a = "M-food" if self.food < self.water else "water"
            res, dist = self.Search(min(7, (min(self.food, self.water) + 10) // 2), a)
            self.move_to(*res) 
            self.last.append(["eat()" if a == "M-food" else "drink()", 2])
 
            self.last.append([("move_to(%d, %d)"%res), self.dist(*res)])
            return
        if len(self.last) != 0:
            exec("self." + self.last[-1][0])
            self.last[-1][1] -= 1
            if self.last[-1][1] == 0:
                self.last.pop()
            return 
        
        if self.isLeader:

            if random() < 1 / 3:
                a = "M-food" if self.food < self.water \
                             else "water"
                res = self.Search(2, a)
                self.last.append(["eat()" if a == "M-food" else "drink()", 2])
                self.move_to(*res[0])
                self.last.append([("move_to(%d, %d)"%res[0]), self.dist(*res[0])])
            else:
                self.wanderAround()
        else:
            if self.dist(*self.getLeaderCoord()) < 3:
                a = "M-food" if self.food < self.water \
                             else "water"
                res = self.Search(2, a)
                self.move_to(*res[0])
                self.last.append(["eat()" if a == "M-food" else "drink()", 2])
                self.last.append([("move_to(%d, %d)"%res[0]), self.dist(*res[0])])
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
            if world.area[x + dx][y + dy].t2 in Passable:
                canCreate = True
                x_new, y_new = x + dx, y + dy
        x, y = x_new, y_new
    for mammoth in herd.mammoths[1:]:
        herd.mammoths[0].herd.append(mammoth)
    Herds.append(herd)
    #return herd

def create_mammoth(world, x, y, herdID, oldest):
    if (world.area[x][y].obj != None or (world.area[x][y].t2 not in Passable)):
        return 0, False
        
    new = mammoth(world, herdID, True if oldest else False, randint(75, 95) if oldest else randint(0, 74))

    new.go_to(x, y)

    return new, True

