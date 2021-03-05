class Position(object):
    """reprsent a Position in 2d space
     with methods to perform vector addition and
     scalar multiplication"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return f"({self.x}, {self.y})"
    def __add__(self, other):
        return Position(self.x+other.x, self.y+other.y)
    def __mul__(self, other):
        return Position(self.x*other, self.y*other)

class Beaver:
    """represent a Beaver, with a method to call every gametick"""
    def __init__(self, start):
        self.pos = start
    def __str__(self):
        return str(self.pos)
    def tick(self):
        pass
