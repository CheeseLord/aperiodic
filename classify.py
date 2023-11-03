from enum import Enum
import itertools
import multiprocessing as mp
import numpy as np
import random
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


def explore(shape, maxSteps=1000):
    oriented = orient(shape, WIDGETS[0], np.random.randint(12))
    allTilings = [[oriented]]
    allUsed = [set(oriented)]

    best = [oriented]
    bestSize = 1

    for _ in range(maxSteps):
        if not allTilings:
            return Behavior.INVALID, bestSize + 1

        shapes = allTilings.pop()
        used = allUsed.pop()
        for widget in WIDGETS:
            if widget not in used:
                break

        for orientation in random.sample(range(12), 12):
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

    # TODO: Handle other lengths.
    for length in [4, 6, 8]:
        # TODO: Handle larger depths.
        for shapes in itertools.combinations(best[:15], length):
            if isRepeating(shapes):
                return Behavior.PERIODIC, len(shapes)

    return Behavior.UNKNOWN, bestSize


if __name__ == '__main__':
    PROCESSES = 4
    BATCH_SIZE = 100
    MAX_STEPS = 1000

    with open('shapes/unknown.txt') as f:
        shapes = [eval(l) for l in f.readlines()]

    i = 0
    pool = mp.Pool(processes=PROCESSES)
    batches = [
        shapes[i: i + BATCH_SIZE]
        for i in range(0, len(shapes), BATCH_SIZE)
    ]
    for b in batches:
        results = pool.starmap(explore, [(s, MAX_STEPS) for s in b])
        print(f'~~ {i: 5d} - {i + BATCH_SIZE - 1: 5d} ~~')
        for shape, (class_, size) in zip(b, results):
            className = str(class_).lower().split('.')[1]
            if class_ == Behavior.UNKNOWN:
                with open(f'shapes/working/unknown.txt', 'a') as f:
                    f.write(f'{shape}\n')
            else:
                with open(f'shapes/working/{className}-{size}.txt', 'a') as f:
                    f.write(f'{shape}\n')
                print(f'{i: 5d}', className, size)

            i += 1
    
