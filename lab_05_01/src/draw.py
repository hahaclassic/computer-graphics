from abc import ABC, abstractmethod
from PyQt6.QtCore import QPointF, QPoint
from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtGui import QColor
from enum import IntEnum
import math


class Circle:
    def __init__(self, center: QPointF, radius: float) -> None:
        self.radius = radius
        self.center = center


class Ellipse:
    def __init__(self, center: QPointF, semi_major_axis: float, semi_minor_axis: float) -> None:
        self.center = center
        self.semi_minor_axis = semi_minor_axis
        self.semi_major_axis = semi_major_axis


class Spectrum:
    def __init__(self, step: float, num_of_figures: int) -> None:
        self.step = step
        self.num_of_figures = num_of_figures


class Algorithm(IntEnum):
    CANONICAL = 0
    PARAMETRIC = 1
    BRESENHAM = 2
    MIDPOINT = 3
    BUILD_IN = 4


class Plotter(ABC):
    def __init__(self, scene: QGraphicsScene) -> None:
        self.scene = scene

        self.algorithms = {
            Algorithm.CANONICAL: self.canonical,
            Algorithm.PARAMETRIC: self.parametric,
            Algorithm.BRESENHAM: self.bresenham,
            Algorithm.MIDPOINT: self.midpoint,
            Algorithm.BUILD_IN: self.build_in
        }

    @abstractmethod
    def plot(self, algo_type: Algorithm, circle: Circle, color: QColor) -> None:
        pass

    @abstractmethod
    def spectrum(self, algo_type: Algorithm, circle: Circle,
                 spectrum: Spectrum, color: QColor) -> None:
        pass

    @abstractmethod
    def canonical(self, circle: Circle) -> list[QPoint]:
        pass

    @abstractmethod
    def parametric(self, circle: Circle) -> list[QPoint]:
        pass

    @abstractmethod
    def bresenham(self, circle: Circle) -> list[QPoint]:
        pass

    @abstractmethod
    def midpoint(self, circle: Circle) -> list[QPoint]:
        pass

    @abstractmethod
    def build_in(self, circle: Circle, color: QColor) -> None:
        pass


class CirclePlotter(Plotter):
    def __init__(self, scene: QGraphicsScene) -> None:
        super().__init__(scene)

    def plot(self, algo_type: Algorithm, circle: Circle, color: QColor) -> None:
        if algo_type not in self.algorithms or not isinstance(circle, Circle):
            return

        if algo_type != Algorithm.BUILD_IN:
            points = self.algorithms[algo_type](circle)
            draw_points(self.scene, points, color)
        else:
            self.build_in(circle, color)

    def spectrum(self, algo_type: Algorithm, circle: Circle, spectrum: Spectrum, color: QColor) -> None:
        if algo_type not in self.algorithms or not isinstance(circle, Circle):
            return

        for _ in range(0, spectrum.num_of_figures):
            self.plot(algo_type, circle, color)
            circle.radius += spectrum.step

    def canonical(self, circle: Circle) -> list[QPoint]:
        points: list[QPoint] = []

        start = int(circle.center.x())
        end = start + int(circle.radius / math.sqrt(2)) + 1

        for x in range(start, end):
            y = math.sqrt(circle.radius**2 -
                          (x - circle.center.x())**2) + circle.center.y()
            add_symmetrical_points(points, QPointF(x, y), circle.center, True)

        return points

    def parametric(self, circle: Circle) -> list[QPoint]:
        points: list[QPoint] = []
        step = 1 / circle.radius

        t = 0.0
        end = math.pi / 4 + step
        while t < end:
            x = circle.center.x() + circle.radius * math.cos(t)
            y = circle.center.y() + circle.radius * math.sin(t)
            t += step
            add_symmetrical_points(points, QPointF(x, y), circle.center, True)

        return points

    def bresenham(self, circle: Circle) -> list[QPoint]:
        points: list[QPoint] = []
        x, y = 0, circle.radius
        delta = 2 * (1 - circle.radius)

        add_symmetrical_points(points, circle.center +
                               QPointF(x, y), circle.center, True)
        while x < y:
            if delta <= 0:
                delta_temp = 2 * (delta + y) - 1
                x += 1
                if delta_temp >= 0:
                    delta += 2 * (x - y + 1)
                    y -= 1
                else:
                    delta += 2 * x + 1

            else:
                delta_temp = 2 * (delta - x) - 1
                y -= 1
                if delta_temp < 0:
                    delta += 2 * (x - y + 1)
                    x += 1
                else:
                    delta -= 2 * y - 1
            add_symmetrical_points(
                points, circle.center + QPointF(x, y), circle.center, True)

        return points

    def midpoint(self, circle: Circle) -> list[QPoint]:
        points: list[QPoint] = []
        x, y = circle.radius, 0
        delta = 1 - circle.radius

        add_symmetrical_points(points, circle.center +
                               QPointF(x, y), circle.center, True)
        while x > y:
            y += 1
            if delta > 0:
                x -= 1
                delta -= 2 * x - 2
            delta += 2 * y + 3
            add_symmetrical_points(
                points, circle.center + QPointF(x, y), circle.center, True)

        return points

    def build_in(self, circle: Circle, color: QColor) -> None:
        self.scene.addEllipse(
            circle.center.x() - circle.radius,
            circle.center.y() - circle.radius,
            circle.radius * 2,
            circle.radius * 2,
            color
        )


