import itertools
import more_itertools
import numpy as np
import sympy

from geometry import translate
import periodic


def overlap(shapes, other):
    shapes = {tuple(shape) for shape in shapes}
    other = {tuple(shape) for shape in other}
    return [list(x) for x in shapes & other]


def findBasis(shapes):
    possible = [
        offset for offset in itertools.product(range(-10, 11), repeat=3)
        if sum(offset) % 2 == 0 and offset > (0, 0, 0)
    ]
    possible = sorted(possible, key=np.linalg.norm)
    repeats = []
    for offset in possible:
        mat = np.array(repeats + [offset])
        if len(sympy.Matrix(mat).T.rref()[1]) <= len(repeats):
            continue
        if len(overlap(shapes, translate(shapes, offset))) >= len(shapes) / 4:
            repeats.append(offset)
        if len(repeats) == 3:
            break
    return repeats


def isRepeating(shapes):
    repeats = findBasis(shapes)
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
        for coeffs in itertools.product(range(-10, 11), repeat=len(offsets)):
            if not any(coeffs):
                continue
            result = fundamental
            for offset, coeff in zip(offsets, coeffs):
                result = translate(result, [x * coeff for x in offset])
            fundamental = [
                shape for shape in fundamental
                if shape not in overlap(fundamental, result)
            ]

    print(repeats)
    print(len(fundamental), abs(round(np.linalg.det(repeats))))

    return periodic.isRepeatingOffsets(fundamental, repeats), len(fundamental)


if __name__ == '__main__':
    import os


    PATH = 'gallery/200'

    with open(f'{PATH}/unknown.txt') as f:
        unknown = [eval(l) for l in f.readlines()]

    for name in sorted(os.listdir(PATH)):
        if name == 'unknown.txt':
            continue
        print(name)

        with open(f'{PATH}/{name}') as f:
            shapes = [eval(l) for l in f.readlines()]

        repeating, period = isRepeating(shapes)
        if not repeating:
            continue

        print(f'* {name} {period} *')
        index = int(name.split('.')[0][-3:])
        s = unknown[index - 1]

        with open(f'shapes/working/periodic-{period}.txt', 'a') as f:
            f.write(f'{s}\n')

