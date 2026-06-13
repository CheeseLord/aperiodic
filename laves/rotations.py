from collections import defaultdict
import itertools
import numpy as np


ry = (-1, 0, 1)
rg = (0, 1, -1)
rb = (1, -1, 0)
r_ = (1, 1, 1)

yg = (-1, -1, 0)
yb = (0, 1, 1)
yr = (1, 0, -1)
y_ = (1, -1, 1)

gb = (-1, 0, -1)
gr = (0, -1, 1)
gy = (1, 1, 0)
g_ = (1, -1, -1)

br = (-1, 1, 0)
by = (0, -1, -1)
bg = (1, 0, 1)
b_ = (1, 1, -1)

colorPairs = {
    'r': 'b',
    'y': 'g',
    'g': 'y',
    'b': 'r',
}
colorMap = {
    'r': 0,
    'y': 1,
    'g': 2,
    'b': 3,
}


if __name__ == '__main__':
    arrays = defaultdict(list)
    for srcMaj, srcMin in itertools.chain(
        itertools.product('rb', 'yg'), itertools.product('yg', 'rb')
    ):
        srcOtherMaj = colorPairs[srcMaj]
        for dstMaj, dstMin in itertools.chain(
            itertools.product('rb', 'yg'), itertools.product('yg', 'rb')
        ):
            dstOtherMaj = colorPairs[dstMaj]

            thing = eval(f'[{srcMaj}{srcOtherMaj}, {srcMaj}{srcMin}, {srcMaj}_]')
            stuff = eval(f'[{dstMaj}{dstOtherMaj}, {dstMaj}{dstMin}, {dstMaj}_]')
            arr = np.round(3 * np.dot(np.linalg.inv(thing), stuff).T).astype(int)
            arr = tuple(tuple(row) for row in arr)

            if arr not in arrays[(colorMap[srcMaj], colorMap[dstMaj])]:
                arrays[(colorMap[srcMaj], colorMap[dstMaj])].append(arr)

    with open('rotations.txt', 'w') as f:
        f.write(str(dict(arrays)))

