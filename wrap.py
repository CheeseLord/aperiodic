import exact_cover
import itertools
import more_itertools
import numpy as np
import random

from geometry import DIRECTIONS, orient
from linearAlgebra import makeCanonical


def getFundamentalWidgets(basis):
    mat = np.array(basis).T
    bounds = np.sum(np.abs(mat), axis=1)
    possible = list(itertools.product(*[range(-x, x) for x in bounds]))
    possible = [
        offset for offset in possible if sum(offset) % 2 == 0
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


def isRepeatingBasis(shape, basis, fundamental):
    volume = len(shape) // 7
    widgets = {w: i for i, w in enumerate(fundamental)}

    # Find the subsets that can be covered with a single tile.
    subsets = {}
    for widget in fundamental:
        for orientation in range(12 * volume):
            newShape = wrap(
                orient(shape, widget, orientation), basis, fundamental
            )
            if len(newShape) != len(set(newShape)):
                continue
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


def isRepeating(shape, bases):
    for basis in bases:
        fundamental = getFundamentalWidgets(basis)
        tiling = isRepeatingBasis(shape, basis, fundamental)

        if tiling is None:
            continue

        period = len(tiling)
        volume = len(shape) // 7
        assert period * volume == int(abs(round(np.linalg.det(basis))))

        merged = []
        for tile in tiling:
            merged += []
        assert len(merged) == len(set(merged))

        return tiling, basis

    return None


if __name__ == '__main__':
    import multiprocessing as mp

    PROCESSES = 4
    BATCH_SIZE = 20

    with open('shapes/allShapes.txt') as f:
        allShapes = [eval(l) for l in f.readlines()]
    with open('shapes/unknown.txt') as f:
        shapes = [eval(l) for l in f.readlines()]
    with open('shapes/bases.txt') as f:
        bases = [eval(l) for l in f.readlines()]

    bases = bases[:11]

    pool = mp.Pool(processes=PROCESSES)
    batches = [
        shapes[i: i + BATCH_SIZE]
        for i in range(0, len(shapes), BATCH_SIZE)
    ]

    i = 0
    for b in batches:
        results = pool.starmap(isRepeating, [(s, bases) for s in b])
        print(f'~~ {i + 1: 5d} - {min(i + BATCH_SIZE, len(shapes)): 5d} ~~')

        for shape, result in zip(b, results):
            i += 1
            if result is None:
                continue

            tiling, basis = result
            period = len(tiling)
            print(f'{i: 5d}: Periodic {period} ({basis})')
            with open(f'shapes/working/periodic-{period}.txt', 'a') as f:
                f.write(f'{shape}\n')

            index = allShapes.index(shape) + 1
            with open(f'shapes/certificates/{index:05d}.txt', 'w+') as f:
                f.write(f'{shape}\n')
                f.write(f'{basis}\n')
                f.write('\n')
                for tile in tiling:
                    f.write(f'{tile}\n')

    """
    while True:
        target = random.choice([48])
        mat = np.random.randint(-target, target + 1, (3, 3))
        basis = []
        for v in mat:
            v[0] += sum(v) % 2
            basis.append(tuple(v))

        period = int(abs(round(np.linalg.det(basis))))
        if period != target:
            continue

        reduced = makeCanonical(basis)
        if reduced in bases:
            continue

        break

    print(f'Basis: {basis} (period {period})')
    print(f'Reduced: {reduced}')

    fundamental = getFundamentalWidgets(basis)

    for i, shape in enumerate(shapes, start=1):
        thing = isRepeatingBasis(shape, basis, fundamental)
        if thing is not None:
            print(f'* {i} *')
            with open(f'shapes/working/periodic-{period}.txt', 'a') as f:
                f.write(f'{shape}\n')
        if i % 10 == 0 or i == len(shapes):
            print(f'Finished {i}')

    with open('shapes/bases.txt', 'a') as f:
        f.write(f'{reduced}\n')
    """

