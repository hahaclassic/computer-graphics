from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QVector2D
import math

def multiply_vector_by_matrix(vector: QVector2D,
                              matrix: list[list[float]]) -> QVector2D:

    x = matrix[0][0] * vector.x() + matrix[0][1] * vector.y()
    y = matrix[1][0] * vector.x() + matrix[1][1] * vector.y()

    return QVector2D(x, y)

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
