import itertools
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np


# Directions around a vertex.
DIRECTIONS = [
    (x, y, z) for x, y, z in itertools.product([1, 0, -1], repeat=3)
    if (x + y + z) % 2 == 1
]

# Adjacent directions at the same vertex.
VERTEX_ADJACENT = {
    direction: [] for direction in DIRECTIONS
}
for direction in DIRECTIONS:
    if 0 in direction:
        continue
    for otherDir in DIRECTIONS:
        if sorted(np.abs(np.array(direction) - otherDir)) == [0, 1, 1]:
            VERTEX_ADJACENT[direction].append(otherDir)
            VERTEX_ADJACENT[otherDir].append(direction)

# Adjacent directions around centers of polyhedra.
CENTER_ADJACENT = {
    direction: [] for direction in DIRECTIONS
}
for direction in DIRECTIONS:
    if 0 in direction:
        for i in range(3):
            if direction[i] != 0:
                continue
            for j in [-1, 1]:
                v = np.zeros(3, dtype=int)
                v[i] = j
                CENTER_ADJACENT[direction].append(
                    (tuple(direction - v), tuple(v))
                )
    else:
        for i in range(3):
            v = np.ones(3, dtype=int) * -1
            v[i] = 1
            v *= direction
            CENTER_ADJACENT[direction].append(
                (tuple((direction - v) // 2), tuple(v))
            )

# Template for octahedron slice.
OCTAHEDRON_VERTICES = np.array([
    [0, 0, 0],
    [1, 0, 0],
    [1 / 2, 0, 1 / 2],
    [1 / 2, 1 / 2, 0],
    [1 / 2, 0, -1 / 2],
    [1 / 2, -1 / 2, 0],
    [2 / 3, 1 / 3, 1 / 3],
    [2 / 3, 1 / 3, -1 / 3],
    [2 / 3, -1 / 3, -1 / 3],
    [2 / 3, -1 / 3, 1 / 3],
])
indices = [
    [0, i + 2, i + 6, (i + 1) % 4 + 2]
    for i in range(4)
]
indices += [
    [1, i + 6, (i + 1) % 4 + 2, (i + 1) % 4 + 6]
    for i in range(4)
]
indices = np.array(indices)
OCTAHEDRON_FACES = OCTAHEDRON_VERTICES[indices]

# Template for tetrahedron slice.
TETRAHEDRON_VERTICES = np.array([
    [0, 0, 0],
    [1 / 2, 1 / 2, 1 / 2],
    [1 / 2, 1 / 2, 0],
    [1 / 2, 0, 1 / 2],
    [0, 1 / 2, 1 / 2],
    [2 / 3, 1 / 3, 1 / 3],
    [1 / 3, 1 / 3, 2 / 3],
    [1 / 3, 2 / 3, 1 / 3],
])
indices = [
    [0, i + 2, i + 5, (i + 1) % 3 + 2]
    for i in range(3)
]
indices += [
    [1, i + 5, (i + 1) % 3 + 2, (i + 1) % 3 + 5]
    for i in range(3)
]
indices = np.array(indices)
TETRAHEDRON_FACES = TETRAHEDRON_VERTICES[indices]


def getNeighbors(center, direction):
    sameVertex = [
        (center, otherDir) for otherDir in VERTEX_ADJACENT[direction]
    ]
    sameCenter = [
        (tuple(np.array(center) + otherCenter), otherDir)
        for otherCenter, otherDir in CENTER_ADJACENT[direction]
    ]
    return sameVertex + sameCenter


def generateShape():
    shape = [
        ((0, 0, 0), (1, 0, 0)),
        ((0, 0, 0), (1, 1, 1)),
    ]
    neighbors = [getNeighbors(*x) for x in shape]
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
        neighbors.extend(getNeighbors(*n))

    return shape


def generateAllShapes():
    shape = [
        ((0, 0, 0), (1, 0, 0)),
        ((0, 0, 0), (1, 1, 1)),
    ]
    shapes = _generateHelper(shape, 2, 3)
    return [list(y) for y in {tuple(sorted(x)) for x in shapes}]


def _generateHelper(shape, o, t):
    if o == t == 0:
        return [shape]

    neighbors = set()
    for x in shape:
        neighbors = neighbors.union(getNeighbors(*x))
    neighbors = neighbors.difference(shape)

    shapes = []
    for other in neighbors:
        isOct = (0 in other[1])
        if isOct and o > 0:
            shapes += _generateHelper(shape + [other], o - 1, t)
        if not isOct and t > 0:
            shapes += _generateHelper(shape + [other], o, t - 1)

    return shapes


if __name__ == '__main__':
    shapes = generateAllShapes()
    print(len(shapes))
    print(shapes[0])

    """
    rows, cols = 1, 1
    fig = plt.figure()
    for i in range(1, rows * cols + 1):
        ax = fig.add_subplot(rows, cols, i, projection='3d')

        lower = np.zeros(3, dtype=float)
        upper = np.zeros(3, dtype=float)

        shape = generateShape()
        for center, direction in shape:
            if 0 in direction:
                index = (np.array(direction) != 0).argmax()
                faces = np.roll(OCTAHEDRON_FACES, index, axis=2)
                faces[:, :, index] *= direction[index]
                faces += center

                lower = np.minimum(lower, np.min(np.min(faces, axis=0), axis=0))
                upper = np.maximum(upper, np.max(np.max(faces, axis=0), axis=0))

                poly = Poly3DCollection(faces)
                poly.set_color('r')
                poly.set_alpha(0.3)
                poly.set_edgecolor('k')
                ax.add_collection3d(poly)
            else:
                faces = TETRAHEDRON_FACES * direction + center

                lower = np.minimum(lower, np.min(np.min(faces, axis=0), axis=0))
                upper = np.maximum(upper, np.max(np.max(faces, axis=0), axis=0))

                poly = Poly3DCollection(faces)
                poly.set_color('b')
                poly.set_alpha(0.3)
                poly.set_edgecolor('k')
                ax.add_collection3d(poly)

        width = np.max(upper - lower) / 2 + 0.1
        center = (upper + lower) / 2

        ax.axes.set_xlim3d(center[0] - width, center[0] + width)
        ax.axes.set_ylim3d(center[1] - width, center[1] + width)
        ax.axes.set_zlim3d(center[2] - width, center[2] + width)
    plt.show()
    """

