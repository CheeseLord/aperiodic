import itertools
import numpy as np


# Directions around a vertex.
DIRECTIONS = [
    (x, y, z) for x, y, z in itertools.product([1, 0, -1], repeat=3)
    if (x + y + z) % 2 == 1
]

# Centers of widgets.
# TODO: Find a better way to organize these.
CENTERS = [
    c for c in itertools.product(range(-10, 11), repeat=3)
    if sum(c) % 2 == 0
]
CENTERS.sort(key=np.linalg.norm)

WIDGETS = list(itertools.product(CENTERS, DIRECTIONS))


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

