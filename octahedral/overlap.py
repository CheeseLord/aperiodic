import matplotlib.pyplot as plt
import numpy as np
import random

from display import getAxis, drawShapes
from satisfy import cover
from shape import load


def overlap(tiling, offset):
    other = {s.translate(offset) for s in tiling}
    return len(set(tiling) & other)


def expected(numTiles, offset):
    volume = numTiles / 12
    r = (3/4 * volume / np.pi)**(1/3)
    d = np.linalg.norm(offset)
    overlapVolume = np.pi/12 * (4 * r + d) * (2 * r - d)**2
    return 12 * overlapVolume


if __name__ == '__main__':
    shapes = load('shapes/unknown.txt')
    shape = random.choice(shapes)
    print(f'Shape {shapes.index(shape) + 1}')

    numTiles = 50000
    tiling = cover(shape, numTiles)
    centers = set()
    for s in tiling:
        centers |= {w.center for w in s}

    for offset in sorted(centers, key=np.linalg.norm)[:50]:
        if offset == (0, 0, 0):
            continue

        o = overlap(tiling, offset)
        e = expected(numTiles, offset)
        if o > 0.5 * e:
            print(offset, o, e)
        elif o > numTiles / 100:
            print(f'* {offset} {o} {o / e}')


