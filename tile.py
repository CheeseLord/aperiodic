import itertools
import numpy as np

from generate import DIRECTIONS, generateShape


CENTERS = [
    c for c in itertools.product(range(-5, 6), repeat=3)
    if sum(c) % 2 == 0
]
CENTERS.sort(key=np.linalg.norm)

WIDGETS = list(itertools.product(CENTERS, DIRECTIONS))


def findTiling(shape, n):
    tiles = [shape]
    while len(tiles) < n:
        # FIXME: Write this.
        break
    else:
        return tiles
    return None


if __name__ == '__main__':
    n = 2
    shape = generateShape()
    #print(findTiling(shape, n))

