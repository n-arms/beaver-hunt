from tkinter import *
from random import random
from math import floor, ceil
from animals import Position

class NoiseSpace:
    def __init__(self, size, amp, freq):
        self.points = [random()*amp for i in range(size)]
        self.amp = amp
        self.freq = freq
    def get(self, x):
        if floor(x) == ceil(x):
            return self.points[int(x)]
        return NoiseSpace.blend(floor(x), self.points[floor(x)], ceil(x), self.points[ceil(x)], x)
    def render(self, canvas):
        for i in [i/self.freq for i in range(len(self.points)*self.freq - self.freq)]:
            canvas.create_rectangle(i*self.freq, self.get(i)+250, i*self.freq+0.1, self.get(i)+250.1)
    @staticmethod
    def blend(x1, y1, x2, y2, a):
        return ((y1 - y2) / (x1 - x2)) * (a - x1) + y1

class NoiseSpace2:
    def __init__(self, size, amp, freq): #let freq be the size of each cell
        self.freq = freq
        self.amp = amp
        self.size = size
        self.points = {Position(a, b): Position(a+random(), b+random()) for a in range(self.size//freq) for b in range(size//freq)}
    def _get_cells(self, pos):
        return [pos//self.freq + i for i in [Position(a, b) for a in range(-1, 2) for b in range(-1, 2)]]
    def get(self, pos):
        return min([self.points[i].distance(pos//self.size) for i in self._get_cells(pos)])
    def render(self, canvas):
        for i in range(self.freq*2, self.size-self.freq*2):
            for j in range(self.freq*2, self.size-self.freq*2):
                canvas.create_rectangle(i*10, j*10, i*10+10, j*10+10, outline="#"+(hex(int(self.get(Position(i, j)) * 15))[2:] * 3))
        for i in self.points:
            canvas.create_oval(*[i*10 for i in i.image_coords()])


root = Tk()
f = Frame(root)
f.grid()
c = Canvas(f, bg="white", width="500", height="500")
c.grid()

n = NoiseSpace2(50, 10, 5)
n.render(c)

root.mainloop()
