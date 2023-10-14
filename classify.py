from collections import Counter
from enum import Enum
import itertools
import numpy as np

from geometry import orient


# TODO: Find a better way to generate these.
CENTERS = [
    c for c in itertools.product(range(-10, 11), repeat=3)
    if sum(c) % 2 == 0
]
CENTERS.sort(key=np.linalg.norm)

WIDGETS = list(itertools.product(CENTERS, DIRECTIONS))


class Behavior(Enum):
    PERIODIC = 0
    INVALID = 1
    UNKNOWN = 2


def classify(shape):
    shapes = []
    positions = []  # [(widget index, orientation)]
    used = set()
    # FIXME: Write this.


def isRepeating(shapes):
    if len(shapes) % 2 != 0:
        return False

    merged = []
    for shape in shapes:
        merged += shape

    # Check if there are the same number of each widget.
    c = Counter([x[1] for x in merged])
    if len(c) != 14 or len(set(c.values())) != 1:
        return False

    count = c[(1, 1, 1)]
    if count == 1:
        return True

    if count == 2 or count == 3:
        vectors = set()
        for (c1, d1), (c2, d2) in itertools.combinations(merged, 2):
            if d1 == d2:
                vectors.add(tuple(np.array(c2) - np.array(c1)))

        # Check if each possible lattice partitions the widgets correctly.
        for a, b, c in itertools.product(range(count), repeat=3):
            for x, y, z in vectors:
                color = (
                    a * (y + z - x)
                    + b * (z + x - y)
                    + c * (x + y - z)
                ) // 2
                if color % count == 0:
                    break
            else:
                return True

    # FIXME: Handle larger counts.
    return False



if __name__ == '__main__':
    with open('allShapes.txt') as f:
        lines = f.readlines()
    shapes = [eval(l) for l in lines]
