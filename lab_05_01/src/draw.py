from dataclasses import dataclass
import time

from PyQt6.QtWidgets import QMainWindow, QMessageBox, \
    QPushButton, QColorDialog, QLabel, QGraphicsView, QGraphicsScene, QTextEdit, QComboBox, QCheckBox
from PyQt6.QtGui import QColor, QTransform, QPolygon
from PyQt6.QtCore import Qt, QChildEvent, QPointF, QPoint, QLine

EPS = 1e-07

@dataclass
class Point:
    x: int
    y: int

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

@dataclass
class Node:
    x: float
    dx: float
    dy: int

    def __init__(self, x=0, dx=0, dy=0):
        self.x = x
        self.dx = dx
        self.dy = dy


def draw_line(canvas, ps, pe, colour):
    x_beg = ps.x + 0.5
    x_end = pe.x + 0.5
    y = ps.y
    canvas.create_line(x_beg, y, x_end, y, fill=colour)


def draw_edges(canvas, edges):
    for i in range(len(edges)):
        canvas.create_line(edges[i][0].x, edges[i][0].y,
                           edges[i][1].x, edges[i][1].y, fill="black")


# figures - полигон фигур или массив всех замкнутых фигур
def make_edges_list(figures):
    edges = list()
    for fig in figures:
        num_points = len(fig)
        for i in range(num_points):
            if i + 1 > num_points - 1:
                edges.append(QLine(fig[-1], fig[0]))
            else:
                edges.append(QLine(fig[i], fig[i + 1]))

    return edges


def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


def find_extrimum_Y_figures(figures):
    yMin = figures[0][0].y()
    yMax = figures[0][0].y()
    for fig in figures:
        for p in fig:
            if p.y() > yMax:
                yMax = p.y()
            if p.y() < yMin:
                yMin = p.y()
    return yMin, yMax

def make_link_list(Ymin=0, Ymax=0):
    link_list = dict()
    for i in range(round(Ymax), round(Ymin), -1):
        link_list.update({i: list()})
    return link_list

def make_insert_thm(edges: list[QLine], link_list):
    for edge in edges:
        x1 = edge.x1()
        y1 = edge.y1()
        x2 = edge.x2()
        y2 = edge.y2()

        len_x = abs(int(x2) - int(x1))
        len_y = abs(int(y2) - int(y1))

        if len_y != 0:
            dx = ((x2 > x1) - (x2 < x1)) * len_x / len_y
            dy = ((y2 > y1) - (y2 < y1))

            nmax = max(y1, y2)

            x = x1 + dx / 2
            y = y2 + dy / 2

            for j in range(len_y):
                sotYdr = link_list.get(nmax)
                sotYdr.append(Node(x1))
                x += dx
                y += dy


def update_y_group(y_groups, edge: QLine):
        x_start, y_start = edge.x1(), edge.y2()
        x_start, y_end = edge.x2(), edge.y2()
        if y_start > y_end:
            x_end, x_start = x_start, x_end
            y_end, y_start = y_start, y_end

        y_proj = abs(y_end - y_start)
        if y_proj != 0:
            x_step = -(x_end - x_start) / y_proj
            if y_end not in y_groups:
                y_groups[y_end] = [Node(x_end, x_step, y_proj)]
            else:
                y_groups[y_end].append(Node(x_end, x_step, y_proj))


def iterator_active_edges(active_edges):
    i = 0
    while i < len(active_edges):
        active_edges[i].x += active_edges[i].dx
        active_edges[i].dy -= 1
        if active_edges[i].dy < 1:
            active_edges.pop(i) # удаляем как в стеке LIFO - размерность списка n x 4, бывают случаи когда нечетное в этом случае не учитвается
        else:
            i += 1


def add_active_edges(y_groups, active_edges: list, y):
    if y in y_groups:
        for y_group in y_groups.get(y):
            active_edges.append(y_group)
    active_edges.sort(key=lambda edge: edge.x)


def draw_act(canvas, active_edges, y, color):
    len_edge = len(active_edges)
    for i in range(0, len_edge - 1, 2):
        draw_line(canvas, QLine(active_edges[i].x, y, active_edges[i + 1].x, y), color)

def CAP_algorithm_with_ordered_list_of_edges(canvas, figures: list, color: QColor, delay: float):
    edges = make_edges_list(figures)

    ymin, ymax = find_extrimum_Y_figures(figures)
    y_groups = make_link_list(ymin, ymax)
        
    for edge in edges:
        update_y_group(y_groups, edge)

    y_end = ymax
    y_start = ymin
    active_edges = []
    while y_end > y_start:
        iterator_active_edges(active_edges)
        add_active_edges(y_groups, active_edges, y_end)

        draw_act(canvas, active_edges, y_end, color)
        y_end -= 1
        if delay > EPS:
            time.sleep(delay)
    draw_edges(canvas, edges, color)


def draw_line(scene: QGraphicsScene, line: QLine, color: QColor) -> None:
    scene.addLine(line.toLineF(), color)

def draw_edges(scene: QGraphicsScene, edges: list[QLine], color: QColor) -> None:
    for edge in edges:
        draw_line(scene, edge, color)