import numpy as np

from widget import Widget


class Shape:
    def __init__(self, widgets):
        self.widgets = widgets

    def __eq__(self, other):
        return self.widgets == other.widgets

    def __iter__(self):
        for w in self.widgets:
            yield w

    def __repr__(self):
        return repr(self.widgets)

    def translate(self, offset):
        return Shape([w.translate(offset) for w in self])

    def orient(self, target, orientation):
        arr = np.array([tuple(w) for w in self])

        if target.isOct:
            index, rotation = divmod(orientation, 4)
            index += 1
            for widget in self:
                if widget.isOct:
                    index -= 1
                if index == 0:
                    break

            arr[:, 0] -= widget.center

            # Rotate the direction onto the target.
            axis = np.argmax(np.abs(widget.direction))
            targetAxis = np.argmax(np.abs(target.direction))
            arr = np.roll(arr, targetAxis - axis, axis=2)
            if widget.direction[axis] != target.direction[targetAxis]:
                arr[:, :, targetAxis] *= -1
                arr[:, :, (targetAxis + 1) % 3] *= -1

            # Use the Rodrigues formula to rotate axes.
            x, y, z = target.direction
            mat = np.array([
                [1 - y * y - z * z, x * y - z, x * z + y],
                [x * y + z, 1 - x * x - z * z, y * z - x],
                [x * z - y, y * z + x, 1 - x * x - y * y],
            ])
            rot = np.linalg.matrix_power(mat, rotation)
            arr = np.matmul(arr, rot)

            arr[:, 0] += target.center

            return Shape([Widget(*x) for x in arr])

        else:
            index, rotation = divmod(orientation, 3)
            index += 1
            for widget in self:
                if widget.isTet:
                    index -= 1
                if index == 0:
                    break

            arr[:, 0] -= widget.center

            # Rotate the direction onto the target.
            arr *= widget.direction
            if np.prod(widget.direction) * np.prod(target.direction) == -1:
                arr = arr[:, :, [1, 0, 2]]
            arr *= target.direction

            # Use the Rodrigues formula to rotate around the target axis.
            x, y, z = target.direction
            mat = np.array([
                [0, x * y - z, x * z + y],
                [x * y + z, 0, y * z - x],
                [x * z - y, y * z + x, 0],
            ], dtype=int) // 2
            rot = np.linalg.matrix_power(mat, rotation)
            arr = np.matmul(arr, rot)

            arr[:, 0] += target.center

            return Shape([Widget(*x) for x in arr])

