import itertools
import numpy as np


def translate(shapes, offset):
    other = np.array(shapes)
    other[:, :, 0] -= offset
    other = [
        tuple(
            tuple(
                tuple(x) for x in widget
            ) for widget in shape
        ) for shape in other
    ]
    return other


def randomTransformation(shapes):
    offset = -np.array(shapes)[
        np.random.randint(len(shapes)),
        np.random.randint(len(shapes[0])),
        0,
    ]
    other = translate(shapes, offset)

    # FIXME: Handle rotation.

    return other


def overlap(shapes, other):
    shapes = {tuple(shape) for shape in shapes}
    other = {tuple(shape) for shape in other}
    return list(shapes & other)


if __name__ == '__main__':
    import argparse
    import matplotlib.pyplot as plt

    from display import drawShapes, drawHull


    parser = argparse.ArgumentParser()
    parser.add_argument('shapeFile', nargs='?')
    args = parser.parse_args()

    with open(args.shapeFile) as f:
        shapes = [eval(l) for l in f.readlines()]

    while True:
        other = randomTransformation(shapes)
        thing = overlap(shapes, other)
        if len(thing) >= 10:
            break
    print(len(shapes), len(thing))
    print((np.array(other) - shapes)[0, 0, 0])

    """
    other = translate(shapes, [0, 1, 1])
    other = translate(shapes, [4, 0, 0])
    other = translate(shapes, [0, 0, 2])
    thing = overlap(shapes, other)
    print(len(shapes), len(thing))
    """

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # drawShapes(ax, thing)

    drawHull(ax, shapes, 'r')
    drawHull(ax, other, 'g')
    drawHull(ax, thing, 'b')

    plt.show()

