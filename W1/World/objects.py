colored = {}
colored['X'] = ['X', '', 'red', 0, 'gray', 1, ["blinked"]]
class obj:
    def __init__(self, sym, size):
        self.c = sym
        self.x = 0
        self.y = 0
        self.size = size

    def move(self, dx, dy):
        if (0 <= self.x + dx < self.size) and (0 <= self.y + dy < self.size):
            self.x += dx
            self.y += dy
    def go_to(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return self.c
    def turn(self):
        return
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


Help()
