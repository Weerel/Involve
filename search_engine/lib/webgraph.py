class WebGraph:
    def __init__(self, dimensions, vector = None):
        self._dimensions = dimensions
        if vector:
            self._vector = [i for i in vector]
        else:
            self._vector = [0 for i in dimensions]

    def dimensions(self):
        return self._dimensions

    def current(self):
        return tuple(self._vector)  

    def next(self, index):
        return WebGraph(self._dimensions, self._neighbor(index, 1))

    def prev(self, index):
        return WebGraph(self._dimensions, self._neighbor(index, -1))

    def get_neighbors(self):
        for i in range(len(self._vector)):
            if self._dimensions[i] > 1:
                yield self.next(i)
            if self._dimensions[i] > 2:
                yield self.prev(i)

    def _neighbor(self, index, direction):
        for i, x in enumerate(self._vector):
            if i == index:
                yield (x + direction) % self._dimensions[i]
            else:
                yield x

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
            and self.current() == other.current())

    def __ne__(self, other):
        return not self.__eq__(other)
