import colorsys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from scipy.spatial import ConvexHull


if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    vertices = np.array([
        [0, 0, 1 / 2],
        [1, 0, 1 / 2],
        [1 / 2, 1 / 2, 0],
        [1 / 2, 1 / 2, 1],
    ])
    circumcenters = np.array([
        [5 / 8, 3 / 8, 1 / 2],
        [3 / 8, 3 / 8, 1 / 2],
        [1 / 2, 1 / 8, 5 / 8],
        [1 / 2, 1 / 8, 3 / 8],
    ])

    for i in range(1):
    #for i in range(4):
        hsv = (i * 0.618, 0.7, 0.7)
        color = '#' + ''.join(
            hex(int(x * 255))[2:]
            for x in colorsys.hsv_to_rgb(*hsv)
        )

        widget = [vertices[i]]
        widget.append(np.mean(vertices, axis=0))
        for j in range(4):
            if j == i:
                continue
            widget.append((vertices[i] + vertices[j]) / 2)
            widget.append(circumcenters[j])

        widget = np.array(widget)
        hull = ConvexHull(widget)
        poly = Poly3DCollection(widget[hull.simplices])
        poly.set_color(color)
        poly.set_alpha(0.3)
        poly.set_edgecolor('k')
        ax.add_collection3d(poly)

    ax.axes.set_xlim3d(-0.1, 1.1)
    ax.axes.set_ylim3d(-0.1, 1.1)
    ax.axes.set_zlim3d(-0.1, 1.1)

    plt.show()

