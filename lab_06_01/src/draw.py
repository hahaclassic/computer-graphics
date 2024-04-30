import time
from PyQt6.QtWidgets import QGraphicsScene, QApplication
from PyQt6.QtGui import QColor
from PyQt6.QtCore import QLine, QPoint, QPointF

EPS = 1e-07


class BoundaryCond:
    def __init__(self, xl: int = 0, xr: int = 0,
                 tx: int = 0, ty: int = 0) -> None:
        self.xl = xl
        self.xr = xr
        self.tx = tx
        self.ty = ty


class FillParameters:
    def __init__(self, scene: QGraphicsScene, color: QColor) -> None:
        self.scene = scene
        self.view = scene.views()[0]
        self.img = self.view.grab().toImage()
        self.color = color


def fill_figure_with_seed_point(fill: FillParameters, 
                                seed_point: QPoint, delay: float) -> None:
    seed_point = fill.view.mapFromScene(seed_point.toPointF())
    cond = BoundaryCond()
    stack = [seed_point]

    while stack:
        seed_point = stack.pop()
        cond.tx, cond.ty = seed_point.x(), seed_point.y()
        draw_pixel(fill, seed_point)

        cond.xr = fill_right_side(fill, QPoint(cond.tx + 1, seed_point.y()))
        cond.xr -= 1
        cond.xl = fill_left_side(fill, QPoint(cond.tx - 1, seed_point.y()))
        cond.xl += 1

        if cond.ty < fill.scene.height():
            cond.ty += 1
            row_traversal(fill, stack, cond)
            cond.ty -= 1

        cond.ty -= 1
        row_traversal(fill, stack, cond)

        if delay > EPS:
            fill.scene.update()
            QApplication.processEvents()
            time.sleep(delay)


def draw_pixel(fill: FillParameters, point: QPoint):
    fill.img.setPixel(point, fill.color.rgb())
    mapped_point = fill.view.mapToScene(point).toPoint()

    fill.scene.addEllipse(
        mapped_point.x() - 2, mapped_point.y() - 2, 5, 5,
        fill.color, fill.color)


def fill_right_side(fill: FillParameters, point: QPoint):
    x = point.x()

    while fill.img.pixelColor(point) != fill.color and x < fill.scene.width():
        draw_pixel(fill, point)
        x += 1
        point.setX(x)

    return x


def fill_left_side(fill: FillParameters, point: QPoint):
    x = point.x()

    while fill.img.pixelColor(point) != fill.color and x > 0:
        draw_pixel(fill, point)
        x -= 1
        point.setX(x)

    return x


def row_traversal(fill: FillParameters,
                  stack: list[QPoint], cond: BoundaryCond) -> None:
    x, y = cond.xl, cond.ty
    while x <= cond.xr:
        flag = False

        while fill.img.pixelColor(x, y) != fill.color and x <= cond.xr:
            flag = True
            x += 1

        if flag:
            if x == cond.xr and fill.img.pixelColor(x, y) != fill.color:
                if y < fill.scene.height():
                    stack.append(QPoint(x, y))
            else:
                if y < fill.scene.height():
                    stack.append(QPoint(x - 1, y))
            flag = False

        x_in = x
        while fill.img.pixelColor(x, y) == fill.color and x < cond.xr:
            x = x + 1
        if x == x_in:
            x += 1


def draw_line(scene: QGraphicsScene, line: QLine, color: QColor) -> None:
    scene.addLine(line.toLineF(), color)


class Ellipse:
    def __init__(self, center: QPointF, semi_major_axis: float,
                 semi_minor_axis: float) -> None:
        self.center = center
        self.semi_minor_axis = semi_minor_axis
        self.semi_major_axis = semi_major_axis


def draw_ellipse_build_in(scene: QGraphicsScene,
                          ellipse: Ellipse, color: QColor) -> None:
    scene.addEllipse(
        ellipse.center.x() - ellipse.semi_major_axis,
        ellipse.center.y() - ellipse.semi_minor_axis,
        ellipse.semi_major_axis * 2,
        ellipse.semi_minor_axis * 2,
        color
    )
