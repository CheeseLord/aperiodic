import exact_cover
import multiprocessing as mp
import numpy as np
import random
import time
import timeout_decorator

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
    NUM_WIDGETS = 20000
    TIMEOUT = 30

    wrapped = timeout_decorator.timeout(TIMEOUT, use_signals=False)(cover)
    with open('shapes/unknown.txt') as f:
        shapes = [eval(l) for l in f.readlines()]

    invalid = 0
    finished = 0
    timeouts = 0
    for i, shape in enumerate(shapes, start=1):
        if i % 100 == 1:
            print(f'~~ Starting {i: 5d} - {min(i + 99, len(shapes))} ~~')

        try:
            cover_ = wrapped(shape, NUM_WIDGETS)
        except timeout_decorator.timeout_decorator.TimeoutError:
            with open(f'shapes/working/unknown.txt', 'a') as f:
                f.write(f'{shape}\n')
            timeouts += 1
        else:
            if cover_ is None:
                with open(
                    f'shapes/working/invalid-cover-{NUM_WIDGETS}.txt', 'a'
                ) as f:
                    f.write(f'{shape}\n')
                invalid += 1
                print(f'{i: 5d} invalid')
            else:
                with open(f'shapes/working/unknown.txt', 'a') as f:
                    f.write(f'{shape}\n')
                with open(f'shapes/frequent.txt', 'a') as f:
                    f.write(f'{NUM_WIDGETS}, {TIMEOUT}, {shape}\n')
                finished += 1
                print(f'{i: 5d} finished')
                for s in cover_:
                    with open(f'shapes/working/tiling{i:03d}.txt', 'a') as f:
                        f.write(f'{s}\n')

        if i % 100 == 0 or i == len(shapes):
            print(f'~~ Finished {(i - 1) // 100 * 100 + 1: 5d} - {i} ~~')

    print(f'Invalid: {invalid}')
    print(f'Finished: {finished}')
    print(f'Timeouts: {timeouts}')

    if invalid:
        exit(1)

