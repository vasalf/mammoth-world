colored = {}
colored['X'] = ['X', '', 'red', 0, 'gray', 1, ["blinked"]]
colored['M'] = ['M', '', 'red', 0, 'gray', 0, ["blinked"]]
colored['@'] = ['@', '', "purpur", 0, 'black', 0, ["hard"]]
class obj:
    def __init__(self, sym, world):
        self.c = sym
        self.x = 0
        self.y = 0
        self.world = world

#All types should be possible on default
    def move(self, dx=0, dy=0, Possible={'ground', 'tree', 'sea water', 'water lake', 'water river', 'ice-berg', 'mountain'}):
        if isinstance(dx, tuple):
            dx, dy = dx
        if (0 <= self.x + dx < self.world.size) and (0 <= self.y + dy < self.world.size) and (self.world.area[self.x + dx][self.y + dy].t in Possible) and self.world.area[self.x + dx][self.y + dy].obj == None:
            self.world.area[self.x][self.y].obj = None
            self.x += dx
            self.y += dy
            print(Possible, self.world.area[self.x][self.y].t, self.world.area[self.x][self.y].t in Possible, sep = '\n')
            self.world.area[self.x][self.y].obj = self
            return True
        return False
    def go_to(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return self.c
    #def turn(self, world):
    
     #   return
    def color_args(self):
        return colored[self.c]

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
