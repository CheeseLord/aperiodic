from collections import defaultdict
import itertools
import more_itertools
import numpy as np
from pysat.solvers import Glucose3
import random

from linearAlgebra import makeCanonical
from shape import Shape
from widget import DIRECTIONS, Widget


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

    return [Widget(*w) for w in itertools.product(centers, DIRECTIONS)]


def wrap(shape, basis, fundamental):
    mat = np.array(basis).T

    wrapped = []
    for widget in shape:
        for target in fundamental:
            if target.direction != widget.direction:
                continue
            coeffs = np.linalg.solve(
                mat, np.array(widget.center) - target.center
            )
            if np.allclose(coeffs - np.round(coeffs), 0):
                wrapped.append(target)
                break

    return Shape(wrapped)


def isRepeatingBasis(shape, basis, fundamental, useReflections=False):
    volume = len(shape) // 7
    if useReflections:
        reflections = [1, -1]
    else:
        reflections = [1]

    # Find all possible tiles containing these widgets.
    shapes = []
    s = set()
    covering = defaultdict(list)
    for widget in fundamental:
        for reflection in reflections:
            flipped = Shape(np.array(shape) * reflection)
            for orientation in range(12 * volume):
                newShape = wrap(
                    flipped.orient(widget, orientation), basis, fundamental
                )
                if len(newShape) != len(set(newShape)):
                    continue
                if newShape in s:
                    continue

                shapes.append(newShape)
                s.add(newShape)
                for w in newShape:
                    covering[w].append(len(shapes))

    # Find the satisfiability constraints.
    constraints = []
    # Make sure all the necessary widgets are covered.
    for widget in fundamental:
        constraints.append(covering[widget])
    # Make sure no widget is covered more than once.
    for widget in covering:
        # TODO: Make this more efficient.
        for i, j in itertools.combinations(covering[widget], 2):
            constraints.append([-i, -j])

    # Solve the constraints.
    with Glucose3() as solver:
        for c in constraints:
            solver.add_clause(c)
        if not solver.solve():
            return None

        result = solver.get_model()

    return [shapes[x - 1] for x in result if x > 0]



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
        allShapes = [Shape(eval(l)) for l in f.readlines()]
    with open('shapes/unknown.txt') as f:
        shapes = [Shape(eval(l)) for l in f.readlines()]
    with open('shapes/bases.txt') as f:
        bases = [eval(l) for l in f.readlines()]

    # bases = bases[:207]
    # bases = bases[207:]

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

