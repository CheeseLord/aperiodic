import itertools
import numpy as np
import random

from numberTheory import indexToColor, partitions
from periodic import isAlmostRepeating


def buildRandomTiling(shape, period):
    if period % 2 != 0:
        return None
    shape = np.array(shape)
    count = period // 2

    # Create all possible colorings.
    mods = []
    colorings = []
    for parts in partitions(count):
        for seeds in itertools.product(range(count), repeat=3):
            mods.append(parts)
            colorings.append(
                tuple(indexToColor(x, parts) for x in seeds)
            )

    # Create all possible tiles.
    variants = []
    for rot in range(3):
        for axes in itertools.product([-1, 1], repeat=3):
            if np.prod(axes) == 1:
                variants.append(np.roll(shape, rot, axis=2) * axes)
            else:
                variants.append(np.roll(shape[:, :, ::-1], rot, axis=2) * axes)
    offsets = [
        (b + c, c + a, a + b)
        for a, b, c in itertools.product(range(count), repeat=3)
    ]
    tiles = []
    for variant in variants:
        for offset in offsets:
            newShape = variant + (offset, (0, 0, 0))
            tiles.append([(tuple(x[0]), tuple(x[1])) for x in newShape])
    random.shuffle(tiles)

    # Add as many tiles as possible.
    shapes = []
    used = [set() for _ in colorings]
    for tile in tiles[:2000]:
        valid = False
        newUsed = []

        for mod, coloring, u in zip(mods, colorings, used):
            if u is None:
                newUsed.append(None)
                continue
            u = u.copy()

            for (x, y, z), direction in tile:
                color = tuple((
                    (y + z - x) // 2 * coloring[0]
                    + (z + x - y) // 2 * coloring[1]
                    + (x + y - z) // 2 * coloring[2]
                ) % mod)
                if (direction, color) in u:
                    newUsed.append(None)
                    break
                else:
                    u.add((direction, color))
            else:
                newUsed.append(u)
                valid = True

        if valid:
            shapes.append(tile)
            used = newUsed
        if len(shapes) == period - 1:
            break

    if isAlmostRepeating(shapes):
        return shapes
    return []


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    from display import drawShapes
    from periodic import isRepeating


    period = 8

    with open('shapes/unknown.txt') as f:
        shapes = [eval(l) for l in f.readlines()]

    count = 0
    for i, shape in enumerate(shapes, start=1):
        for _ in range(100):
            tiling = buildRandomTiling(shape, period)
            if tiling:
                print(f'* {i} *')
                count += 1
                with open(f'shapes/working/periodic-{period}.txt', 'a') as f:
                    f.write(f'{shape}\n')
                break
        if i % 50 == 0 or i == len(shapes):
            print(i, count)

