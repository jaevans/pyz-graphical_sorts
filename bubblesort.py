from random import randint

WIDTH=500
HEIGHT=200


DATA_SIZE=50

sort_pointer = 0

class Sorter(object):
    def __init__(self, starting_data):
        self.data = starting_data[:]
        self._sorted = False

    @property
    def is_sorted(self):
        return self._sorted

    def sort_step(self):
        raise(NotImplementedError)

class ShellSort(object):
    def __init__(self, starting_data):
        super().__init__(self,starting_data)
        self.sort_pointer = 0

    def _swap(x,y):
        return y,x

    def swap_indices(x,y):
        self.data[y],self.data[x] = swap(self.data[x], self.data[y])

    def sort_step(self):
        sort_pointer = sort_pointer % (len(self.data) - 1)
        self._sorted = True
        if data[sort_pointer] > data[sort_pointer + 1]:
            self.swap_indices(sort_pointer, sort_pointer + 1)
            self._sorted = False
        sort_pointer += 1

        yield self.data()


data = [randint(0,100) for x in range(DATA_SIZE)]
sorter_types = [
    ShellSort,
]
sorters = [s(data) for s in sorter_types]


def draw():
    screen.fill('lightblue')
    box_width = WIDTH/DATA_SIZE

    for index,item in enumerate(data):
        r = Rect(index * box_width, HEIGHT - item, box_width, item)
        screen.draw.filled_rect(r,'red')
        screen.draw.rect(r,'black')

def update():
    global sort_pointer
    if sort_pointer < DATA_SIZE - 1:
        if data[sort_pointer] > data[sort_pointer + 1]:
            temp = data[sort_pointer]
            data[sort_pointer] = data[sort_pointer + 1]
            data[sort_pointer + 1] = temp
    sort_pointer = (sort_pointer + 1) % DATA_SIZE
