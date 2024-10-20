# Sorting Visualizer

from tkinter import *
from tkinter import ttk, messagebox
from ttkbootstrap import *
from numpy import random, linspace, uint16
import time

class SortingVisualizer:
    sort_names = ['bubble', 'insertion', 'selection', 'merge', 'quick']
    sorts = {k: False for k in sort_names}
    buttons: list

    def __init__(self, root, title) -> None:
        self.root = root
        self.root.title(title)

        # Restricting window from resizing
        self.root.resizable(width=0, height=0)

        # Buttons
        button_styles = 'info.TButton'
        button_width = 15
        self.buttons = []
        for col, sort_name in enumerate(self.sort_names):
            sort_button = ttk.Button(self.root, text=f'{sort_name.capitalize()} Sort',
                                     style=button_styles, padding=5, width=button_width,
                                     command=getattr(self, sort_name))
            sort_button.grid(column=col, row=1, padx=5, pady=5)
            self.buttons.append(sort_button)

        ttk.Button(self.root, text='Shuffle', style='info.Outline.TButton', padding=5, width=15,
                   command=self.shuffle).grid(column=len(self.sort_names), row=1, padx=5, pady=5)

        ttk.Button(self.root, text='Start', padding=5, width=15, command=self.start).grid(column=len(self.sort_names),
                                                                                        row=2, padx=5, pady=5)

        # Canvas
        self.canvas = Canvas(self.root, width=800 - 5, height=400, highlightbackground="dodgerblue",
                             highlightthickness=2, bg='black')
        self.canvas.grid(row=4, padx=5, pady=10, columnspan=len(self.sort_names) + 1)

        # Speed & Array Size
        ttk.Label(self.root, text='Speed & Array Size:').grid(row=2, column=0)
        self.arraysize = ttk.Scale(self.root, from_=6, to=120, length=380, style='success.Horizontal.TScale', value=10,
                                   command=lambda x: self.slide_function())
        self.arraysize.grid(row=2, column=1, columnspan=len(self.sort_names) - 1)

        # Default values
        self.speed = 0.2  # sorting speed
        self.N = 10
        self.colours = ['dodgerblue' for _ in range(self.N)]
        self.shuffle()

        # Color arrays
        self.__sorted_array = ['lime' for _ in range(self.N)]
        self.__default_colours = ['dodgerblue' for _ in range(self.N)]

    def display(self, N: int, a: list, colors: list) -> None:
        """
        Display the array elements in the canvas.

        Parameters:
            N (int): Number of rectangles.
            a (list): Array of heights of rectangles.
            colors (list): Array of colors for each rectangle.
        """
        self.canvas.delete('all')
        width = (1570) / (3 * N - 1)
        gap = width / 2

        for i in range(N):
            self.canvas.create_rectangle(7 + i * width + i * gap, 0,
                                         7 + (i + 1) * width + i * gap, a[i], fill=colors[i])

        self.root.update_idletasks()

    def slide_function(self) -> None:
        """
        Update array size and speed based on the sliders.
        """
        self.N = int(self.arraysize.get())
        self.data = linspace(5, 400, self.N, dtype=uint16)
        self.speed = 5 / self.arraysize.get()
        self.colours = ['dodgerblue' for _ in range(self.N)]
        self.shuffle()

    def shuffle(self) -> None:
        """
        Shuffle the array and display it.
        """
        self.canvas.delete('all')
        self.data = linspace(5, 400, self.N, dtype=uint16)
        random.shuffle(self.data)
        self.display(self.N, self.data, self.colours)

    def _helper(func):
        def inner(self):
            btn_name = func.__name__
            if self.sorts[btn_name] is False:
                self.sorts[btn_name] = True
                for k in self.sorts.keys():
                    if k == btn_name:
                        self.buttons[k].config(style='success.TButton')
                    else:
                        self.sorts[k] = False
                        self.buttons[k].config(style='info.TButton')
            else:
                self.sorts[btn_name] = False
                self.buttons[btn_name].config(style='info.TButton')

        return inner

    @_helper
    def bubble(self):
        pass

    @_helper
    def merge(self):
        pass

    @_helper
    def selection(self):
        pass

    @_helper
    def quick(self):
        pass

    @_helper
    def insertion(self):
        pass

    def start(self) -> None:
        """
        Start the selected sorting algorithm.
        """
        if self.sorts['bubble'] is True:
            # Bubble Sort
            for i in range(self.N - 1):
                for j in range(self.N - 1 - i):
                    self.display(self.N, self.data,
                                  ['purple' if a == j or a == j + 1 else 'green' if a > self.N - 1 - i else 'dodgerblue'
                                   for a in range(self.N)])
                    time.sleep(self.speed)
                    if self.data[j] > self.data[j + 1]:
                        self.display(self.N, self.data,
                                      ['red' if a == j or a == j + 1 else 'green' if a > self.N - 1 - i else 'dodgerblue'
                                       for a in range(self.N)])
                        time.sleep(self.speed)
                        self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]
                        self.display(self.N, self.data,
                                      ['lime' if a == j or a == j + 1 else 'green' if a > self.N - 1 - i else 'dodgerblue'
                                       for a in range(self.N)])
                        time.sleep(self.speed)
            self.display(self.N, self.data, self.__sorted_array)

        elif self.sorts['insertion'] is True:
            # Insertion Sort
            for j in range(1, len(self.data)):
                key = self.data[j]
                i = j - 1
                self.display(self.N, self.data,
                              ['purple' if a == i or a == i + 1 else 'green' if a <= j else 'dodgerblue' for a in
                               range(self.N)])
                time.sleep(self.speed)
                while i >= 0 and self.data[i] > key:
                    self.data[i + 1] = self.data[i]
                    self.display(self.N, self.data,
                                  ['yellow' if a == i else 'green' if a <= j else 'dodgerblue' for a in range(self.N)])
                    time.sleep(self.speed)
                    i -= 1
                self.data[i + 1] = key
            self.display(self.N, self.data, self.__sorted_array)

        elif self.sorts['selection'] is True:
            # Selection Sort
            for i in range(len(self.data) - 1):
                min_index = i
                for j in range(i + 1, len(self.data)):
                    self.display(self.N, self.data,
                                  ['yellow' if a == min_index or a == i else 'green' if a <= i else 'dodgerblue' for a
                                   in range(self.N)])
                    time.sleep(self.speed)
                    if self.data[min_index] > self.data[j]:
                        self.display(self.N, self.data,
                                      ['red' if a == min_index or a == j else 'green' if a <= i else 'dodgerblue'
                                       for a in range(self.N)])
                        time.sleep(self.speed)
                        min_index = j
                if min_index != i:
                    self.data[i], self.data[min_index] = self.data[min_index], self.data[i]
                    self.display(self.N, self.data,
                                  ['lime' if a == min_index or a == i else 'green' if a <= i else 'dodgerblue' for a
                                   in range(self.N)])
                    time.sleep(self.speed)
            self.display(self.N, self.data, self.__sorted_array)

        elif self.sorts['merge'] is True:
            # Merge Sort
            self.mergesort(self.data, 0, self.N - 1)
            self.display(self.N, self.data, self.__sorted_array)

        elif self.sorts['quick'] is True:
            # Quick Sort
            self.quicksort(self.data, 0, self.N - 1)
            self.display(self.N, self.data, self.__sorted_array)

        else:
            # Show error message
            messagebox.showerror("Algorithm Visualizer", "You didn't select any sorting algorithm")

    def mergesort(self, a, front, last):
        """
        Merge Sort algorithm.

        Parameters:
            a (list): The array to be sorted.
            front (int): Index of the first element.
            last (int): Index of the last element.
        """
        if front < last:
            mid = (front + last) // 2

            self.mergesort(a, front, mid)
            self.mergesort(a, mid + 1, last)

            self.display(self.N, self.data, self.__default_colours)

            rj = mid + 1
            if a[mid] <= a[mid + 1]:
                return

            while front <= mid and rj <= last:
                self.display(self.N, self.data,
                              ['yellow' if x == front or x == rj else 'dodgerblue' for x in range(self.N)])
                time.sleep(self.speed)
                if a[front] <= a[rj]:
                    self.display(self.N, self.data,
                                  ['lime' if x == front or x == rj else 'dodgerblue' for x in range(self.N)])
                    time.sleep(self.speed)
                    front += 1
                else:
                    self.display(self.N, self.data,
                                  ['red' if x == front or x == rj else 'dodgerblue' for x in range(self.N)])
                    time.sleep(self.speed)
                    temp = a[rj]
                    i = rj
                    while i != front:
                        a[i] = a[i - 1]
                        i -= 1
                    a[front] = temp
                    self.display(self.N, self.data,
                                  ['lime' if x == front or x == rj else 'dodgerblue' for x in range(self.N)])
                    time.sleep(self.speed)

                    front += 1
                    mid += 1
                    rj += 1

            self.display(self.N, self.data, self.__default_colours)
            time.sleep(self.speed)

    def partition(self, a, i, j):
        """
        Partitioning function for Quick Sort.

        Parameters:
            a (list): The array to be partitioned.
            i (int): Index from the front.
            j (int): Index from the back.

        Returns:
            int: Partition index.
        """
        l = i  # left index

        pivot = a[i]
        piv_index = i

        while i < j:
            while i < len(a) and a[i] <= pivot:
                i += 1
                self.display(self.N, self.data,
                              ['purple' if x == piv_index else 'yellow' if x == i else "dodgerblue" for x in
                               range(self.N)])
                time.sleep(self.speed)
            while a[j] > pivot:
                j -= 1
            if i < j:
                self.display(self.N, self.data,
                              ['red' if x == i or x == j else "dodgerblue" for x in range(self.N)])
                time.sleep(self.speed)
                a[i], a[j] = a[j], a[i]
                self.display(self.N, self.data,
                              ['lime' if x == i or x == j else "dodgerblue" for x in range(self.N)])
                time.sleep(self.speed)
        a[j], a[l] = a[l], a[j]
        return j

    def quicksort(self, a, i, j):
        """
        Quick Sort algorithm.

        Parameters:
            a (list): The array to be sorted.
            i (int): Index from the front.
            j (int): Index from the back.
        """
        if i < j:
            x = self.partition(a, i, j)
            self.quicksort(a, i, x - 1)
            self.quicksort(a, x + 1, j)

if __name__ == '__main__':
    win = Style(theme='darkly').master
    obj = SortingVisualizer(win, 'Sorting Algorithm Visualizer')

    win.mainloop()
