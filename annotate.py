from collections import Counter, defaultdict
import random
import numpy as np

from shape import Shape


def annotateRandom(shape):
    oo = []
    ot = []
    to = []
    tt = []
    for widget in shape:
        for neighbor in widget.neighbors:
            if neighbor in shape:
                continue
            face = (widget, neighbor)
            if widget.isOct and neighbor.isOct:
                oo.append(face)
            elif widget.isOct:
                ot.append(face)
            elif neighbor.isOct:
                to.append(face)
            else:
                tt.append(face)

    otLabels = [1]
    while len(otLabels) < len(ot):
        otLabels.append(random.randint(1, max(otLabels) + 1))

    c = Counter(otLabels)
    toLabels = [1] * c[1]
    for n in range(2, max(c) + 1):
        for _ in range(c[n]):
            toLabels.insert(
                random.randint(toLabels.index(n - 1) + 1, len(toLabels)), n
            )
    toLabels = [-n for n in toLabels]

    # TODO: Handle multiple forms of 0.
    ooLabels = makeSequence(len(oo))
    ttLabels = makeSequence(len(tt))

    faces = ot + to + oo + tt
    labels = otLabels + toLabels + ooLabels + ttLabels
    shape.faces = dict(zip(faces, labels))


def makeSequence(n):
    # Make a valid sequence.
    indices = list(range(n))
    random.shuffle(indices)
    used = defaultdict(list)
    used[0] = []
    while len(indices) > 0:
        i = random.randint(0, max(used) + 1)
        if len(indices) == 1:
            i = 0

        used[i].append(indices[0])
        indices = indices[1:]
        if i > 0:
            used[-i].append(indices[0])
            indices = indices[1:]

    # Relabel in canonical order.
    seq = np.zeros(n, dtype=int)
    for i in range(1, max(used) + 1):
        if min(used[i]) > min(used[-i]):
            used[i], used[-i] = used[-i], used[i]
    for i, j in enumerate(
        sorted(range(1, max(used) + 1), key=lambda x: min(used[x])),
        start=1,
    ):
        seq[used[j]] = i
        seq[used[-j]] = -i

    return list(seq)

