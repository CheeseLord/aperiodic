from widget import Widget, getFirstWidgets
from shape import Shape, load

def doTest(coords, target):
    print(f"Shape is:")
    for coord in coords:
        widget = Widget(coord)
        print(f"    {widget}  | neighbors: {widget.neighbors}")
    print("")
    s = Shape(coords)
    s.orient(Widget(target), 0, 0)

if True:
    doTest([(-1,  0,  1), ( 0,  1, -1)], ( 0,  0,  0)) # (Y,G)->R: FAILS
   #doTest([(-1,  0,  1), ( 0,  1, -1)], ( 1, -1,  0)) # (Y,G)->B: FAILS
   #doTest([(-1,  0,  1), ( 0,  1, -1)], (-1,  0,  1)) # (Y,G)->Y: works
   #doTest([(-1,  0,  1), ( 0,  1, -1)], ( 0,  1, -1)) # (Y,G)->G: works

   #doTest([( 0,  0,  0), ( 1, -1,  0)], ( 0,  1, -1)) # (R,B)->G: works (!)



# Scratch from before, can probably be ignored

#widgets = [(-1, 0, 1), (0, 1, -1)]
##widgets = [(-1, 0, 1), (-2, -1, 1)]
##widgets = [(0, 0, 0), (3, 1, 2)]
#
#print(widgets)
#print(str(Widget(widgets[0]).neighbors))
#print(str(Widget(widgets[1]).neighbors))
#s = Shape(widgets)
#
#s.orient(Widget(2, 3, 1), 0, 0)
#
##s.orient(Widget(0, 0, 0), 1, 0)
##s.orient(Widget(2, 2, 2), 1, 0)
#
##s.orient(Widget(0, 1, 1), 1, 0) # Works
##s.orient(Widget(1, 0, 1), 1, 0) # Works
#s.orient(Widget(0, 0, 0), 1, 0) # Fails
##s.orient(Widget(1, 1, 0), 1, 0) # Fails
#
##s.orient(Widget(-1, 1, -2), 1, 0)
