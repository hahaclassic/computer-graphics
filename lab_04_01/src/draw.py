from PyQt6.QtCore import QPointF, QLineF
from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtGui import QColor
import src.geometry as geo
from enum import IntEnum
import math


class Ellipse:
    def __init__(self, center: QPointF, big_half_axis: float, small_half_axis: float) -> None:
        self.center = center
        self.small_half_axis = small_half_axis
        self.big_half_axis = big_half_axis

class Circle:
    def __init__(self, center: QPointF, radius: float) -> None:
        self.radius = radius
        self.center = center
    
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

def sign(num: float) -> int:
    if num > 0:
        return 1
    elif num < 0:
        return -1

    return 0


class CirclePlotter:
    def __init__(self, scene: QGraphicsScene) -> None:
        self.scene = scene
        self.Intence = 1.0

        self.algorithms = {
            Algorithm.CANONICAL: self.canonical,
            Algorithm.PARAMETRIC: self.parametric,
            Algorithm.BRESENHAM: self.bresenham,
            Algorithm.MIDPOINT: self.midpoint,
            Algorithm.BUILD_IN: self.build_in
        }

    def plot(self, algo_type: Algorithm, circle: Circle, color: QColor) -> None:
        if algo_type in self.algorithms and isinstance(circle, Circle):
            self.algorithms[algo_type](circle, color)

    def spectrum(self, algo_type: Algorithm, circle: Circle, spectrum: Spectrum, color: QColor) -> None:
        if algo_type not in self.algorithms:
            return

        for _ in range(0, spectrum.num_of_figures):
            self.algorithms[algo_type](circle, color)
            circle.radius += spectrum.step


    def canonical(self, circle: Circle, color: QColor) -> None:
        pass

    def parametric(self, circle: Circle, color: QColor) -> None:
        pass

    def bresenham(self, circle: Circle, color: QColor) -> None:
        pass

    def midpoint(self, circle: Circle, color: QColor) -> None:
        pass

    def build_in(self, circle: Circle, color: QColor) -> None:
        self.scene.addEllipse(
            x = circle.center.x() - circle.radius,
            y = circle.center.y() + circle.radius,
            h = circle.radius * 2, 
            w = circle.radius * 2
        )

class EllipsePlotter:
    def __init__(self, scene: QGraphicsScene) -> None:
        self.scene = scene
        self.Intence = 1.0

        self.algorithms = {
            Algorithm.CANONICAL: self.canonical,
            Algorithm.PARAMETRIC: self.parametric,
            Algorithm.BRESENHAM: self.bresenham,
            Algorithm.MIDPOINT: self.midpoint,
            Algorithm.BUILD_IN: self.build_in
        }

    def plot(self, algo_type: Algorithm, ellipse: Ellipse, color: QColor) -> None:
        if algo_type in self.algorithms and isinstance(ellipse, Circle):
            self.algorithms[algo_type](ellipse, color)

    def spectrum(self, algo_type: Algorithm, ellipse: Ellipse, spectrum: Spectrum, color: QColor) -> None:
        if algo_type not in self.algorithms:
            return

        for _ in range(0, spectrum.num_of_figures):
            self.algorithms[algo_type](ellipse, color)
            ellipse.big_half_axis += spectrum.step
            ellipse.small_half_axis += spectrum.step

    def canonical(self, ellipse: Ellipse, color: QColor) -> None:
        pass

    def parametric(self, ellipse: Ellipse, color: QColor) -> None:
        pass

    def bresenham(self, ellipse: Ellipse, color: QColor) -> None:
        pass

    def midpoint(self, ellipse: Ellipse, color: QColor) -> None:
        pass

    def build_in(self, ellipse: Ellipse, color: QColor) -> None:
        self.scene.addEllipse(
            x = ellipse.center.x() - ellipse.big_half_axis,
            y = ellipse.center.y() + ellipse.small_half_axis,
            h = ellipse.small_half_axis * 2, 
            w = ellipse.big_half_axis * 2
        )

    def __plot_point(self, point: QPointF, color: QColor) -> None:
        self.scene.addEllipse(point.x(), point.y(), 0.5, 0.5, color)


class FigurePlotter:
    def __init__(self, scene: QGraphicsScene) -> None:
        self.circle_plotter = CirclePlotter(scene)
        self.ellipse_plotter = EllipsePlotter(scene)
        self.scene = scene
        self.Intence = 1.0

    def plot(self, algo_type: Algorithm, figure: Circle|Ellipse, color: QColor) -> None:
        if isinstance(figure, Circle):
            self.circle_plotter.plot(algo_type, figure, color)
        elif isinstance(figure, Ellipse):
            self.ellipse_plotter.plot(algo_type, figure, color)
    
    def spectrum(self, algo_type: Algorithm, figure: Circle|Ellipse, spectrum: Spectrum, color: QColor):
        if isinstance(figure, Circle):
            self.circle_plotter.spectrum(algo_type, figure, color)
        elif isinstance(figure, Ellipse):
            self.ellipse_plotter.spectrum(algo_type, figure, color)                                                                                           


def plot_symmetric_points(scene: QGraphicsScene, point: QPointF, center: QPointF, color: QColor) -> None:
    p_x, p_y, c_x, c_y = point.x(), point.y(), center.x(), center.y()

    p1 = QPointF(p_x - c_y + c_x, p_x - c_x + c_y)
    p2 = QPointF(-p_y + c_y + c_x, p_x - c_x + c_y)
    p3 = QPointF(p_y - c_y + c_x, -p_x + c_x + c_y)
    p4 = QPointF(-p_y + c_y + c_x, -p_x + c_x + c_y)
    plot_point(scene, p1, color)
    plot_point(scene, p2, color)
    plot_point(scene, p3, color)
    plot_point(scene, p4, color)

    set_pixel(canvas,  dot[0],           dot[1],          dot[2])
    set_pixel(canvas, -dot[0] + 2 * xc,  dot[1],          dot[2])
    set_pixel(canvas,  dot[0],          -dot[1] + 2 * yc, dot[2])
    set_pixel(canvas, -dot[0] + 2 * xc, -dot[1] + 2 * yc, dot[2])

def plot_point(scene: QGraphicsScene, point: QPointF, color: QColor) -> None:
    scene.addEllipse(point.x(), point.y(), 0.5, 0.5, color)


    