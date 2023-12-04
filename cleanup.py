import os
import re


def cleanup():
    with open('shapes/unknown.txt') as f:
        unknown = [eval(l) for l in f.readlines()]
    try:
        os.remove(f'shapes/working/unknown.txt')
    except OSError:
        pass

    for name in os.listdir('shapes/working'):
        with open(f'shapes/working/{name}') as f:
            shapes = [eval(l) for l in f.readlines()]
            unknown = [s for s in unknown if s not in shapes]
        with open(f'shapes/{name}', 'a+') as f:
            for shape in shapes:
                f.write(f'{shape}\n')
        os.remove(f'shapes/working/{name}')

    with open('shapes/working/unknown.txt', 'a+') as f:
        for shape in unknown:
            f.write(f'{shape}\n')
    os.replace(f'shapes/working/unknown.txt', f'shapes/unknown.txt')


def correct():
    seen = set()

    for base in ['invalid-dfs', 'invalid-cover', 'periodic']:
        names = [x for x in os.listdir('shapes') if x.startswith(base)]
        names = sorted(names,
            key=lambda x: int(re.match('[^\d]*(\d+)[^\d]*', x).groups()[0])
        )
        for name in names:
            with open(f'shapes/{name}') as f:
                shapes = [eval(l) for l in f.readlines()]
            for shape in shapes:
                t = tuple(shape)
                if t in seen:
                    continue
                with open(f'shapes/working/{name}', 'a+') as f:
                    f.write(f'{shape}\n')
                seen.add(t)
    with open(f'shapes/allShapes.txt') as f:
        shapes = [eval(l) for l in f.readlines()]
    for shape in shapes:
        t = tuple(shape)
        if t in seen:
            continue
        with open(f'shapes/working/unknown.txt', 'a+') as f:
            f.write(f'{shape}\n')
        seen.add(t)


if __name__ == '__main__':
    cleanup()

