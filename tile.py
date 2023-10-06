import itertools
import matplotlib.pyplot as plt
import numpy as np

from display import drawShapes
from generate import DIRECTIONS, generateShape


CENTERS = [
    c for c in itertools.product(range(-10, 11), repeat=3)
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
                if not (self.used & set(newShape)):
                    break

            self.redraw()

        # Rotate current backward.
        if event.key == '2':
            while True:
                self.orientation = (self.orientation - 1) % 12
                newShape = orient(self.shape, self.widgetIndex, self.orientation)
                if not (self.used & set(newShape)):
                    break

            self.redraw()

        # Accept current, add new.
        if event.key == '3':
            currentShape = orient(self.shape, self.widgetIndex, self.orientation)
            self.shapes.append(currentShape)
            self.positions.append((self.widgetIndex, self.orientation))
            used = self.used | set(currentShape)

            for i, widget in enumerate(WIDGETS):
                if widget not in self.used:
                    self.widgetIndex = i
                    break

            for orientation in range(12):
                if not (self.used & set(currentShape)):
                    self.used = used
                    self.orientation = orientation
                    break
            else:
                # TODO: Display error.
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
        newShape = orient(self.shape, self.widgetIndex, self.orientation)
        drawShapes(self.ax, self.shapes + [newShape])
        ax.scatter([0], [0], [0], c='k')
        ax.axes.set_xlim3d(-3, 3)
        ax.axes.set_ylim3d(-3, 3)
        ax.axes.set_zlim3d(-3, 3)
        self.fig.canvas.draw()


def orient(shape, widgetIndex, orientation):
    arr = np.array(shape)
    targetCenter, targetDirection = WIDGETS[widgetIndex]

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


if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    shape = generateShape()

    tiling = InteractiveTiling(fig, ax, shape)
    plt.show()

    #print(shape)
    #print(orient(shape, 0, 4))

