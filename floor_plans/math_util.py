from math import sqrt, hypot
import operator
from functools import reduce

def mean(values):
    return sum(values) / float(len(values))

# return = (x0*x1*x2)^(1/3)
def geometric_mean(values):
    return (reduce(operator.mul, values)) ** (1.0/len(values))

"""
>>> a = [1,2,3]
>>> b = ['a','b','c']
>>> for i,j in zip(a,b):
...     print i, j
...
1 a
2 b
3 c
"""
def weighted_geometric_mean(values, weights):
    assert(len(values) == len(weights))
    n = 1
    for v, w in zip(values, weights):
        n *= v ** w
    return n ** (1.0/sum(weights))

# 方差
def variance(values):
    m = mean(values)
    return sum((v - m) ** 2 for v in values) / len(values)

# 标准差
def stdev(values):
    return sqrt(variance(values))

def dist(a, b):
    return hypot(b[0] - a[0], b[1] - a[1])
