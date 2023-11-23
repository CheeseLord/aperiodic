import exact_cover
import multiprocessing as mp
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
        cover_ = exact_cover.get_exact_cover(arr)
        return [subsets[indices[i]] for i in cover_]
    except exact_cover.error.NoSolution:
        return None


def bestCover(shape):
    maxTime = 60
    minWidgets = 210
    maxWidgets = 230
    widgetStep = 10

    shapes = []
    numWidgets = minWidgets
    while True:
        start = time.time()
        shapes = cover(shape, numWidgets)
        end = time.time()
        if shapes is None:
            return None, numWidgets
        if end - start > maxTime:
            return shapes, numWidgets
        if numWidgets >= maxWidgets:
            return shapes, numWidgets
        numWidgets += widgetStep


if __name__ == '__main__':
    PROCESSES = 4
    BATCH_SIZE = 100

    with open('shapes/unknown.txt') as f:
        shapes = [eval(l) for l in f.readlines()]

    pool = mp.Pool(processes=PROCESSES)
    batches = [
        shapes[i: i + BATCH_SIZE]
        for i in range(0, len(shapes), BATCH_SIZE)
    ]

    i = 0
    for b in batches:
        results = pool.map(bestCover, b)
        print(f'~~ {i + 1: 5d} - {min(i + BATCH_SIZE, len(shapes)): 5d} ~~')

        for shape, (cover_, numWidgets) in zip(b, results):
            if cover_ is None:
                with open(
                    f'shapes/working/invalid-cover-{numWidgets}.txt', 'a'
                ) as f:
                    f.write(f'{shape}\n')
                print(f'{i + 1: 5d} invalid {numWidgets}')
            else:
                with open(f'shapes/working/unknown.txt', 'a') as f:
                    f.write(f'{shape}\n')

            i += 1

