import functools
import itertools
import numpy as np


# Directions around a vertex.
DIRECTIONS = [
    (x, y, z) for x, y, z in itertools.product([1, 0, -1], repeat=3)
    if (x + y + z) % 2 == 1
]

# Adjacent directions at the same vertex.
_adjacentSameCenter = {
    direction: [] for direction in DIRECTIONS
}
for direction in DIRECTIONS:
    if 0 in direction:
        continue
    for otherDir in DIRECTIONS:
        if sorted(np.abs(np.array(direction) - otherDir)) == [0, 1, 1]:
            _adjacentSameCenter[direction].append(otherDir)
            _adjacentSameCenter[otherDir].append(direction)

# Adjacent directions around neighboring centers.
_adjacentOtherCenter = {
    direction: [] for direction in DIRECTIONS
}
for direction in DIRECTIONS:
    if 0 in direction:
        for i in range(3):
            if direction[i] != 0:
                continue
            for j in [-1, 1]:
                v = np.zeros(3, dtype=int)
                v[i] = j
                _adjacentOtherCenter[direction].append(
                    (tuple(direction - v), tuple(v))
                )
    else:
        for i in range(3):
            v = np.ones(3, dtype=int) * -1
            v[i] = 1
            v *= direction
            _adjacentOtherCenter[direction].append(
                (tuple((direction - v) // 2), tuple(v))
            )


@functools.total_ordering
class Widget:
    def __init__(self, center, direction):
        self.center = tuple(center)
        self.direction = tuple(direction)

    def __eq__(self, other):
        return self.center == other.center and self.direction == other.direction

    def __lt__(self, other):
        return tuple(self) < tuple(other)

    def __iter__(self):
        yield self.center
        yield self.direction

    def __hash__(self):
        return hash(tuple(self))

    def __repr__(self):
        return repr(tuple(self))

    @property
    def isOct(self):
        return 0 in self.direction

    @property
    def isTet(self):
        return 0 not in self.direction

    @property
    def neighbors(self):
        neighbors = [
            Widget(self.center, otherDir)
            for otherDir in _adjacentSameCenter[self.direction]
        ]
        neighbors += [
            Widget(tuple(np.array(self.center) + otherCenter), otherDir)
            for otherCenter, otherDir in _adjacentOtherCenter[self.direction]
        ]
        return neighbors

    def translate(self, offset):
        return Widget(tuple(np.array(self.center) + offset), self.direction)


def getFirstWidgets(n):
    widgets = []
    used = set()
    toExpand = [Widget((0, 0, 0), (1, 0, 0))]
    while len(widgets) < n:
        w = toExpand[0]
        toExpand = toExpand[1:]
        if w in used:
            continue
        widgets.append(w)
        used.add(w)
        toExpand.extend([x for x in w.neighbors if x not in used])

    return widgets

