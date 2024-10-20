# Sorting Visualizer

from tkinter import *
from tkinter import ttk
from ttkbootstrap import *
from numpy import linspace, random
import time

class SortingApp:
    def __init__(self, root, title) -> None:
        self.root = root
        self.root.title(title)
        self.root.geometry('805x440')

        ttk.Button(self.root, text='Start Sorting', command=self.start_sorting).grid(row=0, column=14)
        ttk.Button(self.root, text='Shuffle', command=self.shuffle).grid(row=0, column=13)

        self.canvas = Canvas(self.root, width=800, height=405, highlightbackground='dodgerblue',
                             bg='black', highlightthickness=2)
        self.canvas.grid(row=1, columnspan=15)

        self.N = 50
        self.data = linspace(5, 400, self.N)
        self.colors = ['dodgerblue' for _ in range(self.N)]
        self.speed = 5 / 1000
        self.shuffle()

    def reset_colors(self, color='dodgerblue'):
        self.colors = [color for _ in range(self.N)]

    def shuffle(self):
        self.reset_colors()
        random.shuffle(self.data)
        self.display(self.colors)

    def display(self, array_color: list):
        gap = self.N * 0.01
        width = lambda x: (800 - 99 * x) / self.N
        self.canvas.delete('all')

        for i in range(self.N):
            x0 = i * width(gap) + i * gap
            y0 = 0
            x1 = (i + 1) * width(gap) + i * gap
            y1 = self.data[i]
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=array_color[i])

        self.root.update_idletasks()

    def start_sorting(self):
        for steps in range(self.N - 1):
            a = self.N - 1 - steps
            for i in range(a):
                self.colors[i] = self.colors[i + 1] = 'yellow'
                self.display(self.colors)
                time.sleep(self.speed)
                if self.data[i] > self.data[i + 1]:
                    self.colors[:a + 1] = ['dodgerblue'] * (a + 1)
                    self.colors[i] = self.colors[i + 1] = 'red'
                    self.display(self.colors)
                    time.sleep(self.speed)
                    self.data[i], self.data[i + 1] = self.data[i + 1], self.data[i]
                    self.colors[i] = self.colors[i + 1] = 'lime'
                    self.display(self.colors)
                    time.sleep(self.speed)
                self.colors[i] = self.colors[i + 1] = 'dodgerblue'
            self.colors[a:] = ['green'] * (self.N - a)
        self.display(self.colors)
        self.reset_colors('green')
        self.display(self.colors)


if __name__ == '__main__':
    window = Style(theme='darkly').master
    SortingApp(window, 'Bubble Sort')
    window.mainloop()
