import itertools
import matplotlib.pyplot as plt
import numpy as np
import random

from generate import generateAllShapes
from shape import Shape
from widget import Widget, getFirstWidgets


if __name__ == '__main__':
    shapes = generateAllShapes(5)
    #shape = random.choice(shapes)
    #shape = Shape(getFirstWidgets(10))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for i, shape in enumerate(shapes):
        s = shape.orient(Widget((0, 0, 0)), 0, 0)
        s = s.translate((4 * i, 0, 0))
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

