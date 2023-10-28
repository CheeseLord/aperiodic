import itertools
import numpy as np
import random

from classify import isRepeating
from geometry import DIRECTIONS, orient


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

