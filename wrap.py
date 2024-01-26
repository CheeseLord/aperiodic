import exact_cover
import itertools
import more_itertools
import numpy as np
import random

from geometry import DIRECTIONS, orient


def getFundamentalWidgets(basis):
    mat = np.array(basis).T
    possible = [
        offset for offset in itertools.product(range(-10, 11), repeat=3)
        if sum(offset) % 2 == 0
    ]
    possible = sorted(possible, key=np.linalg.norm)
    centers = []
    for center in possible:
        arr = np.array(center)
        for c in centers:
            coeffs = np.linalg.solve(mat, arr - c)
            if np.allclose(coeffs - np.round(coeffs), 0):
                break
        else:
            centers.append(center)

    assert round(abs(np.linalg.det(basis))) == 2 * len(centers)

    return list(itertools.product(centers, DIRECTIONS))


def wrap(shape, basis, fundamental):
    mat = np.array(basis).T

    wrapped = []
    for center, direction in shape:
        center = np.array(center)
        for c, d in fundamental:
            if d != direction:
                continue
            coeffs = np.linalg.solve(mat, center - c)
            if np.allclose(coeffs - np.round(coeffs), 0):
                wrapped.append((c, d))
                break

    return wrapped


def isRepeating(shape, basis, fundamental):
    widgets = {w: i for i, w in enumerate(fundamental)}

    # Find the subsets that can be covered with a single tile.
    subsets = {}
    for widget in fundamental:
        for orientation in range(12):
            newShape = wrap(
                orient(shape, widget, orientation), basis, fundamental
            )
            s = [widgets[w] for w in newShape if w in widgets]
            subsets[tuple(sorted(s))] = newShape
    indices = random.sample(list(subsets), len(subsets))

    # Find an exact cover for the widgets.
    arr = np.zeros((len(indices), len(fundamental)), dtype=bool)
    for i, s in enumerate(indices):
        arr[i, s] = True
    try:
        cover_ = exact_cover.get_exact_cover(arr)
        return [subsets[indices[i]] for i in cover_]
    except exact_cover.error.NoSolution:
        return None


if __name__ == '__main__':
    with open('shapes/unknown.txt') as f:
        shapes = [eval(l) for l in f.readlines()]

    while True:
        mat = np.random.randint(-5, 6, (3, 3))
        basis = []
        for v in mat:
            v[0] += sum(v) % 2
            basis.append(tuple(v))
        period = int(abs(round(np.linalg.det(basis))))
        if 0 < period < 20:
            break
    print(f'Basis: {basis} (period {period})')

    fundamental = getFundamentalWidgets(basis)

    for i, shape in enumerate(shapes, start=1):
        thing = isRepeating(shape, basis, fundamental)
        if thing is not None:
            print(f'* {i} *')
            with open(f'shapes/working/periodic-{period}.txt', 'a') as f:
                f.write(f'{shape}\n')
        if i % 10 == 0 or i == len(shapes):
            print(f'Finished {i}')

