import numpy as np


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
        if np.prod(direction) == -1:
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

