import itertools
import numpy as np

from widget import Widget


with open('rotations.txt', 'r') as f:
    ROTATIONS = eval(f.read())


class Shape:
    def __init__(self, widgets):
        if len(widgets) == 0:
            self.widgets = []
        elif isinstance(widgets[0], (tuple, list, np.ndarray)):
            self.widgets = [Widget(*x) for x in widgets]
        else:
            self.widgets = list(widgets)

        self.neighbors = {
            w: [x for x in w.neighbors if x in self.widgets] for w in self.widgets
        }

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
            for r in range(2):
                best = min(best, sorted(self.orient(Widget(0, 0, 0), i, r)))

        return Shape(best)

    def translate(self, offset):
        return Shape([w.translate(offset) for w in self])

    def orient(self, target, index, rotation):
        widget = self.widgets[index]

        matrix = np.array(
            ROTATIONS[(widget.colorIndex, target.colorIndex)][rotation]
        )

        newWidgets = []
        for w in self.widgets:
            center = np.array(w) - np.array(widget)
            center = np.round(np.dot(matrix, center.T).T).astype(int)
            center += target.center
            newWidgets.append(Widget(center))

        return Shape(newWidgets)

    def colorize(self):
        return '[' + ', '.join(w.colorize() for w in self) + ']'

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

