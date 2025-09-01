import itertools
import numpy as np

from widget import Widget


class Shape:
    def __init__(self, widgets):
        if len(widgets) == 0:
            self.widgets = []
        elif isinstance(widgets[0], (tuple, list, np.ndarray)):
            self.widgets = [Widget(*x) for x in widgets]
        else:
            self.widgets = list(widgets)

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
        return Shape([w.translate(offset) for w in self])

    def orient(self, target, index):
        widget = self.widgets[index]

        # Coarsely align the widget's current direction with the target's.
        axis = np.argmax(np.abs(widget.direction))
        targetAxis = np.argmax(np.abs(target.direction))
        transform = np.linalg.matrix_power(
            [[0, 0, 1], [1, 0, 0], [0, 1, 0]],
            targetAxis - axis,
        ).astype(int)
        if widget.direction[axis] != target.direction[targetAxis]:
            invert = np.eye(3, dtype=int)
            invert[targetAxis] *= -1
            invert[(targetAxis + 1) % 3] *= -1
            transform = np.matmul(invert, transform)

        # Rotate around the coarse axis.
        rot = np.array([[0, 1], [-1, 0]])
        rot = np.insert(rot, targetAxis, 0, axis=0)
        rot = np.insert(rot, targetAxis, 0, axis=1)
        rot[targetAxis, targetAxis] = 1
        while (np.matmul(transform, widget.direction) != target.direction).any():
            transform = np.matmul(rot, transform)

        arr = np.array(self)
        arr[:, 0] -= widget.center
        arr = np.matmul(arr, transform.T)
        arr[:, 0] += target.center

        return Shape(arr)

    def save(self, path):
        with open(path, 'a') as f:
            f.write(f'{self}\n')


def load(path):
    shapes = []
    with open(path) as f:
        for line in f.readlines():
            data = eval(line)
            shapes.append(Shape(data))
    return shapes

