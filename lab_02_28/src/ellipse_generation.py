import math
from PyQt6.QtCore import QPointF
from PyQt6.QtWidgets import QGraphicsLineItem

from typing import Callable

NUM_OF_POINTS_OF_ELLIPSE = 100

def create_ellipse_functions(center: QPointF, top_point: QPointF, 
    left_point: QPointF) -> tuple[Callable[[float], float], Callable[[float], float]]:

    center_to_left = center - left_point
    top_to_center = top_point - center

    def x_t(t: float):
        return center_to_left.x() * math.cos(t) + top_to_center.x() * math.sin(t) + center.x()

    def y_t(t: float):
        return center_to_left.y() * math.cos(t) + top_to_center.y() * math.sin(t) + center.y()

    return x_t, y_t


def generate_line_items(func_x_t: Callable[[float], float], func_y_t: Callable[[float], float], 
    start: float, end: float) -> list[QGraphicsLineItem]:
    
    items_list = []
    
    step = (end - start) / NUM_OF_POINTS_OF_ELLIPSE
    last_x, last_y = func_x_t(start), func_y_t(start)
    start += step

    while start < end:

        x, y = func_x_t(start), func_y_t(start)
        items_list.append(QGraphicsLineItem(last_x, last_y, x, y))

        last_x, last_y = x, y
        start += step
        
    return items_list


def build_ellipse(center: QPointF, top_point: QPointF, 
                  left_point: QPointF) -> list[QGraphicsLineItem]:

    func_x_t, func_y_t = create_ellipse_functions(center, top_point, left_point)

    start, end = 0, 2 * math.pi
        
    return generate_line_items(func_x_t, func_y_t, start, end)

# Build_half_ellipse() creates left half of ellipse
def build_left_half_ellipse(center: QPointF, top_point: QPointF, 
        left_point: QPointF) -> list[QGraphicsLineItem]:

    func_x_t, func_y_t = create_ellipse_functions(center, top_point, left_point)

    start, end = math.pi / 2, 3.0 / 2.0 * math.pi
   
    return generate_line_items(func_x_t, func_y_t, start, end)
