import itertools
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from scipy.spatial import ConvexHull


if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.axes.set_xlim3d(-2, 2)
    ax.axes.set_ylim3d(-2, 2)
    ax.axes.set_zlim3d(-2, 2)
    
    # Octahedra.
    vertices = np.array([
        [0, 0, 0],
        [0, 0, 2],
        [0, 1, 1],
        [1, 0, 1],
        [0, -1, 1],
        [-1, 0, 1],
        [2 / 3, 2 / 3, 4 / 3],
        [2 / 3, -2 / 3, 4 / 3],
        [-2 / 3, -2 / 3, 4 / 3],
        [-2 / 3, 2 / 3, 4 / 3],
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
    faces = vertices[indices]

    colors = 'rgbcmy'
    for (i, j), color in zip(itertools.product([1, -1], range(3)), colors):
        modified = np.roll(faces, j, axis=2) * i

        poly = Poly3DCollection(modified)
        #poly.set_color(color)
        poly.set_color('b')
        poly.set_alpha(0.3)
        poly.set_edgecolor('k')
        ax.add_collection3d(poly)

    # Tetrahedra.
    vertices = np.array([
        [0, 0, 0],
        [1, 1, 1],
        [1, 1, 0],
        [1, 0, 1],
        [0, 1, 1],
        [4 / 3, 2 / 3, 2 / 3],
        [2 / 3, 2 / 3, 4 / 3],
        [2 / 3, 4 / 3, 2 / 3],
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
    faces = vertices[indices]

    colors = 'cwgybmkr'
    for (i, j, k), color in zip(itertools.product([1, -1], repeat=3), colors):
        modified = faces * (i, j, k)

        poly = Poly3DCollection(modified)
        #poly.set_color(color)
        poly.set_color('r')
        poly.set_alpha(0.3)
        poly.set_edgecolor('k')
        ax.add_collection3d(poly)

    plt.show()

