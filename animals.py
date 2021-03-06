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
        if self._is_null:
            return Position.null()
        return other.add_exact(self._x, self._y)
    def add_exact(self, x, y):
        if self._is_null:
            return Position.null()
        return Position(self._x+x, self._y+y)
    def __mul__(self, other):
        if self._is_null:
            return Position.null()
        return Position(self._x*other, self._y*other)
    def __sub__(self, other):
        if self._is_null:
            return Position.null()
        return other.sub_exact(self._x, self._y)
    def sub_exact(self, x, y):
        if self._is_null:
            return Position.null()
        return Position(x-self._x, y-self._y)
    def distance(self, x, y=None):
        if y == None:
            return x.distance(self._x, self._y)
        else:
            return sqrt((self._x - x)**2 + (self._y - y)**2)
    def normalize(self):
        if self._is_null:
            return Position.null()
        length = self.distance(0, 0)
        return Position(self._x/length, self._y/length)


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
        return f"Beaver: [hunger: {self._hunger}, thirst: {self._thirst}, position: {self._pos}, state: {self._state}]"
    def tick(self, gameworld):
        self._hunger += 0.01
        self._thirst += 0.01
        if (self._hunger > 1 or self._thirst > 1):
            gameworld.kill(self)
        if (self._state == 0):
            self.chose_state(gameworld.features())
        elif (self._state == 1):
            self._remaining_ticks -= 1
            if (self._remaining_ticks == 0):
                self.eat()
        elif (self._state == 2):
            self._remaining_ticks -= 1
            if (self._remaining_ticks == 1):
                self.drink()
        elif self._state in (3, 4):
            self.advance()
        else:
            raise ValueError("illegal state")

    def move(self):
        self._pos += (self._target - self._pos).normalize()
        return self._pos.distance(self._target) < 2

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

    def eat(self):
        self._hunger = max(0, self._hunger - 0.25)
    def drink(self):
        self._thirst = max(0, self._thirst - 0.25)
    def advance(self):
        result = self.move()
        if result == 0:
            self._state = 2
            self._remaining_ticks == 5
        elif result == 1:
            self._state = 0
