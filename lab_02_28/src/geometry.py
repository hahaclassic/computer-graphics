from PyQt6.QtCore import QPointF
import math
from PyQt6.QtGui import QVector2D
from PyQt6.QtWidgets import QGraphicsLineItem
from typing import Callable

NUM_OF_POINTS_OF_ELLIPSE = 100


def multiply_vector_by_matrix(vector: QVector2D,
                              matrix: list[list[float]]) -> QVector2D:

    x = matrix[0][0] * vector.x() + matrix[0][1] * vector.y()
    y = matrix[1][0] * vector.x() + matrix[1][1] * vector.y()

    return QVector2D(x, y)


def scale_point(point: QPointF, center: QPointF, ratio: float) -> QPointF:
    scale_matrix = [
        [ratio, 0],
        [0, ratio]
    ]
    vector = QVector2D(point - center)
    scaled_vec = multiply_vector_by_matrix(vector, scale_matrix)

    return scaled_vec.toPointF() + center


def rotate_vector(vector: QVector2D, angle: float) -> QVector2D:
    rotate_matrix = [
        [math.cos(angle), -math.sin(angle)],
        [math.sin(angle), math.cos(angle)]
    ]
    return multiply_vector_by_matrix(vector, rotate_matrix)


def rotate_point(point: QPointF, center: QPointF, angle: float) -> QPointF:
    vector = QVector2D(point - center)
    rotated_vec = rotate_vector(vector, angle)

    return rotated_vec.toPointF() + center


def move_point(point: QPointF, dx: float, dy: float) -> QPointF:
    return point + QPointF(dx, dy)


def pseudoscalar_product(vec1: QVector2D, vec2: QVector2D) -> float:
    return vec1.x() * vec2.y() - vec1.y() * vec2.x()


# Возвращает угол, на который надо повернуть вектор vec, чтобы 
# vec и base_vec оказались сонаправленными.
#
# returns angle > 0 -> поворот против часовой
#         angle < 0 -> поворот по часовой
#
# Угол вычисляется через скалярное произведение, т.к. необходимо 
# учесть тупые углы тоже.
def angle_between_vectors(vec: QVector2D, base_vec: QVector2D) -> float:
    prod = pseudoscalar_product(vec, base_vec)
    cos = QVector2D.dotProduct(vec, base_vec) / (vec.length() * base_vec.length())
    angle = math.acos(cos)
    if prod < 0:
        return -angle
    return angle
    

def reflect_vector(vector: QVector2D, symmetry_vector: QVector2D) -> QVector2D:
    angle = angle_between_vectors(vector, symmetry_vector)
    return rotate_vector(vector, angle * 2)


def create_ellipse_functions(center: QPointF, top_point: QPointF,
                             left_point: QPointF) -> tuple[Callable[[float], float], Callable[[float], float]]:

    center_to_left = center - left_point
    top_to_center = top_point - center

    def x_t(t: float):
        return center_to_left.x() * math.cos(t) + top_to_center.x() * \
            math.sin(t) + center.x()

    def y_t(t: float):
        return center_to_left.y() * math.cos(t) + top_to_center.y() * \
            math.sin(t) + center.y()

    return x_t, y_t


# generate_line_items() returns a list of lines connecting the points of the ellipse.
# start, end - the initial and final value of the parameter t for the
# parametric equation of the ellipse.
def generate_line_items(func_x_t: Callable[[float], float], func_y_t: Callable[[float], float],
                        start: float, end: float) -> list[QGraphicsLineItem]:

    items_list = []

    step = (end - start) / NUM_OF_POINTS_OF_ELLIPSE
    last_x, last_y = func_x_t(start), func_y_t(start)
    start += step

    while start < end:

        x, y = func_x_t(start), func_y_t(start)
        items_list.append(QGraphicsLineItem(last_x, last_y, x, y))

        last_x, last_y = x, y
        start += step

    return items_list


def build_ellipse(center: QPointF, top_point: QPointF,
                  left_point: QPointF) -> list[QGraphicsLineItem]:

    func_x_t, func_y_t = create_ellipse_functions(
        center, top_point, left_point)

    start, end = 0, 2 * math.pi

    return generate_line_items(func_x_t, func_y_t, start, end)


def build_left_half_ellipse(center: QPointF, top_point: QPointF,
                            left_point: QPointF) -> list[QGraphicsLineItem]:

    func_x_t, func_y_t = create_ellipse_functions(
        center, top_point, left_point)

    start, end = math.pi / 2, 3.0 / 2.0 * math.pi

    return generate_line_items(func_x_t, func_y_t, start, end)
