import itertools
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


def getNeighbors(widget):
    center, direction = widget
    sameVertex = [
        (center, otherDir) for otherDir in VERTEX_ADJACENT[direction]
    ]
    sameCenter = [
        (tuple(np.array(center) + otherCenter), otherDir)
        for otherCenter, otherDir in CENTER_ADJACENT[direction]
    ]
    return sameVertex + sameCenter


WIDGETS = []
_used = set()
_toExpand = [((0, 0, 0), (1, 0, 0))]
while len(WIDGETS) < 20000:
    w = _toExpand[0]
    _toExpand = _toExpand[1:]
    if w in _used:
        continue
    WIDGETS.append(w)
    _used.add(w)
    _toExpand.extend([x for x in getNeighbors(w) if x not in _used])


def orient(shape, widget, orientation):
    arr = np.array(shape)
    targetCenter, targetDirection = widget

    if 0 in targetDirection:
        position, rotation = divmod(orientation, 4)
        count = position + 1
        for center, direction in shape:
            if 0 in direction:
                count -= 1
            if count == 0:
                break

        arr[:, 0] -= center

        # Rotate the direction onto the target.
        axis = np.argmax(np.abs(direction))
        targetAxis = np.argmax(np.abs(targetDirection))
        arr = np.roll(arr, targetAxis - axis, axis=2)
        if direction[axis] != targetDirection[targetAxis]:
            arr[:, :, targetAxis] *= -1
            arr[:, :, (targetAxis + 1) % 3] *= -1

        # Use the Rodrigues formula to rotate axes.
        x, y, z = targetDirection
        mat = np.array([
            [1 - y * y - z * z, x * y - z, x * z + y],
            [x * y + z, 1 - x * x - z * z, y * z - x],
            [x * z - y, y * z + x, 1 - x * x - y * y],
        ])
        rot = np.linalg.matrix_power(mat, rotation)
        arr = np.matmul(arr, rot)

        arr[:, 0] += targetCenter

        return [(tuple(x[0]), tuple(x[1])) for x in arr]
    else:
        position, rotation = divmod(orientation, 3)
        count = position + 1
        for center, direction in shape:
            if 0 not in direction:
                count -= 1
            if count == 0:
                break

        arr[:, 0] -= center

        # Rotate the direction onto the target.
        arr *= direction
        if np.prod(direction) * np.prod(targetDirection) == -1:
            arr = arr[:, :, [1, 0, 2]]
        arr *= targetDirection

        # Use the Rodrigues formula to rotate around the target axis.
        x, y, z = targetDirection
        mat = np.array([
            [0, x * y - z, x * z + y],
            [x * y + z, 0, y * z - x],
            [x * z - y, y * z + x, 0],
        ], dtype=int) // 2
        rot = np.linalg.matrix_power(mat, rotation)
        arr = np.matmul(arr, rot)

        arr[:, 0] += targetCenter

        return [(tuple(x[0]), tuple(x[1])) for x in arr]


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

