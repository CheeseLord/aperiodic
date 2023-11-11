import matplotlib.pyplot as plt
import numpy as np

from display import drawShapes
from geometry import WIDGETS, orient


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
                newShape = orient(
                    self.shape, WIDGETS[self.widgetIndex], self.orientation
                )
                if not (self.used & set(newShape)):
                    break

            self.redraw()

        # Rotate current backward.
        if event.key == '2':
            while True:
                self.orientation = (self.orientation - 1) % 12
                newShape = orient(
                    self.shape, WIDGETS[self.widgetIndex], self.orientation
                )
                if not (self.used & set(newShape)):
                    break

            self.redraw()

        # Accept current, add new.
        if event.key == '3':
            currentShape = orient(
                self.shape, WIDGETS[self.widgetIndex], self.orientation
            )
            self.shapes.append(currentShape)
            self.positions.append((self.widgetIndex, self.orientation))
            used = self.used | set(currentShape)

            for i, widget in enumerate(WIDGETS):
                if widget not in used:
                    self.widgetIndex = i
                    break

            for orientation in range(12):
                newShape = orient(
                    self.shape, WIDGETS[self.widgetIndex], orientation
                )
                if not (used & set(newShape)):
                    self.used = used
                    self.orientation = orientation
                    break
            else:
                # TODO: Display error.
                print('Invalid configuration')
                shape = self.shapes.pop()
                self.widgetIndex, self.orientation = self.positions.pop()

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
        self.ax.clear()
        newShape = orient(
            self.shape, WIDGETS[self.widgetIndex], self.orientation
        )
        drawShapes(self.ax, self.shapes + [newShape])
        ax.scatter([0], [0], [0], c='k')
        ax.axes.set_xlim3d(-3, 3)
        ax.axes.set_ylim3d(-3, 3)
        ax.axes.set_zlim3d(-3, 3)
        self.fig.canvas.draw()


if __name__ == '__main__':
    import argparse
    import random

    parser = argparse.ArgumentParser()
    parser.add_argument('shape_file', nargs='?', default='shapes/unknown.txt')
    args = parser.parse_args()

    with open(args.shape_file) as f:
        shapes = [eval(l) for l in f.readlines()]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    shape = random.choice(shapes)

    tiling = InteractiveTiling(fig, ax, shape)
    plt.show()

