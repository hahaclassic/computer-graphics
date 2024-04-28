import time
from PyQt6.QtWidgets import QGraphicsScene, QApplication
from PyQt6.QtGui import QColor, QPolygon
from PyQt6.QtCore import QLine

EPS = 1e-07


class EdgeInfoItem:
    def __init__(self, x: int, dx: float, dy: int):
        self.x = x
        self.dx = dx
        self.dy = dy


def fill_figures(scene: QGraphicsScene,
                 figures: list[QPolygon], color: QColor, delay: float) -> None:
    """A filling algorithm with an ordered list of edges (using a list active
    edges)"""
    edges = create_edges_list(figures)
    y_min, y_max = find_extremes(figures)
    y_groups = create_y_groups(y_min, y_max)

    for edge in edges:
        update_y_group(y_groups, edge)

    active_edges = []
    for y in range(y_max, y_min - 1, -1):
        update_active_edges(active_edges)
        add_active_edges(y_groups, active_edges, y)

        draw_active_edges(scene, active_edges, y, color)
        if delay > EPS:
            scene.update()
            QApplication.processEvents()
            time.sleep(delay)

    draw_edges(scene, edges, color)


def create_edges_list(figures: list[QPolygon]) -> list[QLine]:
    edges = []
    for fig in figures:
        num_points = len(fig)
        for i in range(num_points):
            if i == num_points - 1:
                edges.append(QLine(fig[-1], fig[0]))
            else:
                edges.append(QLine(fig[i], fig[i + 1]))

    return edges


def find_extremes(figures: list[QPolygon]) -> tuple[int, int]:
    y_min = figures[0][0].y()
    y_max = figures[0][0].y()
    for figure in figures:
        for point in figure:
            if point.y() > y_max:
                y_max = point.y()
            if point.y() < y_min:
                y_min = point.y()

    return y_min, y_max


def create_y_groups(y_min: int, y_max: int) -> dict:
    link_list = dict()
    for i in range(round(y_max), round(y_min), -1):
        link_list.update({i: list()})
    return link_list


def update_y_group(y_groups: dict, edge: QLine) -> None:
    x_start, y_start = edge.x1(), edge.y1()
    x_end, y_end = edge.x2(), edge.y2()
    if y_start > y_end:
        x_end, x_start = x_start, x_end
        y_end, y_start = y_start, y_end

    y_diff = abs(y_end - y_start)
    if y_diff == 0:
        return

    x_step = -(x_end - x_start) / y_diff
    if y_end not in y_groups:
        y_groups[y_end] = [EdgeInfoItem(x_end, x_step, y_diff)]
    else:
        y_groups[y_end].append(EdgeInfoItem(x_end, x_step, y_diff))


def update_active_edges(active_edges: list[EdgeInfoItem]) -> None:
    i = 0
    while i < len(active_edges):
        active_edges[i].x += active_edges[i].dx
        active_edges[i].dy -= 1.0
        if active_edges[i].dy < 1:
            active_edges.pop(i)
        else:
            i += 1


def add_active_edges(y_groups: dict, active_edges: list[EdgeInfoItem], y: int) -> None:
    if y not in y_groups:
        return

    for y_group in y_groups[y]:
        active_edges.append(y_group)
    active_edges.sort(key=lambda edge: edge.x)


def draw_active_edges(scene: QGraphicsScene, active_edges: list[EdgeInfoItem],
                      y: int, color: QColor) -> None:
    for i in range(0, len(active_edges) - 1, 2):
        x1, x2 = int(active_edges[i].x), int(active_edges[i + 1].x)
        draw_line(scene, QLine(x1, y, x2, y), color)


def draw_line(scene: QGraphicsScene, line: QLine, color: QColor) -> None:
    scene.addLine(line.toLineF(), color)


def draw_edges(scene: QGraphicsScene,
               edges: list[QLine], color: QColor) -> None:
    for edge in edges:
        draw_line(scene, edge, color)
