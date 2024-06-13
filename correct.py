import os
import re


def correct():
    seen = set()

    for base in ['invalid-dfs', 'invalid-cover', 'invalid-satisfy', 'periodic']:
        names = [x for x in os.listdir('shapes') if x.startswith(base)]
        names = sorted(names,
            key=lambda x: int(re.match('[^\d]*(\d+)[^\d]*', x).groups()[0])
        )
        for name in names:
            with open(f'shapes/{name}') as f:
                shapes = [Shape(eval(l)) for l in f.readlines()]
            for shape in shapes:
                if shape in seen:
                    continue
                with open(f'shapes/working/{name}', 'a+') as f:
                    f.write(f'{shape}\n')
                seen.add(shape)
    with open(f'shapes/allShapes.txt') as f:
        shapes = [Shape(eval(l)) for l in f.readlines()]
    for shape in shapes:
        if shape in seen:
            continue
        with open(f'shapes/working/unknown.txt', 'a+') as f:
            f.write(f'{shape}\n')
        seen.add(shape)

    for name in os.listdir('shapes/working'):
        os.replace(f'shapes/working/{name}', f'shapes/{name}')


if __name__ == '__main__':
    correct()

