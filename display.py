import colorsys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from scipy.spatial import ConvexHull


# Template for octahedron slice.
OCTAHEDRON_VERTICES = np.array([
    [0, 0, 0],
    [1, 0, 0],
    [1 / 2, 0, 1 / 2],
    [1 / 2, 1 / 2, 0],
    [1 / 2, 0, -1 / 2],
    [1 / 2, -1 / 2, 0],
    [2 / 3, 1 / 3, 1 / 3],
    [2 / 3, 1 / 3, -1 / 3],
    [2 / 3, -1 / 3, -1 / 3],
    [2 / 3, -1 / 3, 1 / 3],
])
indices = [
    [0, i + 2, i + 6, (i + 1) % 4 + 2]
    for i in range(4)
]
indices += [
    [1, i + 6, (i + 1) % 4 + 2, (i + 1) % 4 + 6]
    for i in range(4)
]
indices = np.array(indices)
OCTAHEDRON_FACES = OCTAHEDRON_VERTICES[indices]

# Template for tetrahedron slice.
TETRAHEDRON_VERTICES = np.array([
    [0, 0, 0],
    [1 / 2, 1 / 2, 1 / 2],
    [1 / 2, 1 / 2, 0],
    [1 / 2, 0, 1 / 2],
    [0, 1 / 2, 1 / 2],
    [2 / 3, 1 / 3, 1 / 3],
    [1 / 3, 1 / 3, 2 / 3],
    [1 / 3, 2 / 3, 1 / 3],
])
indices = [
    [0, i + 2, i + 5, (i + 1) % 3 + 2]
    for i in range(3)
]
indices += [
    [1, i + 5, (i + 1) % 3 + 2, (i + 1) % 3 + 5]
    for i in range(3)
]
indices = np.array(indices)
TETRAHEDRON_FACES = TETRAHEDRON_VERTICES[indices]


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
            if widget.isOct:
                index = (np.array(widget.direction) != 0).argmax()
                faces = np.roll(OCTAHEDRON_FACES, index, axis=2)
                faces[:, :, index] *= widget.direction[index]
                faces += widget.center
            else:
                faces = TETRAHEDRON_FACES * widget.direction + widget.center

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


def drawHull(ax, shapes, color):
    lower = np.zeros(3, dtype=float)
    upper = np.zeros(3, dtype=float)

    vertices = []
    for shape in shapes:
        for widget in shape:
            if widget.isOct:
                index = (np.array(widget.direction) != 0).argmax()
                faces = np.roll(OCTAHEDRON_FACES, index, axis=2)
                faces[:, :, index] *= widget.direction[index]
                faces += widget.center
            else:
                faces = TETRAHEDRON_FACES * widget.direction + widget.center

            lower = np.minimum(lower, np.min(np.min(faces, axis=0), axis=0))
            upper = np.maximum(upper, np.max(np.max(faces, axis=0), axis=0))

            for face in faces:
                for vertex in face:
                    vertices.append(vertex)

    vertices = np.array(vertices)
    hull = ConvexHull(vertices)
    poly = Poly3DCollection(vertices[hull.simplices])
    poly.set_color(color)
    poly.set_alpha(0.3)
    poly.set_edgecolor('k')
    ax.add_collection3d(poly)

    width = np.max(upper - lower) / 2 + 0.1
    center = (upper + lower) / 2

    ax.axes.set_xlim3d(center[0] - width, center[0] + width)
    ax.axes.set_ylim3d(center[1] - width, center[1] + width)
    ax.axes.set_zlim3d(center[2] - width, center[2] + width)


if __name__ == '__main__':
    from generate import generateShape

    rows, cols = 2, 3
    fig = plt.figure()
    for i in range(rows * cols):
        ax = fig.add_subplot(rows, cols, i + 1, projection='3d')
        shape = generateShape()
        drawShapes(ax, [shape])
    plt.show()

