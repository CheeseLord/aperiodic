import os


def cleanup():
    with open('shapes/unknown.txt') as f:
        unknown = [Shape(eval(l)) for l in f.readlines()]
    try:
        os.remove(f'shapes/working/unknown.txt')
    except OSError:
        pass

    for name in os.listdir('shapes/working'):
        with open(f'shapes/working/{name}') as f:
            shapes = [Shape(eval(l)) for l in f.readlines()]
            unknown = [s for s in unknown if s not in shapes]
        with open(f'shapes/{name}', 'a+') as f:
            for shape in shapes:
                f.write(f'{shape}\n')
        os.remove(f'shapes/working/{name}')

    with open('shapes/working/unknown.txt', 'a+') as f:
        for shape in unknown:
            f.write(f'{shape}\n')
    os.replace(f'shapes/working/unknown.txt', f'shapes/unknown.txt')


if __name__ == '__main__':
    cleanup()

