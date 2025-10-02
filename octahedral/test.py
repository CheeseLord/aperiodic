from collections import Counter, defaultdict
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
import os

from display import drawShapes, getAxis
from shape import Shape, load
from satisfy import cover


def distance(tile):
    total = 0
    for w in tile:
        total += np.linalg.norm(w.center)
    return total


if __name__ == '__main__':
    index = 0
    shape = load('shapes/unknown.txt')[index]
    shapeIndex = load('shapes/allShapes.txt').index(shape) + 1
    tiling = load(f'gallery/{shapeIndex}/00001.txt')

    meta = defaultdict(list)
    for tile in tiling:
        (c, _), (d, _) = Counter(w.center for w in tile).most_common()
        meta[c].append(tuple((np.array(d) - c) * 0.4))

    ax = getAxis()

    numMeta = 500
    for center in sorted(meta, key=np.linalg.norm):
        if center[0] % 2 != 0:
            continue

        if not (center[0] == -center[2] and center[0] == 2):
            continue

        face = np.array([
            np.array(center) + direction for direction in meta[center]
        ])
        poly = Poly3DCollection([face])
        poly.set_color('b')
        poly.set_alpha(0.3)
        poly.set_edgecolor('k')
        ax.add_collection3d(poly)

        numMeta -= 1
        if numMeta == 0:
            break

    plt.show()


    """
    allShapes = load('shapes/allShapes.txt')
    shapes = load('shapes/unknown.txt')
    for shape in shapes:
        shapeIndex = allShapes.index(shape) + 1
        path = f'gallery/{shapeIndex}'
        if not os.path.exists(path):
            os.mkdir(path)

        while len(os.listdir(path)) < 10:
            tiling = cover(shape, 100000)
            tilingIndex = len(os.listdir(path)) + 1
            with open(f'{path}/{tilingIndex:05d}.txt', 'w+') as f:
                for tile in tiling:
                    f.write(f'{tile}\n')
    """

