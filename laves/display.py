import colorsys
import matplotlib.pyplot as plt
import numpy as np


def drawShapes(ax, shapes):
    lower = np.zeros(3, dtype=float)
    upper = np.zeros(3, dtype=float)

    for i, shape in enumerate(shapes):
        hsv = (i * 0.618, 0.7, 0.7)
        color = '#' + ''.join(
            hex(int(x * 255))[2:]
            for x in colorsys.hsv_to_rgb(*hsv)
        )

        points = [w.center for w in shape]
        ax.scatter(*zip(*points))

        for w in shape:
            for x in w.neighbors:
                if x < w and x in shape:
                    ax.plot(*zip(*[w.center, x.center]), c='k')

        lower = np.minimum(lower, np.min(shape, axis=0))
        upper = np.maximum(upper, np.max(shape, axis=0))

    width = np.max(upper - lower) / 2 + 0.1
    center = (upper + lower) / 2

    ax.axes.set_xlim3d(center[0] - width, center[0] + width)
    ax.axes.set_ylim3d(center[1] - width, center[1] + width)
    ax.axes.set_zlim3d(center[2] - width, center[2] + width)


def getAxis():
    fig = plt.figure()
    return fig.add_subplot(111, projection='3d')

