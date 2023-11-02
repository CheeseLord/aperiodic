import itertools
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    points = [(0, 0, 0), (1, 1, 0), (1, 0, 1), (2, 1, 1)]
    diffs = [tuple(np.array(x) - y) for x, y in itertools.combinations(points, 2)]

    """
    for a, b, c in itertools.product(range(len(points)), repeat=3):
        valid = True
        for x, y, z in diffs:
            color = (
                a * (y + z - x)
                + b * (z + x - y)
                + c * (x + y - z)
            ) // 2
            if color % len(points) == 0:
                valid = False
        if valid:
            break
    else:
        raise ValueError()
    """
    for a, b, c in itertools.product(range(len(points)), repeat=3):
        a = np.array([a // 2, a % 2], dtype=int)
        b = np.array([b // 2, b % 2], dtype=int)
        c = np.array([c // 2, c % 2], dtype=int)

        valid = True
        for x, y, z in diffs:
            color = (
                a * (y + z - x)
                + b * (z + x - y)
                + c * (x + y - z)
            ) // 2
            if not np.any(color % 2):
                valid = False
        if valid:
            break
    else:
        raise ValueError()
    a = 2 * a[0] + a[1]
    b = 2 * b[0] + b[1]
    c = 2 * c[0] + c[1]

    grid = [
        t for t in itertools.product(range(-5, 6), repeat=3)
        if sum(t) % 2 == 0
    ]
    colors = []
    for x, y, z in grid:
        color = (
            a * (y + z - x)
            + b * (z + x - y)
            + c * (x + y - z)
        ) // 2
        colors.append('rgby'[color % len(points)])

    ax.scatter(*zip(*grid), c=colors, alpha=0.5)
    ax.scatter(*zip(*points), c='k', s=20, alpha=1)
    plt.show()

