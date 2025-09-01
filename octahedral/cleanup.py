import os

from shape import load


def cleanup():
    unknown = load('shapes/unknown.txt')
    try:
        os.remove(f'shapes/working/unknown.txt')
    except OSError:
        pass

    for name in os.listdir('shapes/working'):
        shapes = load(f'shapes/working/{name}')
        for shape in shapes:
            shape.save(f'shapes/{name}')

        unknown = [s for s in unknown if s not in shapes]
        os.remove(f'shapes/working/{name}')

    for shape in unknown:
        shape.save('shapes/working/unknown.txt')

    os.replace(f'shapes/working/unknown.txt', f'shapes/unknown.txt')


if __name__ == '__main__':
    cleanup()

