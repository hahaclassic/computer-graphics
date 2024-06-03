from PyQt6.QtWidgets import QGraphicsView
from PyQt6.QtCore import QPointF, QPoint, QLineF
from typing import Callable
from PyQt6.QtGui import QMatrix4x4, QVector3D


class Interval:
    def __init__(self, start: float, end: float, step: float) -> None:
        self.start = start
        self.end = end
        self.step = step


TOP = 1
BOTTOM = -1
INVISIBLE = 0


class Horizon:
    def __init__(self, view: QGraphicsView) -> None:
        self.view = view
        self.top = [0] * self.view.width()
        self.bottom = [self.view.height()] * self.view.width()

    def visible(self, point: QPointF) -> int:
        p = self.view.mapFromScene(point)
        if p.x() >= len(self.bottom):
            return None
        if p.y() <= self.bottom[p.x()]:
            return BOTTOM
        elif p.y() >= self.top[p.x()]:
            return TOP
        return INVISIBLE

    def update(self, line: QLineF):
        p1, p2 = self.view.mapFromScene(
            line.p1()), self.view.mapFromScene(line.p2())
        x1, y1, x2, y2 = p1.x(), p1.y(), p2.x(), p2.y()
        if (x2 - x1 == 0):
            self.top[x2] = max(self.top[x2], y2)
            self.bottom[x2] = min(self.bottom[x2], y2)
            return

        m = (y2 - y1) / (x2 - x1)
        for x in range(x1, x2 + 1):
            y = round(m * (x - x1) + y1)
            self.top[x] = max(self.top[x], y)
            self.bottom[x] = min(self.bottom[x], y)

    def __intersection(self, point1: QPointF, point2: QPointF,
                       horizon: list[int]) -> QPointF:
        p1, p2 = self.view.mapFromScene(point1), self.view.mapFromScene(point2)
        x1, y1, x2, y2 = p1.x(), p1.y(), p2.x(), p2.y()
        dx, dy = x2 - x1, y2 - y1
        diff_horizon = horizon[x2] - horizon[x1]
        xi, yi = x2, horizon[x2] # dx == 0

        if y1 == horizon[x1] and y2 == horizon[x2]:
            xi, yi = x1, y1
        elif dx != 0:
            m = dy / dx
            xi = x1 - round(dx * (y1 - horizon[x1]) / (dy - diff_horizon))
            yi = round((xi - x1) * m + y1)

        return self.view.mapToScene(QPoint(xi, yi))

    def top_intersection(self, point1: QPointF, point2: QPointF) -> QPointF:
        return self.__intersection(point1, point2, self.top)

    def bottom_intersection(self, point1: QPointF, point2: QPointF) -> QPointF:
        return self.__intersection(point1, point2, self.bottom)


def horizon_method(view: QGraphicsView, x_interval: Interval, z_interval: Interval,
        func: Callable[[float, float], float], transform: QMatrix4x4) -> list[QLineF]:
    result_lines: list[QLineF] = []
    horizon = Horizon(view)
    left_side_point, right_side_point = None, None

    z = z_interval.end
    while z >= z_interval.start - z_interval.step / 2:
        prev_vec = QVector3D(x_interval.start, func(x_interval.start, z), z)
        prev = transform.map(prev_vec).toPointF()
        flag_prev = horizon.visible(prev)
        if flag_prev is None:
            return None
        left_side_point = update_side(result_lines, prev, left_side_point)

        x = x_interval.start
        while x <= x_interval.end + x_interval.step / 2:
            curr_vec = QVector3D(x, func(x, z), z)
            curr = transform.map(curr_vec).toPointF()

            flag_curr = horizon.visible(curr)
            if flag_curr is None:
                return None
            add_lines(horizon, result_lines, 
                      [flag_prev, flag_curr], [prev, curr])
            prev = curr
            flag_prev = flag_curr
            x += x_interval.step

        right_side_point = update_side(result_lines, prev, right_side_point)
        z -= z_interval.step

    return result_lines


def update_side(lines: list[QLineF], curr_side_point: QPointF,
                prev_side_point: QPointF) -> QLineF:
    if prev_side_point is not None:
        lines.append(QLineF(prev_side_point, curr_side_point))
    return curr_side_point


def add_lines(horizon: Horizon, lines: list[QLineF],
              flags: list[int], points: list[QPointF]) -> None:
    flag_prev, flag_curr = flags[0], flags[1]
    prev, curr = points[0], points[1]

    if flag_prev != flag_curr:
        if flag_prev == TOP or flag_curr == TOP:
            top_intersection = horizon.top_intersection(prev, curr)
        if flag_prev == BOTTOM or flag_curr == BOTTOM:
            bottom_intersection = horizon.bottom_intersection(prev, curr)

        if flag_prev == BOTTOM:
            add_line(horizon, lines, QLineF(prev, bottom_intersection))
        if flag_curr == BOTTOM:
            add_line(horizon, lines, QLineF(bottom_intersection, curr))
        if flag_prev == TOP:
            add_line(horizon, lines, QLineF(prev, top_intersection))
        if flag_curr == TOP:
            add_line(horizon, lines, QLineF(top_intersection, curr))

    elif flag_curr != INVISIBLE:
        add_line(horizon, lines, QLineF(prev, curr))


def add_line(horizon: Horizon, lines: list[QLineF], line: QLineF) -> None:
    lines.append(line)
    horizon.update(line)