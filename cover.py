import exact_cover
import numpy as np
import random

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
    for i, s in enumerate(indices): arr[i, s] = True
    try:
        cover_ = exact_cover.get_exact_cover(arr)
        return [subsets[indices[i]] for i in cover_]
    except exact_cover.error.NoSolution:
        return None


if __name__ == '__main__':
    from collections import defaultdict
    import multiprocessing as mp
    import timeout_decorator

    NUM_WIDGETS = 220
    TIMEOUT = 60 * 60 * 24
    BATCH = 20

    with open('shapes/unknown.txt') as f:
        shapes = [eval(l) for l in f.readlines()]

    frequent = defaultdict(int)
    with open('shapes/frequent.txt') as f:
        lines = [eval(l) for l in f.readlines()]
    for n, t, shape in lines:
        frequent[tuple(shape)] = max(n, frequent[tuple(shape)])

    wrapped = timeout_decorator.timeout(TIMEOUT, use_signals=False)(cover)

    invalid = 0
    finished = 0
    timeouts = 0
    skipped = 0
    for i, shape in enumerate(shapes, start=1):
        if i % BATCH == 1:
            print(f'~~ Starting {i: 5d} - {min(i + BATCH - 1, len(shapes))} ~~')

        if frequent[tuple(shape)] >= NUM_WIDGETS:
            reason = 'high'
        elif frequent[tuple(shape)] <= NUM_WIDGETS * 0.7:
            reason = 'low'
        else:
            reason = ''

        if reason:
            with open(f'shapes/working/unknown.txt', 'a') as f:
                f.write(f'{shape}\n')
            skipped += 1
            print(f'{i: 5d} skipped ({reason})')
            if i % BATCH == 0 or i == len(shapes):
                print(f'~~ Finished {(i - 1) // BATCH * BATCH + 1: 5d} - {i} ~~')
            continue

        try:
            cover_ = wrapped(shape, NUM_WIDGETS)
        except timeout_decorator.timeout_decorator.TimeoutError:
            with open(f'shapes/working/unknown.txt', 'a') as f:
                f.write(f'{shape}\n')
            timeouts += 1
            print(f'{i: 5d} timed out')
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

                """
                # NOTE: This includes the original shape for easy comparison.
                for s in [shape] + cover_:
                    with open(f'shapes/working/tiling{i:03d}.txt', 'a') as f:
                        f.write(f'{s}\n')
                """

        if i % BATCH == 0 or i == len(shapes):
            print(f'~~ Finished {(i - 1) // BATCH * BATCH + 1: 5d} - {i} ~~')

    print(f'Invalid: {invalid}')
    print(f'Finished: {finished}')
    print(f'Timeouts: {timeouts}')
    print(f'Skipped: {skipped}')

    if invalid:
        exit(1)

