from PyQt6.QtCore import QLine, QPoint, QPointF
from PyQt6.QtGui import QPolygon, QVector2D


def pseudoscalar_product(vec1: QVector2D, vec2: QVector2D) -> float:
    return vec1.x() * vec2.y() - vec1.y() * vec2.x()


def is_polygon_convex(polygon: QPolygon) -> bool:
    if len(polygon) < 3:
        return False
    num_positive, num_negative = 0, 0

    for i in range(len(polygon)):
        edge1 = QVector2D(polygon[i - 1] - polygon[i - 2])
        edge2 = QVector2D(polygon[i] - polygon[i - 1])
        prod = pseudoscalar_product(edge1, edge2)
        if prod > 0:
            num_positive += 1
        elif prod < 0:
            num_negative += 1

    return not (num_positive > 0 and num_negative > 0) \
        and num_positive + num_negative != 0


def get_normal(point1: QPoint, point2: QPoint, point3: QPoint) -> QVector2D:
    vector = QVector2D(point2 - point1)
    normal = QVector2D(vector.y(), -vector.x())

    if QVector2D.dotProduct(QVector2D(point3 - point2), normal) < 0:
        normal *= -1

    return normal.normalized()


def update_range(w_scalar: float, d_scalar: float,
                 t_range: list[float]) -> bool:
    if d_scalar == 0:
        return w_scalar >= 0

    t = - w_scalar / d_scalar
    if d_scalar > 0:
        if t <= 1:
            t_range[0] = max(t_range[0], t)
        else:
            return False
    elif d_scalar < 0:
        if t >= 0:
            t_range[1] = min(t_range[1], t)
        else:
            return False

    return True


def cyrus_beck(polygon: QPolygon, segment: QLine) -> tuple[QLine, bool]:
    t_range = [0.0, 1.0]
    point1, point2 = segment.p1(), segment.p2()
    d = QVector2D(point2 - point1)

    for i in range(-2, len(polygon) - 2):
        normal = get_normal(polygon[i], polygon[i + 1], polygon[i + 2])

        w = QVector2D(point1 - polygon[i])
        d_scalar = QVector2D.dotProduct(d, normal)
        w_scalar = QVector2D.dotProduct(w, normal)

        ok = update_range(w_scalar, d_scalar, t_range)
        if not ok or t_range[0] > t_range[1]:
            return QLine(), False

    res_point1 = QPointF(point1.x() + d.x() * t_range[0],
        point1.y() + d.y() * t_range[0]).toPoint()
    res_point2 = QPointF(point1.x() + d.x() * t_range[1],
        point1.y() + d.y() * t_range[1]).toPoint()
    return QLine(res_point1, res_point2), True
