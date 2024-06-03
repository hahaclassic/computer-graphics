from math import cos, sin, sqrt, exp, fabs


def func1(x: float, z: float) -> float:
    return cos(x) * sin(z)


def func2(x: float, z: float) -> float:
    return exp(cos(x) + sin(z))


def func3(x: float, z: float) -> float:
    return sqrt(fabs(x ** 2 - z ** 2))


def func4(x: float, z: float) -> float:
    return cos(x * z)
