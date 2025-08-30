import numpy as np
from sympy import divisors


def partitions(n):
    return [np.array(p) for p in _partitions(n, n)]


def _partitions(n, bound):
    parts = []
    for d in divisors(n)[1: -1]:
        if d <= bound:
            parts += [[d] + x for x in _partitions(n // d, d)]
    if n <= bound:
        parts.append([n])

    return sorted(parts, reverse=True)


def indexToColor(n, parts):
    color = []
    for p in parts[::-1]:
        n, x = divmod(n, p)
        color.append(x)
    return np.array(color[::-1])

