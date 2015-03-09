
grass = '`'
swamp = ';'
meadle = ':'
simple = '"'
mountain = '^'
river = '~'
sea = '~'
tree = 'T'

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
        self.attributes["M-food"] = 10 - 5 * (self.t2 == "swamp") - \
                                    9 * (self.t == "mountain") + \
                                    10 * (self.t2 == "grass")
        self.attributes["water"] = 5
        if self.t.split()[0] == "water":
            self.attributes["M-food"] = 0
            self.attributes["water"] = 40


        self.obj = None

    def __str__(self):
#        if self.atr
        return str(self.c)
    def info(self):
        return (self.t + ', ' + (self.t2 + ', ') * bool(self.t2) + ', '.join(map(str, self.attributes))).rstrip(', ')
 
