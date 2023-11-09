from collections import Counter
import itertools
import numpy as np
import random

from geometry import DIRECTIONS, orient


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

    if count > 2 and count % 2 == 0:
        for a, b, c in itertools.product(range(count), repeat=3):
            a = np.array([a // 2, a % 2], dtype=int)
            b = np.array([b // 2, b % 2], dtype=int)
            c = np.array([c // 2, c % 2], dtype=int)

            for x, y, z in vectors:
                color = (
                    a * (y + z - x)
                    + b * (z + x - y)
                    + c * (x + y - z)
                ) // 2
                if not np.any(color % (count // 2, 2)):
                    break
            else:
                return True

    if count == 8:
        for a, b, c in itertools.product(range(count), repeat=3):
            a = np.array([a // 4, (a // 2) % 2, a % 2], dtype=int)
            b = np.array([b // 4, (b // 2) % 2, b % 2], dtype=int)
            c = np.array([c // 4, (c // 2) % 2, c % 2], dtype=int)

            for x, y, z in vectors:
                color = (
                    a * (y + z - x)
                    + b * (z + x - y)
                    + c * (x + y - z)
                ) // 2
                if not np.any(color % (2, 2, 2)):
                    break
            else:
                return True


    if count == 9:
        for a, b, c in itertools.product(range(count), repeat=3):
            a = np.array([a // 3, a % 3], dtype=int)
            b = np.array([b // 3, b % 3], dtype=int)
            c = np.array([c // 3, c % 3], dtype=int)

            for x, y, z in vectors:
                color = (
                    a * (y + z - x)
                    + b * (z + x - y)
                    + c * (x + y - z)
                ) // 2
                if not np.any(color % (3, 3)):
                    break
            else:
                return True

    # FIXME: There are other lattices for composite counts.

    return False


def isAlmostRepeating(shapes):
    if len(shapes) % 2 != 1:
        return False

    shapes = list(shapes)
    merged = []
    for shape in shapes:
        merged += shape

    # Find which directions are missing.
    repeats = (len(shapes) + 1) // 2
    c = Counter([x[1] for x in merged])
    missing = {d: repeats - c[d] for d in DIRECTIONS}
    if any(missing[d] < 0 for d in DIRECTIONS):
        return False

    # Find all variants of the shape.
    shape = np.array(shapes[0])
    variants = []
    for rot in range(3):
        for axes in itertools.product([-1, 1], repeat=3):
            if np.prod(axes) == 1:
                variants.append(np.roll(shape, rot, axis=2) * axes)
            else:
                variants.append(np.roll(shape[:, :, ::-1], rot, axis=2) * axes)

    # Get the variants with the right directions.
    good = []
    for v in variants:
        counts = Counter(tuple(d) for d in v[:, 1])
        if all(missing[d] == counts[d] for d in DIRECTIONS):
            good.append(v)

    # Place each variant in every possible position.
    for v in good:
        for a, b, c in itertools.product(range(repeats), repeat=3):
            newShape = v + ((b + c, c + a, a + b), (0, 0, 0))
            newShapes = shapes + [[(tuple(x[0]), tuple(x[1])) for x in newShape]]
            if isRepeating(newShapes):
                return True

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
    if period % 2 != 0:
        return False

    shape = np.array(shape)

    variants = []
    for rot in range(3):
        for axes in itertools.product([-1, 1], repeat=3):
            if np.prod(axes) == 1:
                variants.append(np.roll(shape, rot, axis=2) * axes)
            else:
                variants.append(np.roll(shape[:, :, ::-1], rot, axis=2) * axes)

    offsets = list(itertools.product(range(period // 2), repeat=3))

    for _ in range(10 ** 5):
        shapes = []
        for _ in range(period - 1):
            v = random.choice(variants).copy()
            a, b, c = random.choice(offsets)
            v += ((b + c, c + a, a + b), (0, 0, 0))
            shapes.append([(tuple(x[0]), tuple(x[1])) for x in v])
        if isAlmostRepeating(shapes):
            return True
    return False


if __name__ == '__main__':
    with open('shapes/unknown.txt') as f:
        shapes = [eval(l) for l in f.readlines()]
    for i, shape in enumerate(shapes):
        periodic = periodicSampling(shape, 6)
        print(i, periodic)
        if periodic:
            with open(f'shapes/working/periodic-6.txt', 'a') as f:
                f.write(f'{shape}\n')
        else:
            with open(f'shapes/working/unknown.txt', 'a') as f:
                f.write(f'{shape}\n')

