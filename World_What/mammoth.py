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
    
    def __init__(self, world, herdID, x=0, y=0, isLeader=False, age=0, hp=10, water=70, food=50):
        objects.obj.__init__(self, 'M', world, x, y)
        self.name = "mammoth"
        self.age, self.hp, self.water, self.food = age, hp, water, food
        self.last = [] 
        self.herd = []
        self.v_rad = 5 + 2 * isLeader
        self.herdID = herdID
        self.isLeader = isLeader
        self.moving_somewhere = True
        if self.isLeader:
            self.moving_somewhere = False

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
                #self.upgrade()
                return True
        #for direction in all_directions:
            #if self.move(direction, 0, Passable):
                #return True
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

    def eat(self, square):
        const = self.get_amount(self.x, self.y, "M-food")
        a = randint(min(5, const), min(10, const))
        square.attributes["M-food"] = const - a 

        self.food += (a)
        return a != 0
    def eatNdrink(self, square):
        const1 = self.get_amount(self.x, self.y, "M-food")
        const2 = self.get_amount(self.x, self.y, "water")
        a = min(const1, const2)
        square.attributes["M-food"] = const1 - a
        square.attributes["water"] -= const2 - a

        self.food += int(a * 0.7)
        self.water += int(a * 0.7)
        return a != 0

    def drink(self, square):
        const = self.get_amount(self.x, self.y, "water")
        a = randint(min(5, const), min(10, const))
        square.attributes["water"] = const - a 
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

    def run_away(self, coords):
        x, y = coords
        self.move_to(self.x-x, self.y-y)

    
    def remove(self, square):
        square.remove()
#        self.world.area[self.x][self.y].obj = Non
    def isThirsty(self):
        return self.water < 30
    def turn(self, square):
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
            self.hp += randint(3, 5)

        if self.food <= 6 and self.water <= 6:
            mx = 0
            res = [0, 0]
            for dx, dy in all_directions:
                if self.world.area[self.x + dx, self.y + dy].attributes["M-food"] + \
                self.world.area[self.x + dx, self.y + dy].attributes["water"] > mx + 5 and \
                self.world.area[self.x + dx, self.y + dy].t in Passable:
                    res = dx, dy
                    mx = self.world.area[self.x + dx, self.y + dy].attributes["M-food"] + \
                    self.world.area[self.x + dx, self.y + dy].attributes["water"] 
            self.move(res[0], res[1], Passable)
            self.eatNdrink(square)
        
       
        if self.isLeader:
            res, coords = self.objects_search("mammoth")
            if res:
                self.last.append(("run_away((%d, %d))"%coords, 2))
                for i in range(1, len(self.herd)):
                    self.herd[i].last.append(("followLeader()", 2))
            else:
                coords, res = self.Search("M-food", Passable)
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
            res, dist = self.Search(a, Passable)
            self.move_to(*res) 
            self.last.append(["eat(square)" if a == "M-food" else "drink(square)", 2])
 
            self.last.append([("move_to(%d, %d)"%res), self.dist(*res)])
            return
        if len(self.last) != 0:
            exec("self." + self.last[-1][0])
            self.last[-1][1] -= 1
            if self.last[-1][1] == 0:
                self.last.pop()
            return 
        
        if self.isLeader:
            a = "M-food" if self.food < self.water \
                         else "water"
            res = self.Search(a, Passable)
            self.last.append(["eat(square)" if a == "M-food" else "drink(square)", 2])
            self.move_to(*res[0])
            self.last.append([("move_to(%d, %d)"%res[0]), self.dist(*res[0])])
        else:
            if self.dist(*self.getLeaderCoord()) < 5:
                a = "M-food" if self.food < self.water \
                             else "water"
                res = self.Search(a, Passable)
                self.move_to(*res[0])
                self.last.append(["eat(square)" if a == "M-food" else "drink(square)", 2])
                self.last.append([("move_to(%d, %d)"%res[0]), self.dist(*res[0])])
            else:
                self.followLeader()

def generate_mammoth_herds(world):
    for herdID in range(1):
        for new in generate_mammoth_herd(world, 3, herdID):
            print(0)
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
        
    new = mammoth(world, herdID, x, y, True if oldest else False, randint(75, 95) if oldest else randint(0, 74))
    world.area[x][y].obj = new
    return new, True

