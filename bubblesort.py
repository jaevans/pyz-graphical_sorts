from random import randint

WIDTH=500
HEIGHT=300


DATA_SIZE=50


class Sorter(object):
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
    def __init__(self, starting_data):
        super().__init__(starting_data)
        self.sort_pointer = 0

    def sort_step(self):
        self.sort_pointer = self.sort_pointer % (len(self.data) - 1)
        if self.data[self.sort_pointer][0] > self.data[self.sort_pointer + 1][0]:
            self.swap_indices(self.sort_pointer, self.sort_pointer + 1)
        self.sort_pointer += 1

class OptimizedBubbleSort(BubbleSort):
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

        if self.data[self.sort_pointer][0] > self.data[self.sort_pointer + 1][0]:
            self.swap_indices(self.sort_pointer, self.sort_pointer + 1)
        self.sort_pointer += 1

data = [(randint(2,100), "#%06X" % randint(0, (2**24) - 1)) for x in range(DATA_SIZE)]
print(data)
sorter_types = [
    BubbleSort,
    OptimizedBubbleSort,
]
sorters = [s(data) for s in sorter_types]
surfaces = [Surface((200,100)) for s in sorter_types]

def draw():
    screen.fill('lightblue')
    box_width = WIDTH/DATA_SIZE
    box_height = HEIGHT/len(sorters)

    for boxnum, sorter in enumerate(sorters):
        baseline = HEIGHT - (boxnum * box_height)
        for index, item in enumerate(sorter.data):
            r = Rect(index * box_width, baseline - item[0], box_width, item[0])
            screen.draw.filled_rect(r, item[1])
            screen.draw.rect(r,'black')

def update():
    for sorter in sorters:
        if not sorter.is_sorted:
            sorter.sort_step()

#def update():
    #global sort_pointer
    #if sort_pointer < DATA_SIZE - 1:
    #    if data[sort_pointer] > data[sort_pointer + 1]:
    #        temp = data[sort_pointer]
    #        data[sort_pointer] = data[sort_pointer + 1]
    #        data[sort_pointer + 1] = temp
    # sort_pointer = (sort_pointer + 1) % DATA_SIZE
