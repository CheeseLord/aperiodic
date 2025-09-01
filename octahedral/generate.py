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

