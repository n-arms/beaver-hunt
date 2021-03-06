from tkinter import *
from random import random

class NoiseSpace:
    def __init__(self, size):
        self.points = [random() for i in range(size)]
    def get(self, x):
        if isinstance(x, int):
            return self.points[x]
        return NoiseSpace.blend(x//1, self.points[x//1], x//1 + 1, self.points[x//1 + 1], x)
    def render(self, canvas):
        for i in range(len(self.points)*10):
            canvas.create_rectangle(i, self.points[i//10]*10+250, (i+0.1), (self.points[i//10]+0.1)*10+250)
    @staticmethod
    def blend(x1, y1, x2, y2, a):
        return ((y1 - y2) / (x1 - x2)) * (a - x1) + y1

root = Tk()
f = Frame(root)
f.grid()
c = Canvas(f, bg="white", width="500", height="500")
c.grid()

n = NoiseSpace(50)
n.render(c)


root.mainloop()
