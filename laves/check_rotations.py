import numpy as np
import sys

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

edges = [
    [ r_, ry, rg, rb ],
    [ yr, y_, yg, yb ],
    [ gr, gy, g_, gb ],
    [ br, by, bg, b_ ],
]

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

colorNames = 'rygb'

PERMS = [
    (0, 1, 2, 3), # RYGB -> RYGB  ()
    (0, 2, 1, 3), # RYGB -> RGYB  (G Y)
    (3, 1, 2, 0), # RYGB -> BYGR  (R B)
    (3, 2, 1, 0), # RYGB -> BGYR  (R B) (G Y)

    (2, 3, 0, 1), # RYGB -> GBRY  (R G) (B Y)
    (2, 0, 3, 1), # RYGB -> GRBY  (R G B Y)
    (1, 3, 0, 2), # RYGB -> YBRG  (R Y B G)
    (1, 0, 3, 2), # RYGB -> YRBG  (R Y) (B G)
]

def findEdgeName(vec, doThird=True):
    if doThird:
        thirdVec = np.round(np.array(vec) / 3).astype(int)
        if not np.allclose(vec, 3*thirdVec):
            return "??"
        vec = thirdVec
    for c1 in range(4):
        for c2 in range(4):
            if np.allclose(edges[c1][c2], vec):
                return colorNames[c1] + colorNames[c2]
    return "??"


if __name__ == '__main__':
    if len(sys.argv) == 1:
        fname = 'rotations.txt'
    elif len(sys.argv) == 2:
        fname = sys.argv[1]
    else:
        assert False
    with open(fname, 'r') as f:
        ROTATIONS = eval(f.read())

    for perm in PERMS:
        for origin in range(4):
            mappedNames = ""
            for i in range(4):
                mappedNames += colorNames[perm[i]]
            srcMaj      = origin
            srcOtherMaj = colorMap[colorPairs[colorNames[srcMaj]]]
            srcMin      = [x for x in range(4) if x not in [srcMaj, srcOtherMaj]][0]
            dstMaj      = perm[srcMaj]
            dstOtherMaj = perm[srcOtherMaj]
            dstMin      = perm[srcMin]
            assert dstOtherMaj == colorMap[colorPairs[colorNames[dstMaj]]]
            key = (srcMaj, dstMaj)
            matrices = ROTATIONS[key]
            print("")
            print(f"Mapping {colorNames} to {mappedNames} with origin {colorNames[origin]}")
            print(f"Key is {key}")
            print(f"Matrix is one of:")
            for matrix in matrices:
                matrix = np.array(matrix)
                print(f"{matrix}")
                for neighbor in range(4):
                    if neighbor == origin:
                        continue
                    srcEdgeName = colorNames[origin] + colorNames[neighbor]
                    srcEdgeVec  = edges[origin][neighbor]
                    dstEdgeVec  = matrix @ np.array(srcEdgeVec).T
                    dstEdgeName = findEdgeName(dstEdgeVec)
                    assert findEdgeName(srcEdgeVec, doThird=False) == srcEdgeName
                    corDstEdgeName = colorNames[perm[origin]] + \
                                     colorNames[perm[neighbor]]
                    note = ""
                    if dstEdgeName != corDstEdgeName:
                        note = "  (WRONG)"
                    print(f"    {srcEdgeName} {srcEdgeVec} -> {dstEdgeVec} {dstEdgeName} expect {corDstEdgeName}{note}")

