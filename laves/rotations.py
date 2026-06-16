from collections import defaultdict
import itertools
import numpy as np


vectors = np.array([
    [(0, 0, 0), (-1, 0, 1), (0, 1, -1), (1, -1, 0)],
    [(1, 0, -1), (0, 0, 0), (-1, -1, 0), (0, 1, 1)],
    [(0, -1, 1), (1, 1, 0), (0, 0, 0), (-1, 0, -1)],
    [(-1, 1, 0), (0, -1, -1), (1, 0, 1), (0, 0, 0)],
])
opposites = [(x, y) for x in range(4) for y in range(4) if x != y and x != 3 - y]


if __name__ == '__main__':
    arrays = defaultdict(list)

    for srcMaj, srcMin in opposites:
        v1 = vectors[srcMaj, srcMin]
        v2 = vectors[srcMaj, (3 - srcMin)]
        srcMatrix = np.array([v1, v2, np.cross(v1, v2)])

        for dstMaj, dstMin in opposites:
            v1 = vectors[dstMaj, dstMin]
            v2 = vectors[dstMaj, (3 - dstMin)]
            dstMatrix = np.array([v1, v2, np.cross(v1, v2)])

            rotation = np.round(dstMatrix.T @ np.linalg.inv(srcMatrix.T)).astype(int)

            arr = tuple(tuple(int(x) for x in row) for row in rotation)
            if arr not in arrays[(srcMaj, dstMaj)]:
                arrays[(srcMaj, dstMaj)].append(arr)

    with open('rotations.txt', 'w') as f:
        f.write(str(dict(arrays)))

