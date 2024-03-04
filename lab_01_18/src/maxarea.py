import math
from itertools import combinations
from src.objects import Cicle, Vector2D

### TODO: Переписать через классы qt

def trapezoid_area(cicle1: Cicle, cicle2: Cicle) -> float:

    distance = math.dist(cicle1.center(), cicle2.center())
    tangent_len = math.hypot(distance, cicle1.radius() - cicle2.radius())

    return (cicle1.radius() + cicle2.radius()) * tangent_len / 2


def find_max_area(set1: set, set2: set) -> tuple[float, Cicle, Cicle]:
    max_s1_cicle, max_s2_cicle = None, None
    max_area = -math.inf

    for s1_point1, s1_point2, s1_point3 in combinations(set1, 3):

        s1_cicle = Cicle(s1_point1, s1_point2, s1_point3)
        if not s1_cicle.is_valid():
            continue

        for s2_point1, s2_point2, s2_point3 in combinations(set2, 3):

            s2_cicle = Cicle(s2_point1, s2_point2, s2_point3)
            if not s2_cicle.is_valid() or \
                s2_cicle.centers_distance(s1_cicle) <= math.fabs(s1_cicle.radius() - s2_cicle.radius()):
                continue

            curr_area = trapezoid_area(s1_cicle, s2_cicle)
            if curr_area > max_area:
                max_s1_cicle, max_s2_cicle = s1_cicle, s2_cicle
                max_area = curr_area

    return max_area, max_s1_cicle, max_s2_cicle


def find_rotate_angle(cicle1: Cicle, cicle2: Cicle) -> float:
    small, big = cicle1, cicle2
    if small.radius() > big.radius():
        small, big = big, small

    small_center, big_center = small.center(), big.center()

    distance = math.dist(small_center, big_center)
    distance_x = math.fabs(small_center[0] - big_center[0])

    sigma = math.asin((big.radius() - small.radius()) / distance)
    beta = math.acos(distance_x / distance)

    if small_center[1] > big_center[1]:
        alpha = beta - sigma  # If the small circle is located above the big one
    else:
        alpha = beta + sigma
    
    # If a small circle is 2 or 4 quarters of a relatively big one
    if small_center[1] > big_center[1] and small_center[0] < big_center[0] \
        or small_center[1] < big_center[1] and small_center[0] > big_center[0]:
        alpha *= -1

    return alpha

def tangent_coordinates(cicle1: Cicle, cicle2: Cicle) -> tuple[tuple[float, float], tuple[float, float]]:
    alpha = find_rotate_angle(cicle1, cicle2)
    center1, center2 = cicle1.center(), cicle2.center()

    # The upper points of the circles
    top_point1 = (center1[0], center1[1] + cicle1.radius())
    top_point2 = (center2[0], center2[1] + cicle2.radius())

    radius_vector1 = Vector2D(center1, top_point1)
    radius_vector2 = Vector2D(center2, top_point2)

    radius_vector1.rotate(alpha)
    radius_vector2.rotate(alpha)
    
    return radius_vector1.end(), radius_vector2.end()
