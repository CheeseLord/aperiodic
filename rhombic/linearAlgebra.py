import decimal
import itertools
import numpy as np


def reduce2D(basis):
    v1, v2 = basis
    v1 = np.array(v1)
    v2 = np.array(v2)

    # Use Gaussian lattice reduction.
    while True:
        v1, v2 = sorted([v1, v2], key=np.linalg.norm)
        m = round_(np.dot(v1, v2) / np.dot(v1, v1))
        if m == 0:
            return [v1, v2]
        v2 -= m * v1


def reduce3D(basis):
    v1, v2, v3 = basis
    v1 = np.array(v1)
    v2 = np.array(v2)
    v3 = np.array(v3)

    # Use 3D Gaussian lattice reduction.
    # https://scholarworks.lib.csusb.edu/cgi/viewcontent.cgi?article=2675&context=etd
    while True:
        v1, v2, v3 = sorted([v1, v2, v3], key=np.linalg.norm)

        m12 = round_(np.dot(v1, v2) / np.dot(v1, v1))
        m13 = round_(np.dot(v1, v3) / np.dot(v1, v1))
        m23 = round_(np.dot(v2, v3) / np.dot(v2, v2))
        m = [m12, m13, m23]
        index = np.argmax(np.abs(m))
        if m[index] == 0:
            return [v1, v2, v3]

        if index == 0:
            v2 -= m12 * v1
        elif index == 1:
            v3 -= m13 * v1
        else:
            v3 -= m23 * v2

def makeCanonical(basis):
    reduced = np.array(reduce3D(basis))

    equivalent = []
    for order in itertools.permutations(range(3)):
        for signs in itertools.product([-1, 1], repeat=3):
            newBasis = [list(x[list(order)] * signs) for x in reduced]
            for i in range(3):
                if newBasis[i] < [0, 0, 0]:
                    newBasis[i] = [-x for x in newBasis[i]]
            equivalent.append(sorted(newBasis))

    return min(equivalent)


def round_(x):
    # Python's default rounding can cause infinte loops.
    decimal.getcontext().rounding = decimal.ROUND_HALF_DOWN
    return int(decimal.Decimal(x).to_integral_value())


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    basis = np.random.randint(-50, 51, (3, 3))
    reduced = reduce3D(basis)
    print(*basis)
    print(*reduced)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(*zip(*[
        np.dot(np.array(basis).T, coeff).T
        for coeff in itertools.product(range(-3, 4), repeat=3)
    ]), c='r', s=20)
    ax.scatter(*zip(*[
        np.dot(np.array(reduced).T, coeff).T
        for coeff in itertools.product(range(-3, 4), repeat=3)
    ]), c='b', s=10)
    plt.show()

