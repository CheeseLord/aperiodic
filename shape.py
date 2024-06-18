import itertools
import numpy as np

from widget import Widget


class Shape:
    def __init__(self, widgets, faces=None):
        if len(widgets) == 0:
            self.widgets = []
        elif isinstance(widgets[0], (tuple, list, np.ndarray)):
            self.widgets = [Widget(*x) for x in widgets]
        else:
            self.widgets = list(widgets)

        self.faces = faces

    def __len__(self):
        return len(self.widgets)

    def __eq__(self, other):
        return self.widgets == other.widgets

    def __add__(self, other):
        if isinstance(other, Shape):
            return Shape(self.widgets + other.widgets)
        return Shape(self.widgets + list(other))

    def __iter__(self):
        for w in self.widgets:
            yield w

    def __contains__(self, item):
        if isinstance(item, tuple):
            item = Widget(*item)
        return item in self.widgets

    def __hash__(self):
        return hash(tuple(self))

    def __repr__(self):
        return repr(self.widgets)

    def __array__(self):
        return np.array([tuple(w) for w in self.widgets])

    def translate(self, offset):
        if self.faces is None:
            newFaces = None
        else:
            newFaces = {
                (w.translate(offset), x.translate(offset)): label
                for (w, x), label in self.faces.items()
            }

        return Shape([w.translate(offset) for w in self], newFaces)

    def orient(self, target, orientation):
        arr = np.array(self)
        faceArr = []
        for w, x in self.faces:
            faceArr += [tuple(w), tuple(x)]
        faceArr = np.array(faceArr)

        # TODO: Unify this.
        if target.isOct:
            index, rotation = divmod(orientation, 4)
            index += 1
            for widget in self:
                if widget.isOct:
                    index -= 1
                if index == 0:
                    break

            arr[:, 0] -= widget.center
            faceArr[:, 0] -= widget.center

            # TODO: Make this a matrix.
            # Rotate the direction onto the target.
            axis = np.argmax(np.abs(widget.direction))
            targetAxis = np.argmax(np.abs(target.direction))
            arr = np.roll(arr, targetAxis - axis, axis=2)
            faceArr = np.roll(faceArr, targetAxis - axis, axis=2)
            if widget.direction[axis] != target.direction[targetAxis]:
                arr[:, :, targetAxis] *= -1
                arr[:, :, (targetAxis + 1) % 3] *= -1
                faceArr[:, :, targetAxis] *= -1
                faceArr[:, :, (targetAxis + 1) % 3] *= -1

            # Use the Rodrigues formula to rotate axes.
            x, y, z = target.direction
            mat = np.array([
                [x * x, -z, y],
                [z, y * y, -x],
                [-y, x, z * z],
            ], dtype=int)

        else:
            index, rotation = divmod(orientation, 3)
            index += 1
            for widget in self:
                if widget.isTet:
                    index -= 1
                if index == 0:
                    break

            arr[:, 0] -= widget.center
            faceArr[:, 0] -= widget.center

            # TODO: Make this a matrix.
            # Rotate the direction onto the target.
            arr *= widget.direction
            faceArr *= widget.direction
            if np.prod(widget.direction) * np.prod(target.direction) == -1:
                arr = arr[:, :, [1, 0, 2]]
                faceArr = faceArr[:, :, [1, 0, 2]]
            arr *= target.direction
            faceArr *= target.direction

            # Use the Rodrigues formula to rotate around the target axis.
            x, y, z = target.direction
            mat = np.array([
                [0, x * y - z, x * z + y],
                [x * y + z, 0, y * z - x],
                [x * z - y, y * z + x, 0],
            ], dtype=int) // 2

        rot = np.linalg.matrix_power(mat, rotation)
        arr = np.matmul(arr, rot)
        faceArr = np.matmul(faceArr, rot)

        arr[:, 0] += target.center
        faceArr[:, 0] += target.center

        faces = {}
        for i, label in zip(range(0, len(faceArr), 2), self.faces.values()):
            faces[(Widget(*faceArr[i]), Widget(*faceArr[i + 1]))] = label

        return Shape(arr, faces)

    def save(self, path):
        with open(path, 'a') as f:
            f.write(f'{self}\n')
            if self.faces is not None:
                f.write(f'{self.faces}\n')


def load(path):
    shapes = []
    with open(path) as f:
        for line in f.readlines():
            data = eval(line)
            if isinstance(data, list):
                shapes.append(Shape(data))
            else:
                shapes[-1].faces = {
                    (Widget(*w), Widget(*x)): label
                    for (w, x), label in data.items()
                }
    return shapes

