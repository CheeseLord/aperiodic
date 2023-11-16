import exact_cover
import numpy as np
import random
import time

from geometry import WIDGETS, orient


def cover(shape, numWidgets):
    widgets = {w: i for i, w in enumerate(WIDGETS[:numWidgets])}

    # Find the subsets that can be covered by a single tile.
    subsets = {}
    for widget in widgets:
        for orientation in range(12):
            newShape = sorted(orient(shape, widget, orientation))
            s = [widgets[w] for w in newShape if w in widgets]
            subsets[tuple(sorted(s))] = newShape
    indices = random.sample(list(subsets), len(subsets))

    # Find an exact cover for the widgets.
    arr = np.zeros((len(indices), numWidgets), dtype=bool)
    for i, s in enumerate(indices):
        arr[i, s] = True
    try:
        cover = exact_cover.get_exact_cover(arr)
        return [subsets[indices[i]] for i in cover]
    except exact_cover.error.NoSolution:
        return None


def bestCover(shape):
    numWidgets = 10
    while True:
        start = time.time()
        shapes = cover(shape, numWidgets)
        if shapes is None:
            return None
        if time.time() - start > 300:
            return shapes, numWidgets
        if numWidgets >= 10 ** 4:
            return shapes, numWidgets
        numWidgets += 10


if __name__ == '__main__':
    COVER_SIZE = 200

    with open('shapes/unknown.txt') as f:
        shapes = [eval(l) for l in f.readlines()]
    for i, shape in enumerate(shapes, start=1):
        if i % 100 == 0:
            print(i)
        if cover(shape, COVER_SIZE) is None:
            print(i, shape)
            with open(f'shapes/working/invalid-cover.txt', 'a') as f:
                f.write(f'{shape}\n')
        else:
            with open(f'shapes/working/unknown.txt', 'a') as f:
                f.write(f'{shape}\n')

