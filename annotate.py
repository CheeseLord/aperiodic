from collections import Counter, defaultdict
import random
import numpy as np


def getFaces(shape):
    faces = []
    for w in shape:
        for neighbor in getNeighbors(w):
            if neighbor not in shape:
                faces.append((w, neighbor))
    return faces


def annotateRandom(shape):
    oo = []
    ot = []
    to = []
    tt = []
    for a, b in getFaces(shape):
        if 0 in a[1] and 0 in b[1]:
            oo.append((a, b))
        elif 0 in a[1]:
            ot.append((a, b))
        elif 0 in b[1]:
            to.append((a, b))
        else:
            tt.append((a, b))

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
    return list(zip(faces, labels))


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


if __name__ == '__main__':
    with open('shapes/allShapes.txt') as f:
        shapes = [eval(l) for l in f.readlines()]
    shape = shapes[0]

    for x in annotateRandom(shape):
        print(x)

