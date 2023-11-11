from enum import Enum
import itertools
import multiprocessing as mp
import numpy as np
import random

from geometry import WIDGETS, orient
from periodic import isRepeating, isAlmostRepeating


class Behavior(Enum):
    PERIODIC = 0
    INVALID = 1
    UNKNOWN = 2


def classify(shape, maxDepth=6):
    for o in range(12):
        oriented = orient(shape, WIDGETS[0], o)
        allTilings = [[oriented]]
        allUsed = [set(oriented)]

        bestSize = 1
        invalid = True
        while allTilings:
            shapes = allTilings.pop()
            used = allUsed.pop()

            if isRepeating(shapes):
                return Behavior.PERIODIC, len(shapes)
            if len(shapes) == maxDepth:
                invalid = False
                continue

            for widget in WIDGETS:
                if widget not in used:
                    break

            for orientation in range(12):
                newShape = orient(shape, widget, orientation)
                newSet = set(newShape)
                if used & newSet:
                    continue
                newShapes = shapes + [newShape]
                bestSize = max(bestSize, len(newShapes))

                allTilings.append(newShapes)
                allUsed.append(used | newSet)

        if invalid:
            return Behavior.INVALID, bestSize + 1

    return Behavior.UNKNOWN, maxDepth


def explore(shape, maxSteps):
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

        # TODO: Handle larger depths.
        if bestSize == 30:
            break

    # TODO: Handle larger subsets.
    relevant = random.sample(best, min(bestSize, 15))
    # TODO: Handle other periods.
    for period in [6, 8]:
        for shapes in itertools.combinations(relevant, period - 1):
            if isAlmostRepeating(shapes):
                return Behavior.PERIODIC, period

    return Behavior.UNKNOWN, bestSize


def findInvalid(shape, maxSteps):
    best = []
    bestSize = 0
    steps = maxSteps // 12

    for o in range(12):
        oriented = orient(shape, WIDGETS[0], o)
        allTilings = [[oriented]]
        allUsed = [set(oriented)]


        for _ in range(steps):
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

    return Behavior.UNKNOWN, bestSize


if __name__ == '__main__':
    PROCESSES = 4
    BATCH_SIZE = 100
    MAX_STEPS = 2000

    with open('shapes/unknown.txt') as f:
        shapes = [eval(l) for l in f.readlines()]

    pool = mp.Pool(processes=PROCESSES)
    batches = [
        shapes[i: i + BATCH_SIZE]
        for i in range(0, len(shapes), BATCH_SIZE)
    ]

    i = 0
    for b in batches:
        results = pool.starmap(explore, [(s, MAX_STEPS) for s in b])
        print(f'~~ {i + 1: 5d} - {min(i + BATCH_SIZE, len(shapes)): 5d} ~~')
        for shape, (class_, size) in zip(b, results):
            className = str(class_).lower().split('.')[1]
            if class_ == Behavior.UNKNOWN:
                with open(f'shapes/working/unknown.txt', 'a') as f:
                    f.write(f'{shape}\n')
            else:
                with open(f'shapes/working/{className}-{size}.txt', 'a') as f:
                    f.write(f'{shape}\n')
                print(f'{i + 1: 5d}', className, size)

            i += 1

