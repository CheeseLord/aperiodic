from collections import defaultdict
from pysat.pb import PBEnc
from pysat.solvers import Glucose3
import random

from shape import Shape, load
from widget import getFirstWidgets


def cover(shape, numWidgets):
    widgets = getFirstWidgets(numWidgets)

    # Find all possible tiles containing these widgets.
    shapes = []
    s = set()
    covering = defaultdict(list)
    for widget in widgets:
        for index in range(len(shape)):
            for rotation in range(2):
                newShape = Shape(sorted(shape.orient(widget, index, rotation)))
                if newShape in s:
                    continue

                shapes.append(newShape)
                s.add(newShape)
                for w in newShape:
                    covering[w].append(len(shapes))

    # Find the satisfiability constraints.
    constraints = []
    # Make sure all the necessary widgets are covered.
    for widget in widgets:
        constraints.append(covering[widget])
    # Make sure no widget is covered more than once.
    maxId = len(shapes)
    for widget in covering:
        pb = PBEnc.atmost(covering[widget], bound=1, top_id=maxId)
        for clause in pb.clauses:
            constraints.append(clause)
            maxId = max(maxId, max(clause))
    # Place the first tile to break symmetry.
    constraints.append([1])

    random.shuffle(constraints)

    # Solve the constraints.
    with Glucose3() as solver:
        for c in constraints:
            solver.add_clause(c)
        if not solver.solve():
            return None

        result = solver.get_model()

    return [shapes[x - 1] for x in result if 0 < x <= len(shapes)]


if __name__ == '__main__':
    import argparse
    import timeout_decorator
    import time

    TIMEOUT = 3600

    parser = argparse.ArgumentParser()
    parser.add_argument('numWidgets')
    args = parser.parse_args()
    numWidgets = int(args.numWidgets)

    #wrapped = timeout_decorator.timeout(TIMEOUT, use_signals=False)(cover)
    wrapped = cover

    shapes = load('shapes/unknown.txt')

    for i, shape in enumerate(shapes, start=1):
        try:
            start = time.time()
            result = wrapped(shape, numWidgets)
            end = time.time()
        except timeout_decorator.timeout_decorator.TimeoutError:
            print(f'{i: 5d} timeout')
            continue

        if result is None:
            with open(
                f'shapes/working/invalid-satisfy-{numWidgets}.txt', 'a'
            ) as f:
                f.write(f'{shape}\n')
            print(f'{i: 5d} {"~" * 30} invalid')
            continue

        print(f'{i: 5d} finished ({end - start:g} seconds)')

