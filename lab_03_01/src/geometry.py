from PyQt6.QtCore import QPointF
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsEllipseItem
from PyQt6.QtGui import QColor

import math

def plot_point(scene: QGraphicsScene, color: QColor, point: QPointF):
    scene.addEllipse(point.x(), point.y(), 0.5, 0.5, color)


def digital_differential_analyzer(scene: QGraphicsScene, color: QColor, start: QPointF, end: QPointF):
    if start == end:
        plot_point(start)
        return
    
    diff: QPointF = end - start
    diff_x = math.fabs(diff.x()) 
    diff_y = math.fabs(diff.y())
    if diff_x > diff_y:
        l = diff_x
    else:
        l = diff_y

    dx = diff.x() / l
    dy = diff.y() / l

    curr_x, curr_y = start.x(), start.y()
    for _ in range(1, int(l) + 1):
        x, y = round(curr_x), round(curr_y)
        plot_point(scene, color, QPointF(x, y))
        curr_x += dx
        curr_y += dy


def sign(num: float) -> int:
    if num > 0:
        return 1
    elif num < 0:
        return -1

    return 0


def float_bresenham(scene: QGraphicsScene, color: QColor, start: QPointF, end: QPointF):
    if start == end:
        plot_point(start)
        return
    
    diff: QPointF = end - start
    sx, sy = sign(diff.x()), sign(diff.y())
    dx, dy = math.fabs(diff.x()), math.fabs(diff.y())
    angle_tan = dy / dx
    fl = 0

    if angle_tan > 1:
        dx, dy = dy, dx
        angle_tan = 1 / angle_tan
        fl = 1
   
    f = angle_tan - 0.5
    x, y = start.x(), start.y()

    for _ in range(1, int(dx) + 1):
        plot_point(scene, color, QPointF(x, y))
        if f > 0:
            if fl == 1:
                x += sx
            else:
                y += sy
            f -= 1
        elif f < 0:
            if fl == 1:
                y += sy
            else:
                x += sx
            f += angle_tan
        

def int_bresenham(scene: QGraphicsScene, color: QColor, start: QPointF, end: QPointF):
    if start == end:
        plot_point(start)
        return
    
    diff: QPointF = end - start
    sx, sy = sign(diff.x()), sign(diff.y())
    dx, dy = math.fabs(diff.x()), math.fabs(diff.y())
    angle_tan = dy / dx
    fl = 0

    if angle_tan > 1:
        dx, dy = dy, dx
        angle_tan = 1 / angle_tan
        fl = 1
   
    f = 2 * dy - dx
    x, y = start.x(), start.y()

    for _ in range(1, int(dx) + 1):
        plot_point(scene, color, QPointF(x, y))
        if f > 0:
            if fl == 1:
                x += sx
            else:
                y += sy
            f -= 2 * dx
        elif f < 0:
            if fl == 1:
                y += sy
            else:
                x += sx
            f += 2 * dy
