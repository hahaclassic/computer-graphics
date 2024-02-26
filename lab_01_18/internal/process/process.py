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

def tangent_coordinates(cicle1: Cicle, cicle2: Cicle) -> tuple[tuple[float, float], tuple[float, float]]:
    if cicle1.radius() > cicle2.radius():
        cicle1, cicle2 = cicle2, cicle1

    center1, center2 = cicle1.center(), cicle2.center()

    distance = math.dist(center1, center2)
    distanceX = math.fabs(center1[0] - center2[0])

    sigma = math.asin((cicle2.radius() - cicle1.radius()) / distance)
    beta = math.acos(distanceX / distance)
    alpha = beta + sigma

    top_point1 = (center1[0], center1[1] + cicle1.radius())
    top_point2 = (center2[0], center2[1] + cicle2.radius())

    radius_vector1 = Vector2D(center1, top_point1)
    radius_vector2 = Vector2D(center2, top_point2)

    radius_vector1.rotate(alpha)
    radius_vector2.rotate(alpha)

    return radius_vector1.end(), radius_vector2.end()