class EllipsePlotter(Plotter):
    def __init__(self, scene: QGraphicsScene) -> None:
        super().__init__(scene)

    def plot(self, algo_type: Algorithm, ellipse: Ellipse, color: QColor) -> None:
        if algo_type not in self.algorithms or not isinstance(ellipse, Ellipse):
            return

        if algo_type != Algorithm.BUILD_IN:
            points = self.algorithms[algo_type](ellipse)
            draw_points(self.scene, points, color)
        else:
            self.build_in(ellipse, color)

    def spectrum(self, algo_type: Algorithm, ellipse: Ellipse,
                 spectrum: Spectrum, color: QColor) -> None:

        if algo_type not in self.algorithms or not isinstance(ellipse, Ellipse):
            return

        for _ in range(0, spectrum.num_of_figures):
            self.plot(algo_type, ellipse, color)
            ellipse.semi_major_axis += spectrum.step
            ellipse.semi_minor_axis += spectrum.step

    def canonical(self, ellipse: Ellipse) -> list[QPoint]:
        points: list[QPoint] = []
        major, minor = ellipse.semi_major_axis, ellipse.semi_minor_axis
        center_x, center_y = ellipse.center.x(), ellipse.center.y()

        limit = int(center_x + major / math.sqrt(1 + minor**2 / major**2))

        for x in range(int(center_x), limit + 1):
            y = math.sqrt(major**2 * minor**2 - (x - center_x) ** 2
                          * minor**2) / major + center_y
            add_symmetrical_points(points, QPointF(x, y),
                                   ellipse.center, False)

        limit = int(center_y + minor / math.sqrt(1 + major**2 / minor**2))

        for y in range(limit, int(center_y) - 1, -1):
            x = math.sqrt(major**2 * minor**2 - (y - center_y) ** 2
                          * major**2) / minor + center_x
            add_symmetrical_points(points, QPointF(x, y),
                                   ellipse.center, False)

        return points

    def parametric(self, ellipse: Ellipse) -> list[QPoint]:
        points: list[QPoint] = []
        step = 1 / ellipse.semi_major_axis
        if ellipse.semi_major_axis < ellipse.semi_minor_axis:
            step = 1 / ellipse.semi_minor_axis

        t = 0.0
        end = math.pi / 2 + step
        while t < end:
            x = ellipse.center.x() + ellipse.semi_major_axis * math.cos(t)
            y = ellipse.center.y() + ellipse.semi_minor_axis * math.sin(t)
            t += step
            add_symmetrical_points(points, QPointF(x, y),
                                   ellipse.center, False)

        return points

    def bresenham(self, ellipse: Ellipse) -> list[QPoint]:
        points: list[QPoint] = []
        minor, major = ellipse.semi_minor_axis, ellipse.semi_major_axis
        x, y = 0, minor
        delta = minor**2 - major**2 * (2 * minor + 1)

        add_symmetrical_points(points, ellipse.center +
                               QPointF(x, y), ellipse.center, False)

        while y > 0:
            if delta <= 0:
                delta_temp = 2 * delta + major**2 * (2 * y - 1)
                x += 1
                delta += minor**2 * (2 * x + 1)
                if delta_temp >= 0:
                    y -= 1
                    delta += major**2 * (-2 * y + 1)

            else:
                delta_temp = 2 * delta + minor**2 * (-2 * x - 1)
                y -= 1
                delta += major**2 * (-2 * y + 1)
                if delta_temp < 0:
                    x += 1
                    delta += minor**2 * (2 * x + 1)

            add_symmetrical_points(
                points, ellipse.center + QPointF(x, y), ellipse.center, False)

        return points

    def midpoint(self, ellipse: Ellipse) -> list[QPoint]:
        points: list[QPoint] = []
        minor, major = ellipse.semi_minor_axis, ellipse.semi_major_axis
        x, y = 0, minor

        delta = minor**2 - major**2 * minor + 0.25 * major * major
        dx, dy = 2 * minor**2 * x, 2 * major**2 * y

        while dx < dy:
            add_symmetrical_points(
                points, ellipse.center + QPointF(x, y), ellipse.center, False)
            x += 1
            dx += 2 * minor**2

            if delta >= 0:
                y -= 1
                dy -= 2 * major**2
                delta -= dy
            delta += dx + minor**2

        delta = minor**2 * (x + 0.5)**2 + major**2 * \
            (y - 1)**2 - major**2 * minor**2

        while y >= 0:
            add_symmetrical_points(
                points, ellipse.center + QPointF(x, y), ellipse.center, False)
            y -= 1
            dy -= 2 * major**2

            if delta <= 0:
                x += 1
                dx += 2 * minor**2
                delta += dx
            delta -= dy - major**2

        return points

    def build_in(self, ellipse: Ellipse, color: QColor) -> None:
        self.scene.addEllipse(
            ellipse.center.x() - ellipse.semi_major_axis,
            ellipse.center.y() - ellipse.semi_minor_axis,
            ellipse.semi_major_axis * 2,
            ellipse.semi_minor_axis * 2,
            color
        )


def draw_points(scene: QGraphicsScene, points: list[QPoint], color: QColor) -> None:
    for point in points:
        scene.addEllipse(point.x(), point.y(), 0.5, 0.5, color)


def add_symmetrical_points(points: list[QPoint], point: QPointF | QPoint,
                           center: QPointF | QPoint, is_circle: bool):

    if isinstance(center, QPointF):
        center = center.toPoint()
    if isinstance(point, QPointF):
        point = point.toPoint()
    center_x, center_y = center.x(), center.y()
    x, y = point.x(), point.y()

    points.extend([
        point,
        QPoint(2*center_x-x, y),
        QPoint(x, 2*center_y-y),
        QPoint(2*center_x-x, 2*center_y-y),
    ])
    if is_circle:
        points.extend([
            QPoint(y + center_x - center_y, x + center_y - center_x),
            QPoint(-y + center_x + center_y, x + center_y - center_x),
            QPoint(y + center_x - center_y, -x + center_y + center_x),
            QPoint(-y + center_x + center_y, -x + center_y + center_x)
        ])
