#!/usr/bin/env python3

from random import randint
from collections import namedtuple
import pygame
from pygame import Rect
import ptext
import math

import pgzrun

DATA_SIZE=100

FPS=25

DataPoint = namedtuple('DataPoint',['value','color'])

class SortObject(object):
    name = "Unknown"
    def __init__(self, starting_data, surface):
        super().__init__()
        self._data = starting_data[:]
        self.sorted = False
        self._surface = surface
        self._status = {
            'compares': 0,
            'swaps': 0
        }
        self._hilights = []
        self.sort = self._do_sort()

    @staticmethod
    def _swap(x,y):
        return y,x
    
    @property
    def compares(self):
        return self._status['compares']
    
    def _inc_compares(self):
        self._status['compares'] += 1
    
    @property
    def swaps(self):
        return self._status['swaps']
    
    def _inc_swaps(self):
        self._status['swaps'] += 1

    def get_frame(self):
        bar_width = self._surface.get_width() / len(self._data)
        self._surface.fill(pygame.Color('lightblue'))
        for hilight in self._hilights:
            r = Rect(hilight * bar_width, 0, bar_width, self._surface.get_height())
            pygame.draw.rect(self._surface, pygame.Color('red'), r, 0)
        for index, item in enumerate(self._data):
            r = Rect((index * bar_width) + 1, self._surface.get_height() - item.value, bar_width - 2, item.value )
            pygame.draw.rect(self._surface, pygame.Color(item.color), r, 0)
            pygame.draw.rect(self._surface, pygame.Color('black'), r, 1)
        if self.sorted:
            text_color = '#00cc00ff' # Link Green
        else:
            text_color = 'orange'
        ptext.draw(self.name, (10, 10), surf=self._surface, color=text_color, owidth=1, ocolor = 'black')
        ptext.draw("C: %d, S: %d " % (self.compares, self.swaps), (10, 24), surf=self._surface, color=text_color, owidth=1, ocolor = 'black')
        return self._surface

    @property
    def surface(self):
        return self._surface

    def _swap_indices(self, x, y):
        v1, v2 = self._swap(self._data[x], self._data[y])
        self._data[x], self._data[y] = v1, v2
        self._inc_swaps()

    @property
    def sorted(self):
        return self.__dict__['sorted']

    @sorted.setter
    def sorted(self, value):
        self.__dict__['sorted'] = value
        if self.sorted:
            temp_data = [s.value for s in self._data[:]]
            temp_data.sort()
            if temp_data != [s.value for s in self._data]:
                print("Problem in %s, data is not sorted correctly!" % self.name)
                print([s.value for s in self._data])

    def _do_sort(self):
        raise(NotImplementedError)

class BubbleSort(SortObject):
    name = "BubbleSort"

    def _do_sort(self):
        while not self.sorted:
            done_sorting = True
            for sort_pointer in range(len(self._data) - 1):
                self._hilights = (sort_pointer, sort_pointer + 1)
                self._inc_compares()
                (yield)
                if self._data[sort_pointer].value > self._data[sort_pointer + 1].value:
                    self._swap_indices(sort_pointer, sort_pointer + 1)
                    (yield)
                    done_sorting = False
            self.sorted = done_sorting
        # Draw the final sorted frame
        self._hilights = []

class OptimizedBubbleSort(SortObject):
    name = "OptimizedBubbleSort"

    def _do_sort(self):
        max_sort = len(self._data)
        while not self.sorted:
            done_sorting = True
            for sort_pointer in range(max_sort - 1):
                self._hilights = (sort_pointer, sort_pointer + 1)
                self._inc_compares()
                yield
                if self._data[sort_pointer].value > self._data[sort_pointer + 1].value:
                    self._swap_indices(sort_pointer, sort_pointer + 1)
                    yield
                    done_sorting = False
            max_sort -= 1
            self.sorted = done_sorting
        # Draw the final sorted frame
        self._hilights = []

