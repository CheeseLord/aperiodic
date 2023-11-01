import os


if __name__ == '__main__':
    for name in os.listdir('shapes/working'):
        if name == 'unknown.txt':
            os.replace(f'shapes/working/{name}', f'shapes/{name}')
        else:
            with open(f'shapes/working/{name}') as f:
                shapes = [eval(l) for l in f.readlines()]
            with open(f'shapes/{name}', 'a+') as f:
                for shape in shapes:
                    f.write(f'{shape}\n')
            os.remove(f'shapes/working/{name}')

