from tkinter import *
from random import random
from math import floor, ceil

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

root = Tk()
f = Frame(root)
f.grid()
c = Canvas(f, bg="white", width="500", height="500")
c.grid()

n = NoiseSpace(50, 10, 5)
n.render(c)

root.mainloop()
