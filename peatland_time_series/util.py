import numpy


def power_law(x, a, b):
    return a * numpy.power(x, b)


def inverse_power_law(y, a, b):
    return (y / a) ** (1 / b)
