import itertools
import more_itertools
import numpy as np
import sympy

import periodic


def randomTransformation(shapes):
    offset = -np.array(shapes)[
        np.random.randint(len(shapes)),
        np.random.randint(len(shapes[0])),
        0,
    ]
    other = translate(shapes, offset)

    # FIXME: Handle rotation.

    return other


def translate(shapes, offset):
    other = np.array(shapes)
    other[:, :, 0] += offset
    other = [
        [
            tuple(
                tuple(x) for x in widget
            ) for widget in shape
        ] for shape in other
    ]
    return other


def overlap(shapes, other):
    shapes = {tuple(shape) for shape in shapes}
    other = {tuple(shape) for shape in other}
    return [list(x) for x in shapes & other]


def isRepeating(shapes):
    # Find a basis for large repeats.
    possible = [
        offset for offset in itertools.product(range(-10, 11), repeat=3)
        if sum(offset) % 2 == 0 and offset > (0, 0, 0)
    ]
    possible = sorted(possible, key=np.linalg.norm)
    repeats = []
    for offset in possible:
        if len(overlap(shapes, translate(shapes, offset))) < len(shapes) // 3:
            continue
        mat = np.array(repeats + [offset])
        if len(sympy.Matrix(mat).T.rref()[1]) > len(repeats):
            repeats.append(offset)
            if len(repeats) == 3:
                break
    if len(repeats) < 3:
        return False, 0

    # Get the fundamental region.
    low = np.zeros(3, dtype=int)
    high = np.zeros(3, dtype=int)
    for subset in more_itertools.powerset(repeats):
        corner = np.sum(subset, axis=0)
        low = np.minimum(low, corner)
        high = np.maximum(high, corner)
    mat = np.array(repeats).T
    possible = [
        offset for offset in itertools.product(range(-10, 11), repeat=3)
        if sum(offset) % 2 == 0
    ]
    centers = []
    for center in possible:
        coeffs = np.linalg.solve(mat, center)
        if np.all((0 <= coeffs) & (coeffs < 1)):
            centers.append(center)

    # Find the tiles in the fundamental region
    fundamental = []
    for shape in shapes:
        for center, _direction in shape:
            if center in centers:
                fundamental.append(shape)
                break
    for offsets in more_itertools.powerset(repeats):
        if not offsets:
            continue
        result = fundamental
        for offset in offsets:
            result = translate(result, offset)
        fundamental = [
            shape for shape in fundamental
            if shape not in overlap(fundamental, result)
        ]

    return periodic.isRepeating(fundamental), len(fundamental)


if __name__ == '__main__':
    import os

    from geometry import orient


    PATH = 'gallery/20k'

    with open(f'{PATH}/unknown.txt') as f:
        unknown = [eval(l) for l in f.readlines()]

    for name in sorted(os.listdir(PATH)):
        with open(f'{PATH}/{name}') as f:
            shapes = [eval(l) for l in f.readlines()]

        repeating, period = isRepeating(shapes)
        if not repeating:
            continue

        print(name, period)
        index = int(name.split('.')[0][-3:])
        s = unknown[index - 1]

        with open(f'shapes/working/periodic-{period}', 'a') as f:
            f.write(f'{s}\n')

