from collections import Counter
from enum import Enum
import itertools
import numpy as np

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


if __name__ == '__main__':
    with open('shapes/unknown.txt') as f:
        shapes = [eval(l) for l in f.readlines()]
    for i, shape in enumerate(shapes):
        class_, size = classify(shape)
        className = str(class_).lower().split('.')[1]
        with open(f'shapes/working/{className}-{size}.txt', 'a') as f:
            f.write(f'{shape}\n')
        print(f'{i: 5d}', className, size)

