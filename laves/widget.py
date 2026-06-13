import functools
import itertools
import numpy as np


COLORS = [
    (0, 0, 0),  # R
    (1, 0, 1),  # Y
    (0, 1, 1),  # G
    (1, 1, 0),  # B
]

ADJACENT = np.array([
    [-1, 0, 1],
    [0, 1, -1],
    [1, -1, 0],
])


@functools.total_ordering
class Widget:
    def __init__(self, *center):
        if len(center) == 1:
            self.center = tuple(center[0])
        else:
            self.center = tuple(center)

        self.center = tuple(int(x) for x in self.center)

    def __eq__(self, other):
        return self.center == other.center

    def __lt__(self, other):
        return self.center < other.center

    def __iter__(self):
        yield self.center

    def __hash__(self):
        return hash(self.center)

    def __repr__(self):
        return repr(self.center)

    def __str__(self):
        return str(self.center) + ':' + 'RYGB'[self.colorIndex]

    def __array__(self):
        return np.array(self.center)

    @property
    def colorIndex(self):
        return COLORS.index(tuple(np.array(self.center) % 2))

    @property
    def neighbors(self):
        m = np.array([
            [1, 0, 0],
            [0, 0, -1],
            [0, 1, 0],
        ])
        arr = np.linalg.matrix_power(m, self.colorIndex)
        edges = np.dot(arr, ADJACENT.T).T
        return [Widget(self.center + e) for e in edges]

    def translate(self, offset):
        return Widget(tuple(np.array(self.center) + offset))


def getFirstWidgets(n):
    widgets = []
    used = set()
    toExpand = [Widget((0, 0, 0))]
    while len(widgets) < n:
        w = toExpand[0]
        toExpand = toExpand[1:]
        if w in used:
            continue
        widgets.append(w)
        used.add(w)
        toExpand.extend([x for x in w.neighbors if x not in used])

    return widgets

