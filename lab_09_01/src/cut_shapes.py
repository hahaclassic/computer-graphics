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


def get_intersection(polygon_edge: QLine, cutter_edge: QLine,
                     cutter_peak: QPoint) -> tuple[QPoint, bool]:
    visiable1 = is_visiable(polygon_edge.p1(), cutter_edge.p1(),
                            cutter_edge.p2(), cutter_peak)
    visiable2 = is_visiable(polygon_edge.p2(), cutter_edge.p1(),
                            cutter_edge.p2(), cutter_peak)
    if not (visiable1 ^ visiable2):
        return None, False

    normal = get_normal(cutter_edge.p1(), cutter_edge.p2(), cutter_peak)
    vec = QVector2D(polygon_edge.p2() - polygon_edge.p1())
    w = QVector2D(polygon_edge.p1() - cutter_edge.p1())

    t = - QVector2D.dotProduct(w, normal) / QVector2D.dotProduct(vec, normal)

    x = polygon_edge.x1() + vec.x() * t
    y = polygon_edge.y1() + vec.y() * t
    return QPointF(x, y).toPoint(), True


def is_visiable(point: QPoint, peak1: QPoint,
                peak2: QPoint, peak3: QPoint) -> bool:
    n = get_normal(peak1, peak2, peak3)
    return QVector2D.dotProduct(n, QVector2D(point - peak2)) >= 0


def sutherland_hodgman(
        cutter: QPolygon, polygon: QPolygon) -> tuple[QPolygon, bool]:
    cutter = QPolygon(cutter)
    cutter.append(cutter[0])
    cutter.append(cutter[1])

    for i in range(len(cutter) - 2):
        new = QPolygon()
        f = polygon[0]
        if is_visiable(f, cutter[i], cutter[i + 1], cutter[i + 2]):
            new.append(f)

        s = polygon[0]
        for j in range(1, len(polygon)):
            polygon_edge = QLine(s, polygon[j])
            cutter_edge = QLine(cutter[i], cutter[i + 1])
            inter, ok = get_intersection(
                polygon_edge, cutter_edge, cutter[i + 2])
            if ok:
                new.append(inter)
            s = polygon[j]
            if is_visiable(s, cutter[i], cutter[i + 1], cutter[i + 2]):
                new.append(s)

        if not len(new):
            return None, False
        inter, ok = get_intersection(QLine(s, f), QLine(
            cutter[i], cutter[i + 1]), cutter[i + 2])
        if ok:
            new.append(inter)
        polygon = QPolygon(new)

    return polygon, True
