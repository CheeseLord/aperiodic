from collections import Counter
import itertools
import numpy as np
import random

from geometry import DIRECTIONS, orient


PRIMES = [2, 3, 5, 7]


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

    if count in PRIMES:
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

    # FIXME: Handle composite counts.
    return False


def periodic2(shape):
    directions = {x[1] for x in shape}
    if len(directions) != 7:
        return False
    for d in DIRECTIONS:
        if 0 not in DIRECTIONS:
            continue
        for i in range(12):
            other = {x[1] for x in orient(shape, ((0, 0, 0), d), i)}
            if not other & directions:
                return True
    return False


def periodicSampling(shape, period):
    shape = np.array(shape)

    variants = []
    for rot in range(3):
        for axes in itertools.product([-1, 1], repeat=3):
            if np.prod(axes) == 1:
                variants.append(np.roll(shape, rot, axis=2) * axes)
            else:
                variants.append(np.roll(shape[:, :, ::-1], rot, axis=2) * axes)

    offsets = list(itertools.product(range(period), repeat=3))

    for _ in range(10000):
        shapes = []
        for _ in range(period):
            v = random.choice(variants).copy()
            a, b, c = random.choice(offsets)
            v += ((b + c, c + a, a + b), (0, 0, 0))
            shapes.append([(tuple(x[0]), tuple(x[1])) for x in v])
        if isRepeating(shapes):
            return True
    return False


if __name__ == '__main__':
    with open('shapes/unknown.txt') as f:
        shapes = [eval(l) for l in f.readlines()]
    for i, shape in enumerate(shapes):
        periodic = periodicSampling(shape, 4)
        print(i, periodic)
        if periodic:
            with open(f'shapes/working/periodic-4.txt', 'a') as f:
                f.write(f'{shape}\n')
        else:
            with open(f'shapes/working/unknown.txt', 'a') as f:
                f.write(f'{shape}\n')

