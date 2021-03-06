#!/usr/bin/env python3
from random import random, randint
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
    @staticmethod
    def rand(lower, upper):
        return Position(randint(lower, upper), randint(lower, upper))
    def __str__(self):
        return "NULL" if self._is_null else f"({self._x:.2f}, {self._y:.2f})"
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
        if (length == 0):
            return Position(0, 0)
        return Position(self._x/length, self._y/length)
    def nearest(self, others):
        if len(others) == 0:
            return Position.null()
        output = others[0]
        for i in range(1, len(others)):
            output = output if output.distance(self) < others[i].distance(self) else others[i]
        return output
    def image_coords(self):
        return (self._x, self._y, self._x+1, self._y+1)

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
        self._speed = 0.5
    def __str__(self):
        return f"Beaver: [hunger: {self._hunger:.3f}, thirst: {self._thirst:.3f}, position: {self._pos}, state: {self._state:.3f}]"
    def tick(self, gameworld):
        self._hunger += 0.002
        self._thirst += 0.002
        if (self._hunger > 1 or self._thirst > 1):
            print("death")
            gameworld.kill(self)
        if (self._state == 0):
            self._chose_state(gameworld.food_water(self._pos))
        elif (self._state == 1):
            self._remaining_ticks -= 1
            if (self._remaining_ticks == 0):
                self._eat(gameworld)
        elif (self._state == 2):
            self._remaining_ticks -= 1
            if (self._remaining_ticks == 1):
                self._drink(gameworld)
        elif self._state in (3, 4):
            self._advance(self._state)
        else:
            raise ValueError("illegal state")

    def _move(self):
        self._pos += (self._target - self._pos).normalize() * self._speed
        return self._pos.distance(self._target) > 2

    def _chose_state(self, features):
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

    def _eat(self, world):
        print("eat")
        self._hunger = max(0, self._hunger - 0.25)
        world.consume("food", world.food_water(self._pos)["food"])
        self._state = 0

    def _drink(self, world):
        print("drink")
        self._thirst = max(0, self._thirst - 0.25)
        world.consume("water", world.food_water(self._pos)["water"])
        self._state = 0

    def _advance(self, target):
        result = self._move()
        if result == 0:
            self._state = target - 2
            self._remaining_ticks = 5
        elif result == 1:
            self._state = 0
    def get_coords(self):
        return self._pos.image_coords()
