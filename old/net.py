from matplotlib.patches import Polygon
import matplotlib.pyplot as plt
import numpy as np
from numpy.linalg import norm


def normalize(face):
    numSides = len(face)
    pos = np.array([0, 0], dtype=float)
    angle = 0
    poly = [pos]
    for i in range(numSides):
        v = face[(i + 1) % numSides] - face[i]
        w = face[(i + 2) % numSides] - face[(i + 1) % numSides]
        r = norm(v)
        pos = pos + [r * np.cos(angle), r * np.sin(angle)]
        angle += np.arccos(np.dot(v, w) / (r * norm(w)))
        poly.append(pos)
    poly[-1] = [0, 0]
    return np.array(poly)


def pack(face, n):
    normalized = normalize(face)
    v = normalized[1]
    w = normalized[-2]
    angle = np.arccos(np.dot(v, w) / (norm(v) * norm(w)))
    faces = []
    for i in range(n):
        mat = np.array([
            [np.cos(i * angle), -np.sin(i * angle)],
            [np.sin(i * angle), np.cos(i * angle)],
        ])
        faces.append(np.dot(mat, normalized.T).T)
    return faces


if __name__ == '__main__':
    octBig = np.array([
        [0, 0, 0],
        [0, 1, 1],
        [2 / 3, 2 / 3, 4 / 3],
        [1, 0, 1],
    ])
    octSmall = np.array([
        [0, 0, 2],
        [-2 / 3, 2 / 3, 4 / 3],
        [0, 1, 1],
        [2 / 3, 2 / 3, 4 / 3],
    ])
    tetBig = np.array([
        [0, 0, 0],
        [1, 1, 0],
        [4 / 3, 2 / 3, 2 / 3],
        [1, 0, 1],
    ])
    tetSmall = np.array([
        [1, 1, 1],
        [2 / 3, 4 / 3, 2 / 3],
        [1, 1, 0],
        [4 / 3, 2 / 3, 2 / 3],
    ])

    ax = plt.gca()
    ax.set_aspect('equal')
    ax.set_xlim(-4, 3)
    ax.set_ylim(-4, 3)

    for shape in pack(octBig, 4):
        transformed = shape - normalize(shape)[2] + [0, -1]
        poly = Polygon(transformed)
        poly.set_ec('b')
        poly.set_fc('none')
        ax.add_patch(poly)
    for shape in pack(octSmall, 4):
        transformed = -shape + normalize(shape)[1] + [0, -1]
        poly = Polygon(transformed)
        poly.set_ec('b')
        poly.set_fc('none')
        ax.add_patch(poly)

    for shape in pack(tetBig, 3):
        transformed = shape - normalize(shape)[2] + [0, 1]
        poly = Polygon(transformed)
        poly.set_ec('r')
        poly.set_fc('none')
        ax.add_patch(poly)
    for shape in pack(tetSmall, 3):
        transformed = -shape + normalize(shape)[1] + [0, 1]
        poly = Polygon(transformed)
        poly.set_ec('r')
        poly.set_fc('none')
        ax.add_patch(poly)

    plt.tight_layout()
    plt.show()

