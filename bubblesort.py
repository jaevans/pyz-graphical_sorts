from random import randint
from collections import namedtuple
import pygame



DATA_SIZE=50

DataPoint = namedtuple('DataPoint',['value','color'])

class Sorter(object):
    name = "Unknown"
    def __init__(self, starting_data):
        self.data = starting_data[:]
        self._sorted = False

    @staticmethod
    def _swap(x,y):
        return y,x

    def swap_indices(self, x, y):
        v1, v2 = self._swap(self.data[x], self.data[y])
        self.data[x], self.data[y] = v1, v2

    @property
    def is_sorted(self):
        return self._sorted

    def sort_step(self):
        raise(NotImplementedError)

class BubbleSort(Sorter):
    name = "BubbleSort"
    def __init__(self, starting_data):
        super().__init__(starting_data)
        self.sort_pointer = 0

    def sort_step(self):
        self.sort_pointer = self.sort_pointer % (len(self.data) - 1)
        if self.data[self.sort_pointer].value > self.data[self.sort_pointer + 1].value:
            self.swap_indices(self.sort_pointer, self.sort_pointer + 1)
        self.sort_pointer += 1

class OptimizedBubbleSort(BubbleSort):
    name = "OptimizedBubbleSort"
    def __init__(self, starting_data):
        super().__init__(starting_data)
        self.end = len(self.data)

    def sort_step(self):
        if self.is_sorted:
            return
        if self.sort_pointer == self.end - 1:
            self.end -= 1
            if self.end <= 1:
                self._sorted = True
            self.sort_pointer = 0

        if self.data[self.sort_pointer].value > self.data[self.sort_pointer + 1].value:
            self.swap_indices(self.sort_pointer, self.sort_pointer + 1)
        self.sort_pointer += 1

class InsertionSort(Sorter):
    name = "InsertionSort"
    def __init__(self, starting_data):
        super().__init__(starting_data)
        self.last_sorted = 1

    def sort_step(self):
        if self.is_sorted:
            return
        if self.last_sorted == len(self.data) - 1:
            self._sorted = True

        x = self.data[self.last_sorted]
        j = self.last_sorted - 1
        while j >= 0 and self.data[j].value > x.value:
            self.data[j + 1] = self.data[j]
            j -= 1
        self.data[j + 1] = x
        self.last_sorted += 1

class ShellSort(Sorter):
    name = "ShellSort"
    def __init__(self, starting_data):
        super().__init__(starting_data)
        self.last_sorted = 1
        self.gap_pointer = 701

    def sort_step(self):
        if self.is_sorted:
            return
        if self.last_sorted == len(self.data) - 1:
            self._sorted = True

        x = self.data[self.last_sorted]
        j = self.last_sorted - 1
        while j >= 0 and self.data[j].value > x.value:
            self.data[j + 1] = self.data[j]
            j -= 1
        self.data[j + 1] = x
        self.last_sorted += 1


# # Sort an array a[0...n-1].
# gaps = [701, 301, 132, 57, 23, 10, 4, 1]
#
# # Start with the largest gap and work down to a gap of 1
# foreach (gap in gaps)
# {
#     # Do a gapped insertion sort for this gap size.
#     # The first gap elements a[0..gap-1] are already in gapped order
#     # keep adding one more element until the entire array is gap sorted
#     for (i = gap; i < n; i += 1)
#     {
#         # add a[i] to the elements that have been gap sorted
#         # save a[i] in temp and make a hole at position i
#         temp = a[i]
#         # shift earlier gap-sorted elements up until the correct location for a[i] is found
#         for (j = i; j >= gap and a[j - gap] > temp; j -= gap)
#         {
#             a[j] = a[j - gap]
#         }
#         # put temp (the original a[i]) in its correct location
#         a[j] = temp
#     }
# }


data = [DataPoint(randint(2,100), "#%06X" % randint(0, (2**24) - 1)) for x in range(DATA_SIZE)]

sorter_types = [
    BubbleSort,
    OptimizedBubbleSort,
    InsertionSort,
    ShellSort,
]

#
# sorters = [s(data) for s in sorter_types]
# surfaces = [Surface((200,100)) for s in sorter_types]

BOX_WIDTH = 400
BOX_HEIGHT = 100
Sorter = namedtuple('Sorter',['sort','surface'])

sorters = [Sorter(s(data), pygame.Surface((BOX_WIDTH, BOX_HEIGHT))) for s in sorter_types]

WIDTH = BOX_WIDTH + 10
HEIGHT= (BOX_HEIGHT + 10) * len(sorters)
def draw():
    # font = pygame.font.Font(None, 18)
    screen.fill('black')
    for index, s in enumerate(sorters):
        screen.blit(s.surface, (5, 5 + (index * (BOX_HEIGHT + 5 ))))
        screen.draw.text(s.sort.name, (10, (index * BOX_HEIGHT) + 15), color='black', owidth=1, ocolor = 'white')
        # text = font.render("Pummel The Chimp, And Win $$$", 1, (10, 10, 10))
        # textpos = text.get_rect(centerx=background.get_width()/2)
        # background.blit(text, textpos)


    # screen.fill('lightblue')
    # box_width = WIDTH/DATA_SIZE
    # box_height = HEIGHT/len(sorters)
    #
    # for boxnum, sorter in enumerate(sorters):
    #     baseline = HEIGHT - (boxnum * box_height)
    #     for index, item in enumerate(sorter.data):
    #         r = Rect(index * box_width, baseline - item.value, box_width, item.value)
    #         screen.draw.filled_rect(r, item.color)
    #         screen.draw.rect(r,'black')

def update():
    bar_width = BOX_WIDTH / DATA_SIZE
    for sorter in sorters:
        if not sorter.sort.is_sorted:
            sorter.sort.sort_step()
            sorter.surface.fill(pygame.Color('lightblue'))
            for index, item in enumerate(sorter.sort.data):
                r = Rect(index * bar_width, BOX_HEIGHT - item.value, bar_width, item.value )
                pygame.draw.rect(sorter.surface, pygame.Color(item.color), r, 0)
                pygame.draw.rect(sorter.surface, pygame.Color('black'), r, 1)

#def update():
    #global sort_pointer
    #if sort_pointer < DATA_SIZE - 1:
    #    if data[sort_pointer] > data[sort_pointer + 1]:
    #        temp = data[sort_pointer]
    #        data[sort_pointer] = data[sort_pointer + 1]
    #        data[sort_pointer + 1] = temp
    # sort_pointer = (sort_pointer + 1) % DATA_SIZE
