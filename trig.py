import matplotlib.pyplot as plt
import math
import numpy

xs = numpy.arange(-360, 360, 1)

def x1(x):
    return x+90
def x2(x):
    return x
def x3(x):
    return 90-x

def y1(x):
    return math.sin(x)
def y2(x):
    return math.sin(x)
def y3(x):
    return math.tan(x)


y1 = [y1(math.radians(v)) for v in [x1(x) for x in xs]]
y2 = [y2(math.radians(v)) for v in [x2(x) for x in xs]]
y3 = [y3(math.radians(v)) for v in [x3(x) for x in xs]]


plt.figure()
# plt.plot(xs, y1, label='sin(x+90)')
# plt.plot(xs, y2, label='sin(x)')
plt.plot(xs, y3, label='tan(90-x)')

plt.legend()
plt.xticks(numpy.arange(-360, 361, 90))
plt.grid(True, linestyle='--')
plt.show()

