moves = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]
grass = '`'
swamp = ';'
meadle = ':'
simple = '"'
mountain = '^'
river = '~'
sea = '~'
tree = 'T'
number = {}

number["swamp"] = 0
number["ground"] = 1
number["meadle"] = 2
number["mountain"] = 3
number["grass"] = 4
number["water river"] = 5
number["water lake"] = 6
max_size = [{} for i in range(10)]
max_size[0]["M-food"] = 5
max_size[0]["water"] = 5
max_size[1]["M-food"] = 10
max_size[1]["water"] = 5
max_size[2]["M-food"] = 20
max_size[2]["water"] = 5
max_size[3]["M-food"] = 0
max_size[3]["water"] = 5
max_size[4]["M-food"] = 18
max_size[4]["water"] = 5
max_size[5]["M-food"] = 0
max_size[5]["water"] = 40
max_size[6]["M-food"] = 0
max_size[6]["water"] = 40

class square:
    def __init__(self, typ):
        self.c = typ if typ != 0 else ''
        self.t = 'ground'
        self.t2 = ''
        if typ == swamp:
            self.t2 = "swamp"
        elif typ == meadle:
            self.t2 = "meadle"
        elif typ == grass:
            self.t2 = "grass"
        self.height = 0
            

        if typ == 'T':
            self.t = 'tree'
        elif typ == chr(8776):
            self.t = "water sea"
        elif typ == 'S':
            self.t = "water lake"
        elif typ == '~':
            self.t = "water river"
        elif typ == 'O':
            self.t = "ice-berg"
        elif typ == '^':
            self.t = "mountain"

        self.attributes = {}
        self.attributes["M-food"] = (10 - 5 * (self.t2 == "swamp") - \
                                    9 * (self.t == "mountain") + \
                                    10 * (self.t2 == "grass" or self.t2 == "meadle") -\
                                    5 * (self.t2 == '') + 10 * (self.t == "tree"))
        self.attributes["water"] = 5
        if self.t.split()[0] == "water":
            self.attributes["M-food"] = 0
            self.attributes["water"] = 40
        self.last = 0


        self.obj = None

    def __str__(self):
#        if self.atr
        return str(self.c)

    def remove(self):
        self.obj = None

    def info(self):
        return (self.t + ', ' + (self.t2 + ', ') * bool(self.t2) + \
               ', '.join(map(str, self.attributes.items()))).rstrip(', ') + \
               ((', ' + str(self.obj)) if self.obj != None else '')
 
