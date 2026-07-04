# Note: pipe output into `less -R` to preserve colors

import sys

from shape import load

_, fname = sys.argv
shapes = load(fname)

try:
    for s in shapes:
        print(s.colorize())
except BrokenPipeError:
    pass
