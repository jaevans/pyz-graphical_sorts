#!/usr/bin/env python3

from random import randint
from collections import namedtuple
import pygame
from pygame import Rect
import ptext

import pgzrun

from threading import Event, Thread, Lock

draw_event = Event()

DATA_SIZE=50

FPS=24

DataPoint = namedtuple('DataPoint',['value','color'])

class SortObject(Thread):
    name = "Unknown"
    def __init__(self, starting_data, surface):
        super().__init__()
        self._data = starting_data[:]
        self._sorted = False
        self._surface = surface
        self._status = {}
        self._hilights = []
        self.drawing_ready = Lock()


    @staticmethod
    def _swap(x,y):
        return y,x

    def _draw_frame(self):
        self.drawing_ready.acquire()
        bar_width = self._surface.get_width() / len(self._data)
        self._surface.fill(pygame.Color('lightblue'))
        for hilight in self._hilights:
            r = Rect(hilight * bar_width, 0, bar_width, self._surface.get_height())
            pygame.draw.rect(self._surface, pygame.Color('red'), r, 0)
            # pygame.draw.rect(self._surface, pygame.Color('black'), r, 1)
        for index, item in enumerate(self._data):
            r = Rect((index * bar_width) + 1, self._surface.get_height() - item.value, bar_width - 2, item.value )
            pygame.draw.rect(self._surface, pygame.Color(item.color), r, 0)
            pygame.draw.rect(self._surface, pygame.Color('black'), r, 1)
        if self.is_sorted:
            text_color = 'green'
        else:
            text_color = 'orange'
        ptext.draw(self.name, (10, 10), surf=self._surface, color=text_color, owidth=1, ocolor = 'black')
        self.drawing_ready.release()
        draw_event.wait()

    @property
    def surface(self):
        return self._surface

    def _swap_indices(self, x, y):
        v1, v2 = self._swap(self._data[x], self._data[y])
        self._data[x], self._data[y] = v1, v2

    @property
    def is_sorted(self):
        return self._sorted

    def do_sort(self):
        raise(NotImplementedError)

    def run(self):
        self._draw_frame() # Draw the first frame
        self.do_sort()

class BubbleSort(SortObject):
    name = "BubbleSort"

    def do_sort(self):
        while not self.is_sorted:
            done_sorting = True
            for sort_pointer in range(len(self._data) - 1):
                self._hilights = (sort_pointer, sort_pointer + 1)
                self._draw_frame()
                if self._data[sort_pointer].value > self._data[sort_pointer + 1].value:
                    self._swap_indices(sort_pointer, sort_pointer + 1)
                    self._draw_frame()
                    done_sorting = False
            self._sorted = done_sorting
        # Draw the final sorted frame
        self._hilights = []
        self._draw_frame()

class OptimizedBubbleSort(SortObject):
    name = "OptimizedBubbleSort"

    def do_sort(self):
        max_sort = len(self._data)
        while not self.is_sorted:
            done_sorting = True
            for sort_pointer in range(max_sort - 1):
                self._hilights = (sort_pointer, sort_pointer + 1)
                self._draw_frame()
                if self._data[sort_pointer].value > self._data[sort_pointer + 1].value:
                    self._swap_indices(sort_pointer, sort_pointer + 1)
                    self._draw_frame()
                    done_sorting = False
            max_sort -= 1
            self._sorted = done_sorting
        # Draw the final sorted frame
        self._hilights = []
        self._draw_frame()

class ShellSort(SortObject):
    name = "ShellSort"

    def do_sort(self):
        gap = len(self._data)

        while gap > 1:
            gap = gap // 2
            for i in range(gap, len(self._data), gap):
                temp = self._data[i]
                j = i
                while j >= gap and self._data[j - gap] > temp:
                    self._hilights = (j, j - gap)
                    self._draw_frame()
                    self._data[j] = self._data[j - gap]
                    self._draw_frame()
                    j -= gap
                self._draw_frame()
                self._data[j] = temp
        self._sorted = True
        # Draw the final sorted frame
        self._hilights = []
        self._draw_frame()

