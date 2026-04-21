import itertools
import matplotlib.pyplot as plt
import numpy as np

from widget import Widget, getFirstWidgets


if __name__ == '__main__':
    widgets = getFirstWidgets(200)
    colors = ['rygb'[w.colorIndex] for w in widgets]
    points = [w.center for w in widgets]

    edges = []
    for p, q in itertools.combinations(points, 2):
        if ((np.array(p) - q) ** 2).sum() == 2:
            edges.append((p, q))

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(*zip(*points), c=colors)
    for e in edges:
        ax.plot(*zip(*e), c='k')
    plt.show()

