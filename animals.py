#!/usr/bin/env python3
from random import random, randint
from math import sqrt
from collections import OrderedDict
from threading import Thread
from time import sleep
from sys import exit

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
        return f"Beaver: [hunger: {self._hunger:.3f}, thirst: {self._thirst:.3f}, position: {self._pos}, state: {self._state:.3f}]"
    def tick(self, gameworld):
        print("ticking: "+str(self))
        self._hunger += 0.01
        self._thirst += 0.01
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
        self._pos += (self._target - self._pos).normalize()
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

class World:
    def __init__(self, num_beavers, num_food, num_water):
        self._beavers = [Beaver(Position.rand(0, 100)) for i in range(num_beavers)]
        self._food = [Position.rand(0, 100) for i in range(num_food)]
        self._water = [Position.rand(0, 100) for i in range(num_water)]
        self._tick_time = 0.5
    def mainloop(self):
        self._loop()
    def _loop(self):
        while True:
            tick_thread = Thread(target = self._tick)
            tick_thread.start() #tick all of the beavers
            self.render_background() #render background while waiting
            tick_thread.join() #join threads
            self.render_beavers() #render beavers
    def _tick(self):
        sleep(self._tick_time)
        print("========= GAMETICK =========")
        print(f"beavers: {len(self._beavers)}, water: {len(self._water)}, food: {len(self._food)}")
        for beaver in self._beavers:
            beaver.tick(self)
        if len(self._beavers) == 0:
            exit()
        print("\n\n\n\n")
    def render_background(self):
        pass
    def render_beavers(self):
        pass
    def food_water(self, position):
        return {"food": position.nearest(self._food), "water": position.nearest(self._water)}
    def kill(self, animal):
        if isinstance(animal, Beaver):
            for i in range(len(self._beavers)):
                if self._beavers[i] is animal:
                    self._beavers.pop(i)
                    return
    def consume(self, resource, position):
        if (resource == "water"):
            self._water.remove(position)
        else:
            self._food.remove(position)


w = World(1, 20, 20)
w.mainloop()