class ShellSort(SortObject):
    name = "ShellSort"

    def _do_sort(self):
        gap = len(self._data)

        while gap > 1:
            gap = int(math.ceil(gap / 2))
            for i in range(gap, len(self._data), gap):
                temp = self._data[i]
                j = i
                while j >= gap and self._data[j - gap].value > temp.value:
                    self._hilights = (j, j - gap)
                    self._inc_compares()
                    yield
                    self._inc_swaps()
                    self._data[j] = self._data[j - gap]
                    yield
                    j -= gap
                self._inc_swaps()
                self._data[j] = temp
                yield
        self.sorted = True
        # Draw the final sorted frame
        self._hilights = []

class InsertionSort(SortObject):
    name = "InsertionSort"

    def _do_sort(self):
        # An insertion sort is a shell sort with gap = 1
        gap = 2

        while gap > 1:
            gap = gap // 2
            for i in range(gap, len(self._data), gap):
                temp = self._data[i]
                j = i
                while j >= gap and self._data[j - gap].value > temp.value:
                    self._hilights = (j, j - gap)
                    self._inc_compares()
                    yield
                    self._data[j] = self._data[j - gap]
                    self._inc_swaps()
                    yield
                    j -= gap
                self._data[j] = temp
                self._inc_swaps()
                yield
        self.sorted = True
        # Draw the final sorted frame
        self._hilights = []

class QuickSort(SortObject):
    name = "QuickSort"

    def _do_sort(self):
        """
        Iterative version of quick sort
        """
        temp_stack = []
        temp_stack.append((0,len(self._data) - 1))
        
        #Main loop to pop and push items until stack is empty
        while temp_stack:      
            pos = temp_stack.pop()
            right, left = pos[1], pos[0]
            ### Inlined partition
            piv = self._data[left]
            i = left + 1
            j = right
            while True:
                while i <= j and self._data[i].value <= piv.value:
                    self._hilights = (i, piv.value)
                    self._inc_compares()
                    yield
                    i += 1
                while j >= i and self._data[j].value >= piv.value:
                    self._hilights = (j, piv.value)
                    self._inc_compares()
                    yield
                    j -= 1
                if j <= i:
                    break
                self._hilights = (j,i)
                yield
                self._swap_indices(j,i)
                yield
            self._hilights = (left, j)
            yield
            self._swap_indices(left, j)
            yield
            piv = j
            ### END Inline partition
            #If items in the left of the pivot push them to the stack
            if piv-1 > left:
                temp_stack.append((left,piv-1))
            #If items in the right of the pivot push them to the stack
            if piv+1 < right:
                temp_stack.append((piv+1,right))
        # Draw the final sorted frame
        self.sorted = True
        self._hilights = []
     

class SelectionSort(SortObject):
    name = "SelectionSort"

    def _do_sort(self):
        for j in range(len(self._data) - 1):
            iMin = j
            for i in range(j + 1, len(self._data)):
                self._hilights = (i,iMin)
                self._inc_compares()
                yield
                if self._data[i].value < self._data[iMin].value:
                    iMin = i
            if iMin != j:
                self._hilights = (j, iMin)
                self._inc_compares()
                yield
                self._swap_indices(j, iMin)
                yield
        # Draw the final sorted frame
        self.sorted = True
        self._hilights = []

data = [DataPoint(randint(2,100), "#%06X" % randint(0, (2**24) - 1)) for x in range(DATA_SIZE)]

sorter_types = [
    BubbleSort,
    OptimizedBubbleSort,
    ShellSort,
    InsertionSort,
    QuickSort,
    SelectionSort,
]

BOX_WIDTH = 600
BOX_HEIGHT = 100
Sorter = namedtuple('Sorter', ['name','sorter'])

WIDTH = BOX_WIDTH + 10
HEIGHT = ((BOX_HEIGHT + 5) * len(sorter_types)) + 5

sorters = None
draw_frame = True
def do_draw():
    global sorters
    global draw_frame
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

    screen.fill('darkgrey')
    for index, s in enumerate(sorters):
        screen.blit(s.sorter.get_frame(), (5, 5 + (index * (BOX_HEIGHT + 5))))
        if not s.sorter.sorted:
            try:
                s.sorter.sort.send(None)
            except StopIteration:
                pass
        

    draw_frame = False

time_accumlate = 1.0
def update(dt):
    global time_accumlate
    time_accumlate += dt
    if time_accumlate > 1.0/FPS:
        # draw_frame = True
        do_draw()
        time_accumlate = 0