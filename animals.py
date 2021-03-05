from random import random

class Position:
    """reprsent a Position in 2d space
     with methods to perform vector addition and
     scalar multiplication"""
    def __init__(self, x, y, is_null = False):
        self._x = x
        self._y = y
        self._is_null = is_null
    @staticmethod
    def null():
        return Position(0, 0, True)
    def __str__(self):
        return "NULL" if self._is_null else f"({self._x}, {self._y})"
    def __add__(self, other):
        if (self._is_null):
            return Position.null()
        return other.add_exact(self._x, self._y)
    def add_exact(self, x, y):
        if (self._is_null):
            return Position.null()
        return Position(self._x+x, self._y+y)
    def __mul__(self, other):
        if (self._is_null):
            return Position.null()
        return Position(self._x*other, self._y*other)

class Beaver:
    default_pref = {"eat": 0.5, "drink": 0.5}
    default_char = {"lazy": 0.5, "vision": 5}
    default_stats = {"hunger": 0.5, "thirst": 0.5}
    """represent a Beaver, with a method to call every gametick"""
    def __init__(self, start):
        self._pos = start
        self._state = 0 # let 0 be null, 1 be lerping, 2 be eating, 3 be drinking
        self._remaining_ticks = 0
        self._target = Position.null()
        self._pref = {i: Beaver.default_pref[i] for i in Beaver.default_pref}
        self._char = {i: Beaver.default_char[i] for i in Beaver.default_char}
        self._stats = {i: Beaver.default_stats[i] for i in Beaver.default_stats}
    def __str__(self):
        return str(self.pos)
    def tick(self, gameworld):
        if (self._state == 0):
            if (random() > self._char["lazy"]):
                nearest_food = gameworld.nearest(self._pos, "food")
                nearest_water = gameworld.nearest(self._pos, "water")
        elif (self._state == 1):

        elif (self._state == 2):

    def lerp(self):
        pass

b = Beaver(Position(3, 4))
b.tick()
print(b)
