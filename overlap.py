from heapq import nlargest
import itertools
import more_itertools
import numpy as np
import sympy

from geometry import translate
from periodic import isRepeatingOffsets


def overlap(shapes, other):
    shapes = {tuple(shape) for shape in shapes}
    other = {tuple(shape) for shape in other}
    return [list(x) for x in shapes & other]


def getBases(shapes):
    # Find the offets with the largest overlap.
    possible = [
        offset for offset in itertools.product(range(-5, 6), repeat=3)
        if sum(offset) % 2 == 0 and offset > (0, 0, 0)
    ]
    best = nlargest(
        8, possible,
        key=lambda offset: len(overlap(shapes, translate(shapes, offset)))
    )

    # Find all linearly independent subsets.
    bases = []
    for offsets in itertools.combinations(best, 3):
        if len(sympy.Matrix(np.array(offsets)).rref()[1]) == 3:
            bases.append(offsets)

    return bases


def getFundamental(shapes, basis):
    # Find the lattice points in the fundamental domain.
    for subset in more_itertools.powerset(basis):
        corner = np.sum(subset, axis=0)
    mat = np.array(basis).T
    possible = [
        offset for offset in itertools.product(range(-10, 11), repeat=3)
        if sum(offset) % 2 == 0
    ]
    centers = []
    for center in possible:
        coeffs = np.linalg.solve(mat, center)
        if np.all((0 <= coeffs) & (coeffs < 1)):
            centers.append(center)

    # Find the tiles overlapping the fundamental domain.
    fundamental = []
    for shape in shapes:
        for center, _direction in shape:
            if center in centers:
                fundamental.append(shape)
                break

    # Remove duplicates offset by the lattice.
    for offsets in more_itertools.powerset(basis):
        if not offsets:
            continue
        for coeffs in itertools.product(range(-5, 6), repeat=len(offsets)):
            if not any(coeffs):
                continue
            result = fundamental
            for offset, coeff in zip(offsets, coeffs):
                result = translate(result, [x * coeff for x in offset])
            fundamental = [
                shape for shape in fundamental
                if shape not in overlap(fundamental, result)
            ]

    return fundamental


def isRepeating(shapes):
    for basis in getBases(shapes):
        fundamental = getFundamental(shapes, basis)
        if isRepeatingOffsets(fundamental, basis):
            return True, len(fundamental)

    return False, 0


if __name__ == '__main__':
    import os


    PATH = 'shapes/temp'

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

