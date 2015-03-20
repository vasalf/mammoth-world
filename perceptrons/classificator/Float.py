class Float:
    def __init__(self, a=0):
        self.down = 35
        if type(a) == Float:
            self.up = a.up
            return
        self.up = a << self.down
    #addition

    def __add__(self, other):
        res = Float(other)
        res.up += self.up
        return res

    def __radd__(self, other):
        res = Float(other)
        res.up += self.up
        return res

    def __iadd__(self, other):
        self = self + other
        return self
    #multiplication

    def __mul__(self, other):
        other = Float(other)
        res = Float(self.up * other.up >> self.down)
        return res

    def __rmul__(self, other):
        other = Float(other)
        res = Float(self.up * other.up >> self.down)
        return res

    def __imul__(self, other):
        other = Float(other)
        self.up *= other.up
        self.up >>= self.down
        return self
    
    #truediv
    
    def __truediv__(self, other):
        _other = Float(other)
        res = Float(self.up // _other.up)
        return res
    
    def __rtruediv__(self, other):
        _other = Float(other)
        res = Float(_other.up // self.up)
        return res
    
    def __itruediv__(self, other):
        self.up //= Float(other).up
        return res
    
    #sub
    def __sub__(self, other):
        _other = Float(other)
        res = Float(self.up - _other.up)
        return res

    def __rsub__(self, other):
        _other = Float(other)
        res = Float(_other.up - self.up)
        return res
    
    def __isub__(self, other):
        _other = Float(other)
        self.up -= _other.up
        return self

    #comparation

    def __lt__(self, other):
        _other = Float(other)
        return self.up < _other.up
    def __le__(self, other):
        _other = Float(other)
        return self.up <= _other.up
    def __eq__(self, other):
        _other = Float(other)
        return self.up == _other.up
    def __ne__(self, other):
        return not(self == other)
    def __gt__(self, other):
        _other = Float(other)
        return self.up > _other.up
    def __ge__(self, other):
        _other = Float(other)
        return self.up >= other.up
    def __str__(self):
        return "%d.%d"%(self.up >> self.down, self.up ^ ((self.up >>self.down) << self.down))

