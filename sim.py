#!/usr/bin/env python3

from animals import Beaver, Position, Lynx
from threading import Thread
from time import sleep
from sys import exit
from tkinter import *

class WorldCanvas(Canvas):
    def __init__(self, master):
        Canvas.__init__(self, master, bg="green", width=500, height=500)
        self._beavers = []
        self._food = []
        self._water = []

    def _reset_beavers(self):
        for i in self._beavers:
            self.delete(i)
        self._beavers = []

    def _reset_background(self):
        for i in self._water:
            self.delete(i)
        for i in self._food:
            self.delete(i)
        self._food = []
        self._water = []
    def redraw_beavers(self, beavers):
        self._reset_beavers()
        for beaver in beavers:
            self._beavers.append(self.draw_beaver(*[i*5 for i in beaver.get_coords()]))
    def redraw_background(self, food, water):
        self._reset_background()
        for tree in food:
            self._food.append(self.draw_food(*[i*5 for i in tree.image_coords()]))
        for pool in water:
            self._water.append(self.draw_water(*[i*5 for i in pool.image_coords()]))
    def draw_beaver(self, x1, y1, x2, y2):
        return self.create_oval(x1, y1, x2, y2, fill="#c97e2c", outline="#c97e2c")
    def draw_food(self, x1, y1, x2, y2):
        return self.create_rectangle(x1, y1-10, x2, y2+10, fill="#754a1a", outline="#754a1a")
    def draw_water(self, x1, y1, x2, y2):
        return self.create_oval(x1, y1, x2, y2, fill="blue", outline="blue")
    def draw_lynx(self, x1, y1, x2, y2):
        return self.create_oval(x1, y1, x2, y2, fill="tan", outline="tan")

class World:
    def __init__(self, num_beavers, num_food, num_water, num_lynx, master):
        self._beavers = [Beaver(Position.rand(0, 100)) for i in range(num_beavers)]
        self._food = [Position.rand(0, 100) for i in range(num_food)]
        self._water = [Position.rand(0, 100) for i in range(num_water)]
        self._lynx = [Lynx(Position.rand(0, 100)) for i in range(num_lynx)]
        self._tick_time = 0.1

        self.frame = Frame(root)
        self.frame.grid()
        self.canvas = WorldCanvas(root)
        self.canvas.grid()
        self.render_background()
        self.render_beavers()

        self.mainloop()

    def mainloop(self):
        tick_thread = Thread(target = self._tick)
        tick_thread.start() #tick all of the beavers
        self.render_background() #render background while waiting
        tick_thread.join() #join threads
        self.render_beavers() #render beavers
        self.frame.after(10, self.mainloop)

    def _tick(self):
        sleep(self._tick_time)
        for beaver in self._beavers:
            beaver.tick(self)
        for lynx in self._lynx:
            lynx.tick(self)
        if len(self._beavers) == 0 and len(self._lynx) == 0:
            exit()
    def render_background(self):
        self.canvas.redraw_background(self._food, self._water)
    def render_beavers(self):
        self.canvas.redraw_beavers(self._beavers)
    def features(self, position):
        return {"food": position.nearest(self._food), "water": position.nearest(self._water), "beaver": position.nearest([i.get_pos() for i in self._beavers])}
    def kill(self, animal):
        if isinstance(animal, Beaver):
            for i in range(len(self._beavers)):
                if self._beavers[i] is animal:
                    self._beavers.pop(i)
                    return
        elif isinstance(animal, Lynx):
            for i in range(len(self._lynx)):
                if self._lynx[i] is animal:
                    self._beavers.pop(i)
                    return
    def consume(self, resource, position):
        if (resource == "water"):
            self._water.remove(position)
        else:
            self._food.remove(position)

root = Tk()
w = World(5, 20, 20, 5, root)
root.mainloop()
