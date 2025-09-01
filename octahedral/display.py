import colorsys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np


# Template for single widget.
VERTICES = np.array([
    [0, 0, 0],
    [0, 1, 2],
    [0, 3/2, 3/2],
    [1, 1, 1],
    [1/2, 1/2, 2],
    [0, 0, 2],
    [-1/2, 1/2, 2],
    [-1, 1, 1],
])
indices = np.array([
    [1, 2, 3, 4],
    [0, 3, 4, 5],
    [1, 4, 5, 6],
    [0, 5, 6, 7],
    [1, 6, 7, 2],
    [0, 7, 2, 3],
])
FACES = VERTICES[indices]


def drawShapes(ax, shapes):
    lower = np.zeros(3, dtype=float)
    upper = np.zeros(3, dtype=float)

    for i, shape in enumerate(shapes):
        hsv = (i * 0.618, 0.7, 0.7)
        color = '#' + ''.join(
            hex(int(x * 255))[2:]
            for x in colorsys.hsv_to_rgb(*hsv)
        )
        for widget in shape:
            faces = FACES.copy()
            reflect = False

            # Permute the axes.
            indices = np.abs(widget.direction)
            faces = faces[:, :, indices]
            reflect ^= (indices[0] > indices[1])
            reflect ^= (indices[0] > indices[2])
            reflect ^= (indices[1] > indices[2])

            # Negate coordinates.
            for i, coord in enumerate(widget.direction):
                if coord < 0:
                    faces[:, :, i] *= -1
                    reflect = not reflect

            # Make sure we have a rotation, not a reflection.
            if reflect:
                faces[:, :, list(indices).index(0)] *= -1

            faces += widget.center

            lower = np.minimum(lower, np.min(np.min(faces, axis=0), axis=0))
            upper = np.maximum(upper, np.max(np.max(faces, axis=0), axis=0))

            poly = Poly3DCollection(faces)
            poly.set_color(color)
            poly.set_alpha(0.3)
            poly.set_edgecolor('k')
            ax.add_collection3d(poly)

    width = np.max(upper - lower) / 2 + 0.1
    center = (upper + lower) / 2

    ax.axes.set_xlim3d(center[0] - width, center[0] + width)
    ax.axes.set_ylim3d(center[1] - width, center[1] + width)
    ax.axes.set_zlim3d(center[2] - width, center[2] + width)


def getAxis():
    fig = plt.figure()
    return fig.add_subplot(111, projection='3d')


if __name__ == '__main__':
    from widget import Widget, DIRECTIONS

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    shape = [Widget((0, 0, 0), d) for d in DIRECTIONS]
    drawShapes(ax, [shape])

    plt.show()

