import math
from itertools import combinations
from ..model.objects import Cicle, Vector2D

def trapezoid_area(cicle1: Cicle, cicle2: Cicle) -> float:

    distance = math.dist(cicle1.center(), cicle2.center())
    tangent_len = math.hypot(distance, cicle1.radius() - cicle2.radius())

    return (cicle1.radius() + cicle2.radius()) * tangent_len / 2

def find_max_area(set1: set, set2: set) -> tuple[float, Cicle, Cicle]:
    max_area = 0
    for s1_point1, s1_point2, s1_point3 in combinations(set1, 3):

        s1_cicle = Cicle(s1_point1, s1_point2, s1_point3)

        for s2_point1, s2_point2, s2_point3 in combinations(set2, 3):
            s2_cicle = Cicle(s2_point1, s2_point2, s2_point3)
            curr_area = trapezoid_area(s1_cicle, s2_cicle)
            if curr_area > max_area:
                max_s1_cicle, max_s2_cicle = s1_cicle, s2_cicle
                max_area = curr_area

    return max_area, max_s1_cicle, max_s2_cicle

# TODO: Переименовать переменные получше
def tangent_coordinates(cicle1: Cicle, cicle2: Cicle) -> tuple[tuple[float, float], tuple[float, float]]:
    small, big = cicle1, cicle2
    if cicle1.radius() > cicle2.radius():
        small, big = big, small

    small_center, big_center = small.center(), big.center()

    distance = math.dist(small_center, big_center)
    distanceX = math.fabs(small_center[0] - big_center[0])

    sigma = math.asin((big.radius() - small.radius()) / distance)
    beta = math.acos(distanceX / distance)

    if small_center[1] > big_center[1]:
        alpha = beta - sigma
    else:
        alpha = beta + sigma
    if small_center[1] > big_center[1] and small_center[0] < big_center[0] \
        or small_center[1] < big_center[1] and small_center[0] > big_center[0]:
        alpha *= -1

    top_point1 = (small_center[0], small_center[1] + small.radius())
    top_point2 = (big_center[0], big_center[1] + big.radius())

    radius_vector1 = Vector2D(small_center, top_point1)
    radius_vector2 = Vector2D(big_center, top_point2)

    radius_vector1.rotate(alpha)
    radius_vector2.rotate(alpha)

    if cicle1.radius() > cicle2.radius():
        return radius_vector2.end(), radius_vector1.end()
    
    return radius_vector1.end(), radius_vector2.end()
