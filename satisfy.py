from collections import defaultdict
import itertools
import numpy as np
from pysat.solvers import Glucose3

from geometry import WIDGETS, orient


def cover(shape, numWidgets):
    volume = len(shape) // 7
    widgets = WIDGETS[:numWidgets]

    # Find all possible tiles containing these widgets.
    shapes = []
    s = set()
    covering = defaultdict(list)
    for widget in widgets:
        for orientation in range(12 * volume):
            newShape = sorted(orient(shape, widget, orientation))
            if tuple(newShape) in s:
                continue

            shapes.append(newShape)
            s.add(tuple(newShape))
            for w in newShape:
                covering[w].append(len(shapes))

    # Find the satisfiability constraints.
    constraints = []
    # Make sure all the necessary widgets are covered.
    for widget in widgets:
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


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('numWidgets')
    args = parser.parse_args()
    numWidgets = int(args.numWidgets)


    with open('shapes/unknown.txt') as f:
        shapes = [eval(l) for l in f.readlines()]

    for i, shape in enumerate(shapes, start=1):
        result = cover(shape, numWidgets)
        if result is None:
            with open(
                f'shapes/working/invalid-satisfy-{numWidgets}.txt', 'a'
            ) as f:
                f.write(f'{shape}\n')
            print(f'{i: 5d} invalid')
            continue

        print(f'{i: 5d} finished')

        combined = []
        for x in result:
            combined += x
        for widget in WIDGETS[:numWidgets]:
            assert widget in combined
        assert len(combined) == len(set(combined))

