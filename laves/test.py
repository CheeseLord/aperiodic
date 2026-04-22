import itertools
import matplotlib.pyplot as plt
import numpy as np

from shape import Shape
from widget import Widget, getFirstWidgets


if __name__ == '__main__':
    shape = Shape(getFirstWidgets(10))

    fig = plt.figure()

    ax = fig.add_subplot(111, projection='3d')
    for target in [(0, 0, 0), (6, 7, 5)]:
        s = shape.orient(Widget(target), 0)
        colors = ['rygb'[w.colorIndex] for w in s]
        points = [w.center for w in s]

        edges = []
        for p, q in itertools.combinations(points, 2):
            if ((np.array(p) - q) ** 2).sum() == 2:
                edges.append((p, q))

        ax.scatter(*zip(*points), c=colors)
        for e in edges:
            ax.plot(*zip(*e), c='k')

    plt.show()

