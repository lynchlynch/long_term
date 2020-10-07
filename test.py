import numpy
from numba import njit
import timeit

def do_trig(x, y):
    z = numpy.empty_like(x)
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            z[i, j] = numpy.sin(x[i, j]**2) + numpy.cos(y[i, j])
    return z

x = numpy.random.random((1000, 1000))
y = numpy.random.random((1000, 1000))

# do_trig(x, y)
t1 = timeit.timeit('do_trig(x, y)','from __main__ import do_trig')
print(t1)