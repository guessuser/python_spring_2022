from random import randrange as rnd, choice, shuffle
from tkinter import *
import itertools, time, copy
import time

root = Tk()
root.geometry('800x600')

canv = Canvas(root, bg='white')
canv.pack(fill=BOTH, expand=1)

nr = 6
nc = 6
np = 6
m = 24
y0 = x0 = m


class cell():
    def __init__(self):
        self.n = 0
        self.bomb = 0
        self.mode = 'closed'

class Layer():
    def __init__(self):
        self.n = 0

    def change_up(self):
        self.n += 1


    def change_down(self):
        self.n -= 1

layer = Layer()
def new_game():
    global a
    a = [[[cell() for c in range(nc)] for r in range(nr)] for p in range(np)]
    bomb_count = 20
    while bomb_count > 0:
        r = rnd(nr)
        c = rnd(nc)
        p = rnd(np)
        if not a[r][c][p].bomb:
            a[r][c][p].bomb = 1
            bomb_count -= 1

    for r in range(nr):
        for c in range(nc):
            for p in range(np):
                k = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        for dp in [-1, 0, 1]:
                            rr = r + dr
                            cc = c + dc
                            pp = p + dp
                            if rr in range(nr) and cc in range(nc) and pp in range(np):
                                if a[rr][cc][pp].bomb:
                                    k += 1
                a[r][c][p].n = k
    paint()


def paint():
    canv.delete(ALL)

    for r in range(nr):
        for c in range(nc):
            x = x0 + c * m
            y = y0 + r * m
            p = layer.n
            if a[r][c][p].mode == 'opened':
                if not a[r][c][p].bomb:
                    canv.create_rectangle(x, y, x + m, y + m, fill='white')
                    if a[r][c][p].n > 0:
                        canv.create_text(x + m // 2, y + m // 2, text=a[r][c][p].n)
                else:
                    canv.create_rectangle(x, y, x + m, y + m, fill='red')
            elif a[r][c][p].mode == 'closed':
                canv.create_rectangle(x, y, x + m, y + m, fill='gray')
            elif a[r][c][p].mode == 'flag':
                canv.create_rectangle(x, y, x + m, y + m, fill='green')
def cell_change(r, c, p, button):
    if a[r][c][p].mode == 'closed':
        if button == 1:
            time.sleep(0.001)
            a[r][c][p].mode = 'opened'
            if a[r][c][p].n == 0:
                for dp in [-1, 0, 1]:
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            rr = r + dr
                            cc = c + dc
                            pp = p +dp
                            if rr in range(nr) and cc in range(nc) and pp in range(np):
                                paint()
                                canv.update()
                                cell_change(rr, cc, pp, 1)

            if a[r][c][p].bomb:
                print('boom!!!')
        elif button == 3:
            a[r][c][p].mode = 'flag'
    elif a[r][c][p].mode == 'flag' and button == 3:
        a[r][c][p].mode = 'closed'

def click(event):
    r = (event.y - y0) // m
    c = (event.x - x0) // m
    p=layer.n
    if r in range(nr) and c in range(nc):
        cell_change(r, c, p, event.num)
    paint()


new_game()

def task_up(event):
    layer.change_up()
    paint()

def task_down(event):
    layer.change_down()
    paint()

button_up = Button(canv, width = 4, height = 2, text = 'up')
button_up.focus()
button_up.place(x = 250, y = 100)
button_up.bind('<Button-1>', task_up)

button_down = Button(canv, width = 4, height = 2, text = 'down')
button_down.focus()
button_down.place(x = 250, y = 140)
button_down.bind('<Button-1>', task_down)

canv.bind('<1>', click)
canv.bind('<3>', click)
mainloop()