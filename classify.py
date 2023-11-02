from enum import Enum
import more_itertools
import numpy as np
import time

from geometry import WIDGETS, orient
from periodic import isRepeating


class Behavior(Enum):
    PERIODIC = 0
    INVALID = 1
    UNKNOWN = 2


def classify(shape, maxDepth=6):
    oriented = orient(shape, WIDGETS[0], 0)
    allTilings = [[oriented]]
    allUsed = [set(oriented)]
    for i in range(2, maxDepth + 1):
        newTilings = []
        newUsed = []
        # Expand each tiling in each possible way.
        for shapes, used in zip(allTilings, allUsed):
            for widget in WIDGETS:
                if widget not in used:
                    break

            for orientation in range(12):
                newShape = orient(shape, widget, orientation)
                newSet = set(newShape)
                if used & newSet:
                    continue
                newShapes = shapes + [newShape]
                if isRepeating(newShapes):
                    return Behavior.PERIODIC, i
                newTilings.append(newShapes)
                newUsed.append(used | newSet)

        if not newTilings:
            return Behavior.INVALID, i
        allTilings = newTilings
        allUsed = newUsed

    return Behavior.UNKNOWN, maxDepth


def explore(shape, timeout=1):
    oriented = orient(shape, WIDGETS[0], 0)
    allTilings = [[oriented]]
    allUsed = [set(oriented)]

    best = [oriented]
    bestSize = 1

    end = time.time() + timeout
    while time.time() < end:
        if not allTilings:
            return Behavior.INVALID, bestSize + 1

        shapes = allTilings.pop()
        used = allUsed.pop()
        for widget in WIDGETS:
            if widget not in used:
                break

        for orientation in range(12):
            newShape = orient(shape, widget, orientation)
            newSet = set(newShape)
            if used & newSet:
                continue
            newShapes = shapes + [newShape]
            if len(newShapes) > bestSize:
                best = newShapes
                bestSize = len(newShapes)

            allTilings.append(newShapes)
            allUsed.append(used | newSet)

        # TODO: Handle larger depths.
        if bestSize == 20:
            break

    # TODO: Handle larger depths.
    for shapes in more_itertools.powerset(best[:20]):
        if len(shapes) == 0:
            continue

        # TODO: Handle larger subsets.
        if len(shapes) > 6:
            break

        if isRepeating(shapes):
            return Behavior.PERIODIC, len(shapes)

    return Behavior.UNKNOWN, bestSize


if __name__ == '__main__':
    with open('shapes/unknown.txt') as f:
        shapes = [eval(l) for l in f.readlines()]
    for i, shape in enumerate(shapes):
        class_, size = explore(shape, 1)
        className = str(class_).lower().split('.')[1]
        if class_ == Behavior.UNKNOWN:
            with open(f'shapes/working/unknown.txt', 'a') as f:
                f.write(f'{shape}\n')
        else:
            with open(f'shapes/working/{className}-{size}.txt', 'a') as f:
                f.write(f'{shape}\n')
        print(f'{i: 5d}', className, size)

