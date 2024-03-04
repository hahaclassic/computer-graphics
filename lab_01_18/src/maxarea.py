import math
from itertools import combinations
from src.cicle import Cicle, QPointF
from PyQt6.QtGui import QVector2D

def trapezoid_area(cicle1: Cicle, cicle2: Cicle) -> float:

    distance = cicle1.centers_distance(cicle2)
    tangent_len = math.hypot(distance, cicle1.radius() - cicle2.radius())

    return (cicle1.radius() + cicle2.radius()) * tangent_len / 2


def find_max_area(set1: list[QPointF], set2: list[QPointF]) -> tuple[float, Cicle, Cicle]:
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

    distance = small.centers_distance(big)
    distance_x = math.fabs(small_center.x() - big_center.x())

    sigma = math.asin((big.radius() - small.radius()) / distance)
    beta = math.acos(distance_x / distance)

    if small_center.y() > big_center.y():
        alpha = beta - sigma  # If the small circle is located above the big one
    else:
        alpha = beta + sigma
    
    # If a small circle is 2 or 4 quarters of a relatively big one
    if small_center.y() > big_center.y() and small_center.x() < big_center.x() \
        or small_center.y() < big_center.y() and small_center.x() > big_center.x():
        alpha *= -1

    return alpha


def rotate_vector(vector: QVector2D, angle: float) -> None:
  
    x = math.cos(angle) * vector.x() - math.sin(angle) * vector.y()
    y = math.sin(angle) * vector.x() + math.cos(angle) * vector.y()
    vector.setX(x)
    vector.setY(y)

def tangent_coordinates(cicle1: Cicle, cicle2: Cicle) -> tuple[QPointF, QPointF]:
    alpha = find_rotate_angle(cicle1, cicle2)
    center1, center2 = cicle1.center(), cicle2.center()

    # The upper points of the circles
    top_point1 = QPointF(center1.x(), center1.y() + cicle1.radius())
    top_point2 = QPointF(center2.x(), center2.y() + cicle2.radius())

    radius_vector1 = QVector2D(top_point1 - center1)
    radius_vector2 = QVector2D(top_point2 - center2)

    rotate_vector(radius_vector1, alpha)
    rotate_vector(radius_vector2, alpha)
    
    tangent_p1 = radius_vector1.toPointF() + center1
    tangent_p2 = radius_vector2.toPointF() + center2
    
    return tangent_p1, tangent_p2
