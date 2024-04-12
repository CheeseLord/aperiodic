import itertools
import numpy as np
import random

from geometry import getNeighbors


def generateRandomShape(n):
    shape = [
        ((0, 0, 0), (1, 0, 0)),
        ((0, 0, 0), (1, 1, 1)),
    ]

    while len(shape) < 7 * n:
        neighbors = set()
        for x in shape:
            neighbors = neighbors.union(getNeighbors(x))
        neighbors = neighbors.difference(shape)
        newShape = shape + [random.choice(list(neighbors))]

        octs = sum(0 in w[1] for w in newShape)
        tets = len(newShape) - octs
        if octs <= 3 * n and tets <= 4 * n:
            shape = newShape

    return makeCanonical(shape)


def generateAllShapes(n):
    shape = [
        ((0, 0, 0), (1, 0, 0)),
        ((0, 0, 0), (1, 1, 1)),
    ]
    shapes = _generateHelper(shape, 3 * n - 1, 4 * n - 1)
    shapes = [list(y) for y in {tuple(sorted(x)) for x in shapes}]
    shapes = [list(y) for y in {tuple(makeCanonical(x)) for x in shapes}]
    return shapes


def _generateHelper(shape, o, t):
    if o == t == 0:
        return [shape]

    neighbors = set()
    for x in shape:
        neighbors = neighbors.union(getNeighbors(x))
    neighbors = neighbors.difference(shape)

    shapes = []
    for other in neighbors:
        isOct = (0 in other[1])
        if isOct and o > 0:
            shapes += _generateHelper(shape + [other], o - 1, t)
        if not isOct and t > 0:
            shapes += _generateHelper(shape + [other], o, t - 1)

    return shapes


"""
def generateShapes(n):
    o = 3 * n
    t = 4 * n

    shapes = [[
        ((0, 0, 0), (1, 0, 0)),
        ((0, 0, 0), (1, 1, 1)),
    ]]
    for _ in range(7 * n - 2):
        newShapes = []

        for shape in shapes:
            neighbors = set()
            for w in shape:
                neighbors = neighbors.union(getNeighbors(w))
            neighbors = neighbors.difference(shape)
            for w in neighbors:
                newShapes += [shape + [w]]

        newShapes = [
            x for x in newShapes
            if sum(0 in w[1] for w in x) <= o
            and sum(0 not in w[1] for w in x) <= t
        ]
        newShapes = [
            list(y) for y in {tuple(sorted(x)) for x in newShapes}
        ]
        newShapes = [
            list(y) for y in {tuple(makeCanonical(x)) for x in newShapes}
        ]
        shapes = newShapes

    return shapes
"""


def makeCanonical(shape):
    best = None
    arr = np.array(shape)

    for sign in itertools.product([1, -1], repeat=3):
        for perm in itertools.permutations(range(3)):
            modified = arr[:, :, perm] * sign
            modified[:, 0] -= np.min(modified[:, 0], axis=0)
            newShape = sorted([(tuple(x[0]), tuple(x[1])) for x in modified])
            if best is None:
                best = newShape
            else:
                best = min(best, newShape)

    return best


if __name__ == '__main__':
    """
    shapes = generateShapes(2)
    with open('shapes/allShapes.txt', 'w') as f:
        f.writelines([f'{shape}\n' for shape in shapes])
    print(len(shapes))
    """

    with open('shapes/allShapes.txt') as f:
        shapes = {tuple(eval(l)) for l in f.readlines()}

    newShapes = []
    repeats = 0
    while len(newShapes) < 10 ** 3:
        shape = generateRandomShape(2)
        if tuple(shape) in shapes or shape in newShapes:
            print('Repeated shape')
            repeats += 1
            continue
        newShapes.append(shape)
    print(f'{repeats} repeats')

    with open('shapes/allShapes.txt', 'a') as f:
        for shape in newShapes:
            f.write(f'{shape}\n')

