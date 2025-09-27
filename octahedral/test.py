import matplotlib.pyplot as plt

from satisfy import cover
from shape import Shape, load
from display import drawShapes, getAxis


if __name__ == '__main__':
    shapes = load('shapes/unknown.txt')
    tiling = cover(shapes[0], 100)
    ax = getAxis()
    drawShapes(ax, tiling)
    plt.show()

