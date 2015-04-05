from square import max_size, number

sums = [0, 1, 4, 9, 16, 21, 24, 25]
colored = {}
names = {}
colored['X'] = ['X', '', 'red', 0, 'gray', 1, ["blinked"]]
colored['M'] = ['M', '', 'red', 0, 'gray', 0, []]
colored['@'] = ['@', '', "purpur", 0, 'black', 0, ["hard"]]
names['M'] = "mammoth"
names['X'] = "SightOfGod"
names['@'] = "wolf"
class obj:
    def __init__(self, sym, world):
        self.c = sym
        self.x = 0
        self.y = 0
        self.world = world
        self.name = names[sym]
#    def remove(self):
#        self.obj = None
#All types should be possible on default
    def move(self, dx=0, dy=0, Possible={'ground', 'tree', 'sea water', 'water lake', 'water river', 'ice-berg', 'mountain'}, flag=0):
        if isinstance(dx, tuple):
            dx, dy = dx
        if (0 <= self.x + dx < self.world.size) and \
        (0 <= self.y + dy < self.world.size) and \
        (self.world.area[self.x + dx][self.y + dy].t + self.world.area[self.x + dx][self.y + dy].t2 in Possible) and \
        self.world.area[self.x + dx][self.y + dy].obj == None:
            self.world.area[self.x][self.y].obj = None
            if not flag:
                self.world.area[self.x][self.y].last_time = self.world.turn
            self.x += dx
            self.y += dy
            print(Possible, self.world.area[self.x][self.y].t, self.world.area[self.x][self.y].t\
            + self.world.area[self.x + dx][self.y + dy].t2 in Possible, sep = '\n')
            self.world.area[self.x][self.y].obj = self
            if not flag:
                self.world.area[self.x][self.y].last_time = self.world.turn
            return True
        return False

    def turn(self):
        pass

    def dist(self, x, y):
        return abs(x - self.x) + abs(y - self.y) - min(abs(x - self.x), abs(y - self.y)) // 2

    def go_to(self, x, y):
        self.world.area[self.x][self.y].remove()
        self.x = x
        self.y = y
        self.world.area[self.x][self.y].obj = self

    def __str__(self):
        return self.c
    #def turn(self, world):
    
     #   return
    def color_args(self):
        return colored[self.c]

    def get_amount(self, i, j, obj):
        x = self.world.area[i][j].last_time
        return int(-self.dist(i, j) * 1.5) + \
        int((max_size[number[self.world.area[i][j].t +\
        self.world.area[i][j].t2]][obj] - self.world.area[i][j].attributes[obj]) *\
        (sums[min(7, max(0, (-x + self.world.turn - 2)))]) / 25) +\
        self.world.area[i][j].attributes[obj]


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
