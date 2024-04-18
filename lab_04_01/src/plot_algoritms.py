from PyQt6.QtCore import QPointF, QLineF
from PyQt6.QtWidgets import QGraphicsScene
from PyQt6.QtGui import QColor
import src.geometry as geo
from enum import IntEnum
import math
from functools import singledispatch

class Ellipse:
    def __init__(self, center: QPointF, big_half_axis: float, small_half_axis: float) -> None:
        self.center = center
        self.small_half_axis = small_half_axis
        self.big_half_axis = big_half_axis

class Circle(Ellipse):
    def __init__(self, center: QPointF, radius: float) -> None:
        super.__init__(self, center, radius, radius)

    def radius(self):
        return self.small_half_axis
    
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


class FigurePlotter:
    def __init__(self, scene: QGraphicsScene) -> None:
        self.scene = scene
        self.Intence = 1.0
        self.circle_algorithms = {
            Algorithm.CANONICAL: self.circle_canonical,
            Algorithm.PARAMETRIC: self.circle_parametric,
            Algorithm.BRESENHAM: self.circle_bresenham,
            Algorithm.MIDPOINT: self.circle_midpoint,
            Algorithm.BUILD_IN: self.circle_build_in
        }
        self.ellipse_algorithms = {
            Algorithm.CANONICAL: self.ellipse_canonical,
            Algorithm.PARAMETRIC: self.ellipse_parametric,
            Algorithm.BRESENHAM: self.ellipse_bresenham,
            Algorithm.MIDPOINT: self.ellipse_midpoint,
            Algorithm.BUILD_IN: self.ellipse_build_in
        }

    def __plot_point(self, point: QPointF, color: QColor) -> None:
        self.scene.addEllipse(point.x(), point.y(), 0.5, 0.5, color)

    @singledispatch
    def plot(self, type: Algorithm, circle: Circle, color: QColor) -> None:
        # if isinstance(figure, Circle):
        #     self.__plot_circle(type, figure, color)
        # elif isinstance(figure, Ellipse):
        #     self.__plot_ellipse(type, figure, color)
        #self.algorithms[type](segment.p1(), segment.p2(), color)

    def plot(self, type: Algorithm, ellipse: Ellipse, color: QColor) -> None:
        self.algorithms[type](segment.p1(), segment.p2(), color)
    
    def spectrum(self, type: Algorithm, segment: QLineF, color: QColor, angle: float):
        if type not in self.algorithms:
            return

        start, end = segment.p1(), segment.p2()
        sum_angle = 0.0
        full_circle = 2 * math.pi  
        while sum_angle < full_circle:
            self.algorithms[type](start, end, color)
            end = geo.rotate_point(end, start, angle)
            sum_angle += angle

    def build_in(self, start: QPointF, end: QPointF, color: QColor) -> None:
        line = QLineF(start, end)
        self.scene.addLine(line, color)

    def digital_differential_analyzer(self, start: QPointF, end: QPointF, color: QColor) -> None:
        diff: QPointF = end - start
        diff_x = math.fabs(diff.x()) 
        diff_y = math.fabs(diff.y())
        if diff_x > diff_y:
            length = diff_x
        else:
            length = diff_y

        dx = diff.x() / length
        dy = diff.y() / length

        curr_x = start.x() + 0.5 * sign(dx)
        curr_y = start.y() + 0.5 * sign(dy)

        for _ in range(1, int(length) + 1):
            x, y = int(curr_x), int(curr_y)
            self.__plot_point(QPointF(x, y), color)
            curr_x += dx
            curr_y += dy

    def bresenham_float(self, start: QPointF, end: QPointF, color: QColor) -> None:
        diff: QPointF = end - start
        sx, sy = sign(diff.x()), sign(diff.y())
        dx, dy = abs(diff.x()), abs(diff.y())
       
        exchange = False
        if dy > dx:
            dx, dy = dy, dx
            exchange = True 
        m = dy / dx

        err = m - 0.5
        x, y = start.x(), start.y()

        for _ in range(int(dx)):
            self.__plot_point(QPointF(x, y), color)
            while err >= 0:
                if exchange:
                    x += sx
                else:
                    y += sy
                err -= 1.0
            if exchange:
                y += sy
            else:
                x += sx
            err += m

    def bresenham_int(self, start: QPointF, end: QPointF, color: QColor) -> None:
        diff: QPointF = end - start
        sx, sy = sign(diff.x()), sign(diff.y())
        dx, dy = int(abs(diff.x())), int(abs(diff.y()))
        
        exchange = False
        if dy > dx:
            dx, dy = dy, dx
            exchange = True
        err = 2 * dy - dx
        x, y = int(start.x()), int(start.y())

        for _ in range(dx):
            self.__plot_point(QPointF(x, y), color)
            while err >= 0:
                if exchange:
                    x += sx
                else:
                    y += sy
                err -= 2 * dx
            if exchange:
                y += sy
            else:
                x += sx
            err += 2 * dy

    def bresenham_smooth(self, start: QPointF, end: QPointF, color: QColor) -> None:
        color = QColor(color)
        
        diff: QPointF = end - start
        sx, sy = sign(diff.x()), sign(diff.y())
        dx, dy = int(abs(diff.x())), int(abs(diff.y()))
       
        exchange = False
        if dy > dx:
            dx, dy = dy, dx
            exchange = True 

        m = dy / dx * self.Intence
        err = self.Intence / 2
        w = self.Intence - m

        x, y = start.x(), start.y()
        color.setAlphaF(err)
        
        for _ in range(int(dx)):
            color.setAlphaF(err)
            self.__plot_point(QPointF(x, y), color)
            if err <= w:
                if exchange:
                    y += sy
                else:
                    x += sx
                err += m
            else:
                y += sy
                x += sx
                err -= w
    
    def wu(self, start: QPointF, end: QPointF, color: QColor) -> None:
        color = QColor(color)
        
        diff: QPointF = end - start
        sx, sy = sign(diff.x()), sign(diff.y())
        dx, dy = abs(diff.x()), abs(diff.y())
       
        exchange = False
        if dy > dx:
            dx, dy = dy, dx
            exchange = True 
        m = dy / dx

        err = -1
        x, y = start.x(), start.y()

        for _ in range(int(dx)):
            color.setAlphaF(-err)
            self.__plot_point(QPointF(x, y), color)
            color.setAlphaF(1 + err)
            err += m
            if exchange:
                self.__plot_point(QPointF(x + sx, y + sy), color)
                if err >= 0:
                    x += sx
                    err -= 1
                y += sy
            else:
                self.__plot_point(QPointF(x, y + sy), color)
                if err >= 0:
                    y += sy
                    err -= 1
                x += sx
 