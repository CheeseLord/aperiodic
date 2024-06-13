import itertools
import numpy as np
import random

from widget import Widget
from shape import Shape


def generateRandomShape(n):
    shape = Shape([
        ((0, 0, 0), (1, 0, 0)),
        ((0, 0, 0), (1, 1, 1)),
    ])

    while len(shape) < 7 * n:
        neighbors = set()
        for w in shape:
            neighbors = neighbors.union(w.neighbors)
        neighbors = neighbors.difference(shape.widgets)
        newShape = shape + [random.choice(list(neighbors))]

        octs = sum(w.isOct for w in newShape)
        tets = len(newShape.widgets) - octs
        if octs <= 3 * n and tets <= 4 * n:
            shape = newShape

    return makeCanonical(shape)



def generateAllShapes(n):
    shape = Shape([
        ((0, 0, 0), (1, 0, 0)),
        ((0, 0, 0), (1, 1, 1)),
    ])
    shapes = _generateHelper(shape, 3 * n - 1, 4 * n - 1)
    shapes = [
        Shape(t) for t in {tuple(sorted(s.widgets, key=tuple)) for s in shapes}
    ]
    shapes = [
        Shape(t) for t in {tuple(makeCanonical(s)) for s in shapes}
    ]
    return shapes


def _generateHelper(shape, o, t):
    if o == t == 0:
        return [shape]

    neighbors = set()
    for w in shape:
        neighbors = neighbors.union(w.neighbors)
    neighbors = neighbors.difference(shape.widgets)

    shapes = []
    for other in neighbors:
        if other.isOct and o > 0:
            shapes += _generateHelper(shape + [other], o - 1, t)
        if other.isTet and t > 0:
            shapes += _generateHelper(shape + [other], o, t - 1)

    return shapes


def makeCanonical(shape):
    best = None
    arr = np.array(shape)

    for sign in itertools.product([1, -1], repeat=3):
        for perm in itertools.permutations(range(3)):
            modified = arr[:, :, perm] * sign
            modified[:, 0] -= np.min(modified[:, 0], axis=0)
            newShape = Shape(sorted([Widget(*w) for w in modified], key=tuple))
            if best is None:
                best = newShape
            else:
                best = min(best, newShape, key=list)

    return best


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('numShapes')
    args = parser.parse_args()


    with open('shapes/allShapes.txt') as f:
        shapes = {Shape(eval(l)) for l in f.readlines()}

    newShapes = []
    repeats = 0
    while len(newShapes) < int(args.numShapes):
        shape = generateRandomShape(2)
        if shape in shapes or shape in newShapes:
            print('Repeated shape')
            repeats += 1
            continue
        newShapes.append(shape)
    print(f'{repeats} repeats')

    with open('shapes/allShapes.txt', 'a') as f:
        for shape in newShapes:
            f.write(f'{shape}\n')

