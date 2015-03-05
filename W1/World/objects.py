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
