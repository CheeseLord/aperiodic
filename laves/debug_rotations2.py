import numpy as np

from widget import Widget, getFirstWidgets, COLOR_NAMES
from shape import Shape, ROTATIONS


# FIXME: I think the premise of this script is wrong.
# You can't make a red node blue by rotating it about the origin by some
# particular matrix, because the red node could _be_ the origin. You make it
# blue by translating it to a blue location... but in order to preserve the
# orientation of everything else, you have to rotate the _rest_ of the nodes
# about the translated one by a red->blue conversion matrix.


def nextGeneration(soFar):
    s = set([])
    for w in soFar:
        s.update(w.neighbors)
    s.difference_update(soFar)
    return sorted(s)

gen0 = [Widget((0, 0, 0))]
gen1 = nextGeneration(gen0)
gen2 = nextGeneration(gen0 + gen1)

print(gen0)
print("")
print(gen1)
print("")
print(gen2)
print("")

for startWidget in gen0 + [None] + gen1 + [None] + gen2:
    if startWidget is None:
        print("")
        continue
    startColor = startWidget.colorIndex
    for targetColor in range(4):
        if targetColor == startColor:
            continue
        for rotation in [0, 1]:
            matrix = np.array(ROTATIONS[(startColor, targetColor)][rotation])
            unscaled = np.dot(matrix, np.array(startWidget.center).T).T
            scaled = np.round(unscaled / 3).astype(int)
            endWidget = Widget(scaled)
            roundNote = ""
            if np.linalg.norm(3*scaled - unscaled) > 0.01:
                roundNote = " (ROUND FAIL)"
            colorNote = " (WRONG COLOR)"
            try:
                if endWidget.colorIndex == targetColor:
                    colorNote = ""
            except:
                pass
            print(f"Rotate {startWidget} ({COLOR_NAMES[startColor]} -> "
                    f"{COLOR_NAMES[targetColor]} r{rotation})  ==>  "
                    f"{endWidget}{colorNote}{roundNote}")

