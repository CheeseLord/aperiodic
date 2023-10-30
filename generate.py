import itertools
import numpy as np

from geometry import getNeighbors


def generateShape():
    shape = [
        ((0, 0, 0), (1, 0, 0)),
        ((0, 0, 0), (1, 1, 1)),
    ]
    neighbors = [getNeighbors(x) for x in shape]
    neighbors = neighbors[0] + neighbors[1]

    o = 2
    t = 3
    while o or t:
        i = np.random.randint(len(neighbors))
        n = neighbors[i]
        del neighbors[i]

        inOct = 0 in n[1]

        if n in shape:
            continue
        if inOct and o == 0:
            continue
        if not inOct and t == 0:
            continue

        if inOct:
            o -= 1
        else:
            t -= 1
        shape.append(n)
        neighbors.extend(getNeighbors(n))

    return shape


def generateAllShapes():
    shape = [
        ((0, 0, 0), (1, 0, 0)),
        ((0, 0, 0), (1, 1, 1)),
    ]
    shapes = _generateHelper(shape, 2, 3)
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
    best = sorted(shape)
    arr = np.array(shape)

    for sign in itertools.product([1, -1], repeat=3):
        for perm in itertools.permutations(range(3)):
            modified = arr[:, :, perm] * sign
            newShape = sorted([(tuple(x[0]), tuple(x[1])) for x in modified])
            best = min(best, newShape)

    # TODO: Translate each widget to (0, 0, 0).

    return best


if __name__ == '__main__':
    shapes = generateAllShapes()
    with open('shapes/allShapes.txt', 'w') as f:
        f.writelines([f'{shape}\n' for shape in shapes])
    print(len(shapes))

