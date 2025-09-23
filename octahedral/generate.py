import itertools
import numpy as np
import random

from widget import Widget
from shape import Shape


def generateRandomShape(n):
    shape = Shape([((0, 0, 0), (0, 1, 2))])

    while len(shape) < n:
        neighbors = set()
        for w in shape:
            neighbors = neighbors.union(w.neighbors)
        neighbors = neighbors.difference(shape)
        shape = shape + [random.choice(list(neighbors))]

    return shape.canonical


def generateAllShapes(n):
    if n == 1:
        return [Shape([((0, 0, 0), (0, 1, 2))])]

    shapes = set()
    for subshape in generateAllShapes(n - 1):
        neighbors = set()
        for w in subshape:
            neighbors = neighbors.union(w.neighbors)
        neighbors = neighbors.difference(subshape)

        for neighbor in neighbors:
            shape = subshape + [neighbor]
            shapes.add(tuple(sorted(shape, key=tuple)))
    shapes = list({Shape(s).canonical for s in shapes})

    return shapes


if __name__ == '__main__':
    # shapes = []
    # for i in range(1, 8):
    #    shapes += generateAllShapes(i)
    shapes = generateAllShapes(8)

    for shape in shapes:
        shape.save('shapes/allShapes.txt')

