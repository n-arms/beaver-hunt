from random import random
from math import sqrt
from collections import OrderedDict

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
    def distance(self, x, y=None):
        if (y == None):
            return x.distance(self._x, self._y)
        else:
            return sqrt((self._x - x)**2 + (self._y - y)**2)

class Beaver:
    """represent a Beaver, with a method to call every gametick"""
    def __init__(self, start):
        self._pos = start
        self._remaining_ticks = 0
        self._state = 0 # 0 is null, 1 is eating, 2 is drinking, 3 is moving to eat, 4 is moving to drink
        self._vision = 0.5
        self._hunger = 0.5
        self._thirst = 0.5
        self._target = Position.null()
    def __str__(self):
        return str(self.pos)
    def tick(self, gameworld):
        self._hunger += 0.01
        self._thirst += 0.01
        if (self._hunger > 1 or self._thirst > 1):
            gameworld.kill(self)
        if (self._state == 0):
            self.chose_state()
        elif (self._state == 1):
            self._remaining_ticks -= 1
            if (self._remaining_ticks == 0):
                self.eat()
        elif (self._state == 2):
            self._remaining_ticks -= 1
            if (self._remaining_ticks == 1):
                self.drink()
        elif (self._state == 3):
            result = self.move()
            if result == 0:
                self._state = 1
                self._remaining_ticks = 5
            elif result == 1:
                self._state = 0
        elif (self._state == 4):
            result = self.move()
            if result == 0:
                self._state = 2
                self._remaining_ticks == 5
            elif result == 1:
                self._state = 0

        else:
            raise ValueError("illegal state")


    def chose_state(self, features):
        if "food" in features:
            if "water" in features:
                if self._hunger > self._thirst:
                    self._target = features["food"]
                    self._state = 3
                else:
                    self._target  = features["water"]
                    self._state = 4
            else:
                self._target = features["food"]
                self._state = 3
        else:
            if "water" in features:
                self._target = features["water"]
                self._state = 4
            else:
                self._target = Position.null()
                self._state = 0



b = Beaver(Position(3, 4))
b.tick()
print(b)
