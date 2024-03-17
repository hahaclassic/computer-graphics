import math
from itertools import combinations
from PyQt6.QtGui import QVector2D
from src.circle import Circle, QPointF

def trapezoid_area(circle1: Circle, circle2: Circle) -> float:

    distance = circle1.centers_distance(circle2)
    tangent_len = math.hypot(distance, circle1.radius() - circle2.radius())

    return (circle1.radius() + circle2.radius()) * tangent_len / 2


def find_max_area(set1: list[QPointF], set2: list[QPointF]) -> tuple[float, Circle, Circle]:
    max_s1_circle, max_s2_circle = None, None
    max_area = -math.inf

    for s1_point1, s1_point2, s1_point3 in combinations(set1, 3):

        s1_circle = Circle(s1_point1, s1_point2, s1_point3)
        if not s1_circle.is_valid():
            continue

        for s2_point1, s2_point2, s2_point3 in combinations(set2, 3):

            s2_circle = Circle(s2_point1, s2_point2, s2_point3)
            if not s2_circle.is_valid() or \
                s2_circle.centers_distance(s1_circle) <= math.fabs(s1_circle.radius() - s2_circle.radius()):
                continue

            curr_area = trapezoid_area(s1_circle, s2_circle)
            if curr_area > max_area:
                max_s1_circle, max_s2_circle = s1_circle, s2_circle
                max_area = curr_area

    return max_area, max_s1_circle, max_s2_circle


def find_rotate_angle(circle1: Circle, circle2: Circle) -> float:
    small, big = circle1, circle2
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

def tangent_coordinates(circle1: Circle, circle2: Circle) -> tuple[QPointF, QPointF]:
    alpha = find_rotate_angle(circle1, circle2)
    center1, center2 = circle1.center(), circle2.center()

    # The upper points of the circles
    top_point1 = QPointF(0, circle1.radius())
    top_point2 = QPointF(0, circle2.radius())

    radius_vector1 = QVector2D(top_point1)
    radius_vector2 = QVector2D(top_point2)

    rotate_vector(radius_vector1, alpha)
    rotate_vector(radius_vector2, alpha)
    
    tangent_p1 = radius_vector1.toPointF() + center1
    tangent_p2 = radius_vector2.toPointF() + center2
    
    return tangent_p1, tangent_p2
