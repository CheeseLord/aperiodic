from collections import defaultdict
import itertools
import numpy as np
from pysat.solvers import Glucose3

from shape import Shape, load
from widget import Widget


def getFundamentalWidgets(basis):
    # Get all points in a prism containing the fundamental parallelapiped.
    bounds = np.sum(np.abs(basis), axis=1)
    possible = list(itertools.product(*[range(-x, x) for x in bounds]))
    possible = [
        offset for offset in possible
        if all([x % 2 == 0 for x in offset])
        and len(set(x % 4 for x in offset)) == 1
    ]
    possible = sorted(possible, key=np.linalg.norm)

    # Remove corresponding points.
    centers = []
    for center in possible:
        arr = np.array(center)
        for other in centers:
            coeffs = np.linalg.solve(basis, arr - other)
            if np.allclose(coeffs - np.round(coeffs), 0):
                break
        else:
            centers.append(center)

    # The basis only gives one color of widget, so generate the others.
    widgets = []
    for c in centers:
        widgets.append(Widget(c))
        widgets += widgets[-1].neighbors
    return widgets


def wrap(shape, basis, fundamental):
    wrapped = []
    for widget in shape:
        for target in fundamental:
            coeffs = np.linalg.solve(
                basis, np.array(widget.center) - target.center
            )
            if np.allclose(coeffs - np.round(coeffs), 0):
                wrapped.append(target)
                break

    return Shape(wrapped)


def isRepeatingBasis(shape, basis, fundamental):
    if len(fundamental) % len(shape) != 0:
        return None

    # Find all possible tiles containing these widgets.
    shapes = []
    s = set()
    covering = defaultdict(list)
    for widget in fundamental:
        for index in range(len(shape)):
            for rotation in range(2):
                newShape = wrap(
                    shape.orient(widget, index, rotation), basis, fundamental
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

        merged = []
        for tile in tiling:
            merged += []
        assert len(merged) == len(set(merged))

        return tiling, basis

    return None


if __name__ == '__main__':
    import multiprocessing as mp

    PROCESSES = 8
    BATCH_SIZE = 20

    allShapes = load('shapes/allShapes.txt')
    shapes = load('shapes/unknown.txt')

    with open('bases.txt') as f:
        bases = [eval(l) for l in f.readlines()]

    bases = bases[:10]
    for b in bases:
        print(b)

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
            shape.save(f'shapes/working/periodic-{period}.txt')

            index = allShapes.index(shape) + 1
            with open(f'shapes/certificates/{index:05d}.txt', 'w+') as f:
                f.write(f'{shape}\n')
                f.write(f'{basis}\n')
                f.write('\n')
                for tile in tiling:
                    f.write(f'{tile}\n')