class InsertionSort(SortObject):
    name = "InsertionSort"

    def do_sort(self):
        # An insertion sort is a shell sort with gap = 1
        gap = 2

        while gap > 1:
            gap = gap // 2
            for i in range(gap, len(self._data), gap):
                temp = self._data[i]
                j = i
                while j >= gap and self._data[j - gap] > temp:
                    self._hilights = (j, j - gap)
                    self._draw_frame()
                    self._data[j] = self._data[j - gap]
                    self._draw_frame()
                    j -= gap
                self._draw_frame()
                self._data[j] = temp
        self._sorted = True
        # Draw the final sorted frame
        self._hilights = []
        self._draw_frame()

class QuickSort(SortObject):
    name = "QuickSort"

    def __partition(self, lo, hi):
        pivot = self._data[hi]
        i = lo
        for j in range(lo, hi):
            self._hilights = (j, hi)
            self._draw_frame()
            if self._data[j] < pivot:
                self._hilights = (i,j)
                self._draw_frame()
                self._swap_indices(i,j)
                self._draw_frame()
                i = i + 1
        self._hilights = (i,hi)
        self._draw_frame()
        self._swap_indices(i, hi)
        self._draw_frame()
        return i

    def __quicksort(self, lo, hi):
        if lo < hi:
            p = self.__partition(lo, hi)
            self.__quicksort(lo, p - 1)
            self.__quicksort(p + 1, hi)

    def do_sort(self):
        self.__quicksort(0, len(self._data) - 1)
        self._sorted = True
        # Draw the final sorted frame
        self._hilights = []
        self._draw_frame()

class SelectionSort(SortObject):
    name = "SelectionSort"

    def do_sort(self):
        for j in range(len(self._data) - 1):
            iMin = j
            for i in range(j + 1, len(self._data)):
                self._hilights = (i,iMin)
                self._draw_frame()
                if self._data[i] < self._data[iMin]:
                    iMin = i
            if iMin != j:
                self._hilights = (j, iMin)
                self._draw_frame()
                self._swap_indices(j, iMin)
                self._draw_frame()
        # Draw the final sorted frame
        self._sorted = True
        self._hilights = []
        self._draw_frame()

data = [DataPoint(randint(2,100), "#%06X" % randint(0, (2**24) - 1)) for x in range(DATA_SIZE)]

sorter_types = [
    BubbleSort,
    OptimizedBubbleSort,
    ShellSort,
    InsertionSort,
    QuickSort,
    SelectionSort,
]

BOX_WIDTH = 400
BOX_HEIGHT = 100
Sorter = namedtuple('Sorter', ['name','sorter'])

WIDTH = BOX_WIDTH + 10
HEIGHT = ((BOX_HEIGHT + 5) * len(sorter_types)) + 5

sorters = None

def draw():
    screen.fill('grey')
    draw_event.clear()
    for index, s in enumerate(sorters):
        s.sorter.drawing_ready.acquire()
        screen.blit(s.sorter.surface, (5, 5 + (index * (BOX_HEIGHT + 5))))
        s.sorter.drawing_ready.release()

time_accumlate = 1.0
def update(dt):
    global time_accumlate
    if time_accumlate >= 1.0 / FPS:
        draw_event.set()
        time_accumlate = 0
    else:
        time_accumlate += dt

    global sorters
    if sorters is None:
        # This is the first time through, but we have to do this here so the
        # video mode has been set
        sorters = []
        for s in sorter_types:
            sorters.append(
                Sorter(name = s.name, 
                    sorter = s(data, 
                        pygame.Surface((BOX_WIDTH, BOX_HEIGHT))
                    )
                )
            )
            sorters[-1].sorter.start()

if __name__ == "__main__":
    pgzrun.go()
