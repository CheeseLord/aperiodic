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
            item = Widget(item)
        return item in self.widgets

    def __hash__(self):
        return hash(tuple(self))

    def __repr__(self):
        return repr(self.widgets)

    def __array__(self):
        return np.array(self.widgets)

    @property
    def canonical(self):
        best = sorted(self)
        for i in range(len(self)):
            for r in range(3):
                best = min(best, sorted(self.orient(Widget(0, 0, 0), i, r)))

        return Shape(best)

    def translate(self, offset):
        return Shape([w.translate(offset) for w in self])

    def orient(self, target, index, rotation):
        widget = self.widgets[index]

        power = (target.colorIndex - widget.colorIndex) % 4
        m = np.array([
            [1, 0, 0],
            [0, 0, -1],
            [0, 1, 0],
        ])
        r = np.array([
            [0, 1, 0],
            [0, 0, 1],
            [1, 0, 0],
        ])
        arr = np.dot(
            np.linalg.matrix_power(r, rotation),
            np.linalg.matrix_power(m, power),
        )

        newWidgets = []
        for w in self.widgets:
            center = np.array(w) - np.array(widget)
            center = np.dot(arr, center.T).T
            center += target.center
            newWidgets.append(Widget(center))

        return Shape(newWidgets)

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

