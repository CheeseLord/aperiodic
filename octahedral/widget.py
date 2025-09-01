import functools
import itertools
import numpy as np


# Directions around a vertex.
DIRECTIONS = sorted({
    (a * x, b * y, c * z)
    for (a, b, c) in itertools.product([-1, 1], repeat=3)
    for (x, y, z) in itertools.permutations([0, 1, 2])
})

# Adjacent directions at the same vertex.
_adjacentSameCenter = {
    direction: [] for direction in DIRECTIONS
}
for direction, otherDir in itertools.combinations(DIRECTIONS, 2):
    if sorted(np.abs(np.array(direction) - otherDir)) == [0, 1, 1]:
        _adjacentSameCenter[direction].append(otherDir)
        _adjacentSameCenter[otherDir].append(direction)

# Adjacent directions around neighboring centers.
_adjacentOtherCenter = {
    direction: [] for direction in DIRECTIONS
}
for direction in DIRECTIONS:
    otherCenters = []
    otherCenters += list(itertools.product([-2, 2], repeat=3))
    otherCenters += list(set(itertools.permutations([0, 0, 4])))
    otherCenters += list(set(itertools.permutations([0, 0, -4])))
    for otherCenter in otherCenters:
        otherDir = tuple(-(np.array(otherCenter) - direction))
        if otherDir in DIRECTIONS:
            _adjacentOtherCenter[direction].append((otherCenter, otherDir))


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

    def __array__(self):
        return np.array(tuple(self))

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
    toExpand = [Widget((0, 0, 0), (0, 1, 2))]
    while len(widgets) < n:
        w = toExpand[0]
        toExpand = toExpand[1:]
        if w in used:
            continue
        widgets.append(w)
        used.add(w)
        toExpand.extend([x for x in w.neighbors if x not in used])

    return widgets

