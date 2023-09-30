import itertools
import matplotlib.pyplot as plt
import numpy as np

from display import drawShapes
from generate import DIRECTIONS, generateShape


CENTERS = [
    c for c in itertools.product(range(-5, 6), repeat=3)
    if sum(c) % 2 == 0
]
CENTERS.sort(key=np.linalg.norm)

WIDGETS = list(itertools.product(CENTERS, DIRECTIONS))


class InteractiveTiling:
    def __init__(self, fig, ax, shape):
        self.fig = fig
        self.ax = ax
        self.shape = shape

        self.shapes = []
        self.positions = []  # [(widget index, orientation)]
        self.used = set()

        self.widgetIndex = 0
        self.orientation = 0

        fig.canvas.mpl_connect('key_press_event', self.onPress)
        self.redraw()

    def onPress(self, event):
        # TODO: Pick better keys.

        # Rotate current forward.
        if event.key == '1':
            while True:
                self.orientation = (self.orientation + 1) % 12
                newShape = orient(self.shape, self.widgetIndex, self.orientation)
                good = True
                for widget in newShape:
                    if widget in self.used:
                        good = False
                        break
                if good:
                    break
            self.redraw()

        # Rotate current backward.
        if event.key == '2':
            while True:
                self.orientation = (self.orientation - 1) % 12
                newShape = orient(self.shape, self.widgetIndex, self.orientation)
                good = True
                for widget in newShape:
                    if widget in self.used:
                        good = False
                        break
                if good:
                    break
            self.redraw()

        # Accept current, add new.
        if event.key == '3':
            currentShape = orient(self.shape, self.widgetIndex, self.orientation)
            self.shapes.append(currentShape)
            self.positions.append((self.widgetIndex, self.orientation))
            self.used |= set(currentShape)

            # FIXME: Widget index.
            # FIXME: Orientation
            # FIXME: Handle impossible.
            self.redraw()

        # Delete current, return to old.
        if event.key == '4':
            if not self.shapes:
                return
            shape = self.shapes.pop()
            self.widgetIndex, self.orientation = self.positions.pop()
            self.used -= set(shape)
            self.redraw()

        # Skip widgets.
        if event.key == '5':
            # FIXME: Write this.
            pass


    def redraw(self):
        newShape = orient(self.shape, self.widgetIndex, self.orientation)
        drawShapes(self.ax, self.shapes + [newShape])
        self.fig.canvas.draw()


def orient(shape, widgetIndex, orientation):
    # FIXME: Write this.
    return shape


if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    shape = generateShape()

    tiling = InteractiveTiling(fig, ax, shape)

    plt.show()

