from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtCore import QPointF, QPoint, QLineF
from typing import Callable
from PyQt6.QtGui import QMatrix4x4, QVector3D

class Interval:
    def __init__(self, start: float, end: float, step: float) -> None:
        self.start = start
        self.end = end
        self.step = step


class Rotation:
    def __init__(self, angle_x: float, angle_y: float, angle_z: float) -> None:
        """angles in degrees"""
        self.angle_x = angle_x
        self.angle_y = angle_y
        self.angle_z = angle_z


class Transformation:
    def __init__(self, rotation: Rotation, scale_ratio: float) -> None:
        self.rotation = rotation
        self.scale_ratio = scale_ratio

    def rotate_vector(self, vector: QVector3D) -> QVector3D:
        transform = QMatrix4x4()
        transform.rotate(self.rotation.angle_x, 1, 0, 0)
        transform.rotate(self.rotation.angle_y, 0, 1, 0)
        transform.rotate(self.rotation.angle_z, 0, 0, 1)

        return transform.map(vector)

    def scale_vector(self, vector: QVector3D) -> QVector3D:
        transform = QMatrix4x4()
        transform.scale(self.scale_ratio)
        return transform.map(vector)
 
    def transform_vector(self, vector: QVector3D) -> QVector3D:
        vector = self.rotate_vector(vector)
        return self.scale_vector(vector)

TOP = 1
BOTTOM = -1
INVISIBLE = 0

class Horizon:
    def __init__(self, scene: QGraphicsScene) -> None:
        self.scene = scene
        self.view = scene.views()[0]
        self.top = [0] * self.view.width()
        self.bottom = [self.view.height()] * self.view.width()

    def visible(self, point: QPointF) -> int:
        p = self.view.mapFromScene(point)
        if p.y() <= self.bottom[p.x()]:
            return BOTTOM
        elif p.y() >= self.top[p.x()]:
            return TOP
        return INVISIBLE
    
    def update(self, line: QLineF):
        p1, p2 = self.view.mapFromScene(line.p1()), self.view.mapFromScene(line.p2())
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

    def __intersection(self, point1: QPointF, point2: QPointF, horizon: list[int]) -> QPointF:
        p1, p2 = self.view.mapFromScene(point1), self.view.mapFromScene(point2)
        x1, y1, x2, y2 = p1.x(), p1.y(), p2.x(), p2.y()
        dx = x2 - x1
        dyc = y2 - y1
        dyp = horizon[x2] - horizon[x1]
        if dx == 0:
            xi = x2
            yi = horizon[x2]
            return self.view.mapToScene(QPoint(xi, yi))
        
        if y1 == horizon[x1] and y2 == horizon[x2]:
            return self.view.mapToScene(QPoint(x1, y1))
        
        m = dyc / dx
        xi = x1 - round(dx * (y1 - horizon[x1]) / (dyc - dyp))
        yi = round((xi - x1) * m + y1)
        return self.view.mapToScene(QPoint(xi, yi))

    def top_intersection(self, point1: QPointF, point2: QPointF) -> QPointF:
        return self.__intersection(point1, point2, self.top)
    
    def bottom_intersection(self, point1: QPointF, point2: QPointF) -> QPointF:
        return self.__intersection(point1, point2, self.bottom)


def horizon_method(canvas: QGraphicsScene, x_interval: Interval, z_interval: Interval, \
        func: Callable[[float, float], float], transform: Transformation) -> list[QLineF]:
    
    result_lines: list[QLineF] = []
    horizon = Horizon(canvas)
    left, right = None, None
    
    z = z_interval.end
    while z >= z_interval.start - z_interval.step / 2:

        prev_vec = QVector3D(x_interval.start, func(x_interval.start, z), z)
        prev = transform.transform_vector(prev_vec).toPointF()

        flag_prev = horizon.visible(prev)
        x = x_interval.start

        result_lines.extend(update_side(horizon, prev, left))
        left = prev

        while x <= x_interval.end + x_interval.step / 2:
            curr_vec = QVector3D(x, func(x, z), z)
            curr = transform.transform_vector(curr_vec).toPointF()

            flag_curr = horizon.visible(curr)
            result_lines.extend(add_lines(
                horizon, 
                [flag_prev, flag_curr],
                [prev, curr]
            ))

            prev = curr
            flag_prev = flag_curr
            x += x_interval.step

        result_lines.extend(update_side(horizon, prev, right))
        right = prev
        z -= z_interval.step

    return result_lines


def update_side(horizon: Horizon, curr: QPointF, prev: QPointF) -> list[QLineF]:
    if prev == None:
        return []
    
    flag_prev = horizon.visible(prev)
    flag_curr = horizon.visible(curr)
    return add_lines(horizon,
                    [flag_prev, flag_curr],
                    [prev, curr])


def add_lines(horizon: Horizon, flags: list[int], points: list[QPointF]) -> list[QLineF]:
    lines: list[QLineF] = []
    flag_prev, flag_curr = flags[0], flags[1]
    prev, curr = points[0], points[1]

    if flag_prev != flag_curr:
        if flag_prev == TOP or flag_curr == TOP:
            top_intersection = horizon.top_intersection(prev, curr)
        if flag_prev == BOTTOM or flag_curr == BOTTOM:
            bottom_intersection = horizon.bottom_intersection(prev, curr)

        if flag_prev == BOTTOM:
            line = QLineF(prev, bottom_intersection)
            lines.append(line)
        if flag_curr == BOTTOM:
            line = QLineF(bottom_intersection, curr)
            lines.append(line)
        if flag_prev == TOP: 
            line = QLineF(prev, top_intersection)
            lines.append(line)
        if flag_curr == TOP:
            line = QLineF(top_intersection, curr)
            lines.append(line)
    
    elif flag_curr != INVISIBLE:
        line = QLineF(prev, curr)
        lines.append(line)
        horizon.update(line)
    
    return lines
