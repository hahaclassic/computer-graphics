from PyQt6.QtCore import QPointF
from PyQt6.QtWidgets import QGraphicsLineItem, QGraphicsPolygonItem
from PyQt6.QtGui import QVector2D, QPolygonF
import src.geometry as geo

NUM_OF_SATELLITE_POINTS = 12

class Satellite:
    def __init__(self, points: list[QPointF]) -> None:
        self.window_center = points[0]
        self.window_top_point = points[1]
        self.window_left_point = points[2]
        self.front_wall_center = points[0]
        self.front_wall_top_point = points[3]
        self.front_wall_left_point = points[4]
        self.top_antenna_point = points[5]
        self.solar_panel_point1 = points[6] # bottom right
        self.solar_panel_point2 = points[7] # bottom left
        self.solar_panel_point3 = points[8] # top right
        self.back_wall_center = points[9]
        self.back_wall_top_point = points[10]
        self.back_wall_left_point = points[11]

    def to_points(self) -> list[QPointF]:
        return [
            self.window_center, self.window_top_point, self.window_left_point,
            self.front_wall_top_point, self.front_wall_left_point, 
            self.top_antenna_point, self.solar_panel_point1,
            self.solar_panel_point2, self.solar_panel_point3,
            self.back_wall_center, self.back_wall_top_point,
            self.back_wall_left_point
        ]

    def move(self, dx: float, dy: float) -> None:
        self.window_center = geo.move_point(self.window_center, dx, dy)
        self.window_top_point = geo.move_point(self.window_top_point, dx, dy)
        self.window_left_point = geo.move_point(self.window_left_point, dx, dy)
        self.front_wall_center = geo.move_point(self.front_wall_center, dx, dy)
        self.front_wall_top_point = geo.move_point(self.front_wall_top_point, dx, dy)
        self.front_wall_left_point = geo.move_point(self.front_wall_left_point, dx, dy)
        self.top_antenna_point = geo.move_point(self.top_antenna_point, dx, dy)
        self.solar_panel_point1 = geo.move_point(self.solar_panel_point1, dx, dy)
        self.solar_panel_point2 = geo.move_point(self.solar_panel_point2, dx, dy)
        self.solar_panel_point3 = geo.move_point(self.solar_panel_point3, dx, dy)
        self.back_wall_center = geo.move_point(self.back_wall_center, dx, dy)
        self.back_wall_top_point = geo.move_point(self.back_wall_top_point, dx, dy)
        self.back_wall_left_point = geo.move_point(self.back_wall_left_point, dx, dy)

    def scale(self, center: QPointF, ratio: float) -> None:

        self.window_center = geo.scale_point(self.window_center, center, ratio)
        self.window_top_point = geo.scale_point(self.window_top_point, center, ratio)
        self.window_left_point = geo.scale_point(self.window_left_point, center, ratio)
        self.front_wall_center = geo.scale_point(self.front_wall_center, center, ratio)
        self.front_wall_top_point = geo.scale_point(self.front_wall_top_point, center, ratio)
        self.front_wall_left_point = geo.scale_point(self.front_wall_left_point, center, ratio)
        self.top_antenna_point = geo.scale_point(self.top_antenna_point, center, ratio)
        self.solar_panel_point1 = geo.scale_point(self.solar_panel_point1, center, ratio)
        self.solar_panel_point2 = geo.scale_point(self.solar_panel_point2, center, ratio)
        self.solar_panel_point3 = geo.scale_point(self.solar_panel_point3, center, ratio)
        self.back_wall_center = geo.scale_point(self.back_wall_center, center, ratio)
        self.back_wall_top_point = geo.scale_point(self.back_wall_top_point, center, ratio)
        self.back_wall_left_point = geo.scale_point(self.back_wall_left_point, center, ratio)

    def rotate(self, center: QPointF, angle: float) -> None:

        self.window_center = geo.rotate_point(self.window_center, center, angle)
        self.window_top_point = geo.rotate_point(self.window_top_point, center, angle)
        self.window_left_point = geo.rotate_point(self.window_left_point, center, angle)
        self.front_wall_center = geo.rotate_point(self.front_wall_center, center, angle)
        self.front_wall_top_point = geo.rotate_point(self.front_wall_top_point, center, angle)
        self.front_wall_left_point = geo.rotate_point(self.front_wall_left_point, center, angle)
        self.top_antenna_point = geo.rotate_point(self.top_antenna_point, center, angle)
        self.solar_panel_point1 = geo.rotate_point(self.solar_panel_point1, center, angle)
        self.solar_panel_point2 = geo.rotate_point(self.solar_panel_point2, center, angle)
        self.solar_panel_point3 = geo.rotate_point(self.solar_panel_point3, center, angle)
        self.back_wall_center = geo.rotate_point(self.back_wall_center, center, angle)
        self.back_wall_top_point = geo.rotate_point(self.back_wall_top_point, center, angle)
        self.back_wall_left_point = geo.rotate_point(self.back_wall_left_point, center, angle)

    def center(self) -> QPointF:
        center = (self.window_center + self.back_wall_left_point) / 2
        return center

    def build(self) -> list[QGraphicsLineItem, QGraphicsPolygonItem]:
        satellite_items = []
        satellite_items.extend(self.__build_ellipsoid_objects())
        satellite_items.extend(self.__build_top_side_wall())
        satellite_items.extend(self.__build_bottom_side_wall())
        return satellite_items

    def __build_bottom_side_wall(self) -> list[QGraphicsLineItem, QGraphicsPolygonItem]:
        
        bottom_solar_panel_p1 = self.__reflect_point(self.solar_panel_point1)
        bottom_solar_panel_p2 = self.__reflect_point(self.solar_panel_point2)
        bottom_solar_panel_p3 = self.__reflect_point(self.solar_panel_point3)
        bottom_antenna_point = self.__reflect_point(self.top_antenna_point)
        front_wall_bottom_point = self.__reflect_point(self.front_wall_top_point)
        back_wall_bottom_point = self.__reflect_point(self.back_wall_top_point)

        bottom_solar_panel = self.__build_solar_panel(bottom_solar_panel_p1,
            bottom_solar_panel_p2, bottom_solar_panel_p3)

        bottom_antenna = QGraphicsLineItem(bottom_antenna_point.x(), bottom_antenna_point.y(),
            front_wall_bottom_point.x(), front_wall_bottom_point.y())
        
        bottom_front_line = QGraphicsLineItem(bottom_solar_panel_p1.x(), bottom_solar_panel_p1.y(),
            front_wall_bottom_point.x(), front_wall_bottom_point.y())
        
        bottom_back_line = QGraphicsLineItem(bottom_solar_panel_p2.x(), bottom_solar_panel_p2.y(),
            back_wall_bottom_point.x(), back_wall_bottom_point.y())
        
        return [bottom_solar_panel, bottom_antenna, bottom_front_line, bottom_back_line]

    def __reflect_point(self, point: QPointF) -> QPointF:
        center = self.center()
        symmetry_vector = QVector2D(self.window_center - center)
        vector = QVector2D(point - center)

        reflected = geo.reflect_vector(vector, symmetry_vector)
        return reflected.toPointF() + center

    def __build_top_side_wall(self) -> list[QGraphicsLineItem, QGraphicsPolygonItem]:
        top_solar_panel = self.__build_solar_panel(self.solar_panel_point1,
            self.solar_panel_point2, self.solar_panel_point3)

        top_antenna = QGraphicsLineItem(self.top_antenna_point.x(), self.top_antenna_point.y(),
            self.front_wall_top_point.x(), self.front_wall_top_point.y())
        
        top_front_line = QGraphicsLineItem(self.solar_panel_point1.x(), self.solar_panel_point1.y(),
            self.front_wall_top_point.x(), self.front_wall_top_point.y())
        
        top_back_line = QGraphicsLineItem(self.solar_panel_point2.x(), self.solar_panel_point2.y(),
            self.back_wall_top_point.x(), self.back_wall_top_point.y())

        return [top_solar_panel, top_antenna, top_front_line, top_back_line]

    def __build_solar_panel(self, p1: QPointF, p2: QPointF, p3: QPointF) -> QGraphicsPolygonItem:
        top_solar_panel = QPolygonF(
            [p1,
            p2,
            p3 - (p1 - p2),
            p3]
        )
        return QGraphicsPolygonItem(top_solar_panel)
    
    def __build_ellipsoid_objects(self) -> list[QGraphicsPolygonItem]:
        window_items = geo.build_ellipse(self.window_center, self.window_top_point, 
            self.window_left_point)
        
        front_wall_items = geo.build_ellipse(self.front_wall_center, 
            self.front_wall_top_point, self.front_wall_left_point)
        
        back_wall_items = geo.build_left_half_ellipse(self.back_wall_center,
            self.back_wall_top_point, self.back_wall_left_point)

        return window_items + front_wall_items + back_wall_items
         
