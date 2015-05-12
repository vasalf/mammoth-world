from square import max_size, number
all_directions = [(0,1),(1,0),(-1,0),(0,-1)]
import copy
sums = [0, 1, 4, 9, 16, 21, 24, 25]
colored = {}
names = {}
colored['X'] = ['X', '', 'red', 0, 'gray', 1, ["blinked"]]
colored['M'] = ['M', '', 'red', 0, 'gray', 0, []]
colored['@'] = ['@', '', "purpur", 0, 'black', 0, ["hard"]]
names['M'] = "mammoth"
names['X'] = "SightOfGod"
names['@'] = "wolf"

class char:
    __slots__ = ['attr']
    def __init__(self, pars):
        self.attr = dict()
        for k, v in pars:
            self.attr[k] = v

    def size(self):
        return self.attr['size']

    def turn(self):
        return self.attr['Turn'][0]

def change_energy(delta_height, type_a, type_b):
    return 0

class obj:
    __slots__ = ['c', 'x', 'y', 'memory', 'world', 'name', 'energy', 'Turn']
    def __init__(self, sym, world, x=0, y=0, mem=[[]]):
        self.c = sym
        self.Turn = world.Turn
        self.x = x
        self.y = y
        self.memory = {}
        for i in range(len(mem)):
            for j in range(len(mem[i])):
                self.memory[i, j] = mem[i][j]
        self.world = char([('size', world.size), ('Turn', world.Turn)])
        self.name = names[sym]
        self.energy = 0
        world.area[x][y].obj = self
        self.memory[x, y] = copy.deepcopy(world.area[x][y])
#    def remove(self):
#        self.obj = None
#All types should be possible on default
    def move(self, dx=0, dy=0, Possible={'ground', 'tree', 'sea water', 'water lake', 'water river', 'ice-berg', 'mountain'}, flag=0):
        if isinstance(dx, tuple):
            dx, dy = dx
        if (0 <= self.x + dx < self.world.size()) and \
        (0 <= self.y + dy < self.world.size()) and \
        (self.memory[(self.x + dx, self.y + dy)].get_name() in Possible) and \
         self.memory[(self.x + dx, self.y + dy)].obj == None:
            self.memory[(self.x, self.y)].obj = None
            if not flag:
                self.memory[(self.x, self.y)].last_time = self.world.turn()
            self.energy -= change_energy(\
            self.memory[self.x + dx, self.y + dy].height - self.memory[self.x, self.y].height,
            self.memory[self.x, self.y].get_name(), self.memory[self.x + dx, self.y + dy].get_name())
            self.x += dx
            self.y += dy
            
            #print(Possible, self.memory[self.x, self.y].t, self.memory[self.x, self.y].t\
            #+ self.memory[self.x + dx, self.y + dy].t2 in Possible, sep = '\n')
            self.memory[self.x, self.y].obj = self
            if not flag:
                self.memory[self.x, self.y].last_time = self.world.turn()
            return True
        return False

    def copy(self):
        
        res = copy.copy(self)
        res.memory = {}
        print(len(self.memory.keys()))
        return res


    def turn(self):
        pass
    
    def Search(self, obj, Passable):
        rad = self.v_rad
        x, y = self.x, self.y
        used = dict()
        used[(x, y)] = 0
        q = [(x, y)]
        mx = self.memory[x, y].attributes[obj]
        res = (x, y)
        for u in q:
            if used[u] >= rad:
                continue
            i, j = u
            if self.get_amount(i, j, obj) > mx and self.memory[i, j].t in Passable:
                res = (i, j)
                mx = self.memory[i, j].attributes[obj] - 1.5 * used[u]
            for dx, dy in all_directions:
                if 0 <= i + dx < self.world.size() and 0 <= j + dy < self.world.size() and \
                used.get((i + dx, j + dy), -1) == -1:
                    used[(i + dx, j + dy)] = used[(i, j)] + 1
                    q.append((i + dx, j + dy))
        return res, used[res]
    
    def dist(self, x, y):
        return abs(x - self.x) + abs(y - self.y) - min(abs(x - self.x), abs(y - self.y)) // 2

    def go_to(self, x, y):
        self.memory[self.x, self.y].remove()
        self.x = x
        self.y = y
        self.memory[self.x, self.y].obj = self

    def __str__(self):
        return self.c
    #def turn(self, world):
    
     #   return
    def turn_number(self):
        return self.Turn[0]


    def color_args(self):
        return colored[self.c]

    def get_amount(self, i, j, obj):
        x = self.memory[i, j].last_time
        return int(-self.dist(i, j) * 2) + \
        int((max_size[number[self.memory[i, j].get_name()]][obj] - self.memory[i, j].attributes[obj]) *\
        (sums[min(7, max(0, (-x + self.turn_number() - 2)))]) / 25) +\
        self.memory[i, j].attributes[obj]
    
    def objects_search(self, obj="SideOfGod"):
        rad = self.v_rad
        x, y = self.x, self.y
        used = dict()
        used[(x, y)] = 0
        q = [(x, y)]
        for u in q:
            if used[u] >= rad:
                return (False, (0, 0))
            i, j = u
            if self.memory[i, j].obj != None and self.memory[i, j].obj.name != obj and\
            self.memory[i, j].obj.name != "SideOfGod":
                return (True, (i, j))
            for dx, dy in all_directions:
                if 0 <= i + dx < self.world.size() and 0 <= j + dy < self.world.size() and \
                used.get((i + dx, j + dy), -1) == -1:
                    used[(i + dx, j + dy)] = used[(i, j)] + 1
                    q.append((i + dx, j + dy))


def Help():
    print("""\n
    If you want to make a new type of object, 
    you should go into the file W1/World/objects.py and write: 
    colored['<view of object>'] = ['<view of object>', '', '<color>', 0, 
    '<background>', 0, []] \n 
    if you want to make new object in new programm, write 
    a = obj(<symbol>, <size of the world>)
    if you want to move, you should use "move"\n
    if you want to print all, you should ask me
    """)


#Help()
