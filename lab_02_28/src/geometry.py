from PyQt6.QtCore import QPointF
import math
from PyQt6.QtGui import QVector2D

def multiply_vector_by_matrix(vector: QVector2D, matrix: list[list[float]]) -> QVector2D:

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


def angle_between_vectors(vec1: QVector2D, vec2: QVector2D) -> float:
    return math.acos(QVector2D.dotProduct(vec1, vec2) / (vec1.length() * vec2.length()))


def reflect_vector(vector: QVector2D, symmetry_vector: QVector2D) -> QVector2D:

    angle = angle_between_vectors(vector, symmetry_vector)

    return rotate_vector(vector, -angle * 2)

