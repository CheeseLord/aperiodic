from widget import Widget
from shape import Shape


def generateAllShapes(n):
    if n == 1:
        return [Shape([(0, 0, 0)])]

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
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('numWidgets')
    args = parser.parse_args()
    numWidgets = int(args.numWidgets)

    for i in range(4, numWidgets + 1):
        for shape in generateAllShapes(i):
            shape.save('shapes/allShapes.txt')

