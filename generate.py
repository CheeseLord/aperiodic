import itertools
import numpy as np

from geometry import getNeighbors


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
    shapes = generateAllShapes(1)
    with open('shapes/allShapes.txt', 'w') as f:
        f.writelines([f'{shape}\n' for shape in shapes])
    print(len(shapes))

