import exact_cover
import numpy as np
import random

from geometry import DIRECTIONS, orient, getNeighbors


def addLayer(shape, interior):
    interior = set(interior)

    # Find the widgets in the next layer.
    nextLayer = set()
    for widget in interior:
        for w in getNeighbors(widget):
            if w not in interior:
                nextLayer.add(w)

        c, _ = widget
        for d in DIRECTIONS:
            if (c, d) not in interior:
                nextLayer.add((c, d))

        # TODO: Include widgets sharing a non-center corner.
    widgets = {w: i for i, w in enumerate(nextLayer)}

    # Find the subsets that can be covered with a single tile.
    subsets = {}
    for widget in nextLayer:
        for orientation in range(12):
            newShape = orient(shape, widget, orientation)

            # Tiles must not overlap the interior.
            valid = True
            for w in newShape:
                if w in interior:
                    valid = False
                    break
            if not valid:
                continue

            s = [widgets[w] for w in newShape if w in widgets]
            subsets[tuple(sorted(s))] = newShape
    indices = random.sample(list(subsets), len(subsets))

    # Find an exact cover for the widgets.
    arr = np.zeros((len(indices), len(nextLayer)), dtype=bool)
    for i, s in enumerate(indices):
        arr[i, s] = True
    try:
        cover_ = exact_cover.get_exact_cover(arr)
        return [subsets[indices[i]] for i in cover_]
    except exact_cover.error.NoSolution:
        return None


def getLayers(shapes):
    # Map widgets to the tiles that contain them.
    widgets = {}
    for shape in shapes:
        for widget in shape:
            widgets[widget] = shape

    # Use BFS to find the layers.
    layers = []
    completeLayers = 0
    allComplete = True
    seen = set()
    queue = [(((0, 0, 0), (1, 0, 0)), 0)]
    while queue:
        widget, depth = queue[0]
        queue = queue[1:]
        if widget in seen:
            continue

        if allComplete:
            completeLayers = depth
        if depth == len(layers):
            layers.append([])

        shape = widgets[widget]
        layers[-1].append(shape)
        for w in shape:
            seen.add(w)

            for other in getNeighbors(w):
                if other in seen:
                    continue
                elif other in widgets:
                    queue.append((other, depth + 1))
                else:
                    allComplete = False

            c, _ = w
            for d in DIRECTIONS:
                if (c, d) in seen:
                    continue
                elif (c, d) in widgets:
                    queue.append(((c, d), depth + 1))
                else:
                    allComplete = False

            # TODO: Include widgets sharing a non-center corner.

    return layers, completeLayers



if __name__ == '__main__':
    import matplotlib.pyplot as plt

    from display import drawShapes


    with open('gallery/tiling170.txt') as f:
        shapes = [eval(l) for l in f.readlines()]

    layers, completeLayers = getLayers(shapes)
    layers = [sum(x, []) for x in layers]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    drawShapes(ax, layers)
    plt.show()

