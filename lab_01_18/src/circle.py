import math
from PyQt6.QtCore import QPointF

class Circle: 
    def __init__(self, point1: QPointF, point2: QPointF, point3: QPointF) -> None:

        self.__is_valid = True
        self.__p1 = point1
        # self.__p2 = point2
        # self.__p3 = point3
        try:
            self.__center = self.__find_center(point1, point2, point3)
            self.__radius = self.__find_radius()
        except:
            self.__center, self.__radius = QPointF(0,0), 0
            self.__is_valid = False

    def __find_center(self, p1: QPointF, p2: QPointF, p3: QPointF) -> QPointF:

        squares_sum1 = (p1.x() ** 2) + (p1.y() ** 2)
        squares_sum2 = (p2.x() ** 2) + (p2.y() ** 2)
        squares_sum3 = (p3.x() ** 2) + (p3.y() ** 2) 
        a = squares_sum2 - squares_sum3
        b = squares_sum3 - squares_sum1
        c = squares_sum1 - squares_sum2 
        d = p1.x() * (p2.y() - p3.y()) + p2.x() * (p3.y() - p1.y()) + p3.x() * (p1.y() - p2.y())
        
        center_x = -0.5 * (p1.y() * a + p2.y() * b + p3.y() * c) * (1 / d) 
        center_y = 0.5 * (p1.x() * a + p2.x() * b + p3.x() * c) * (1 / d)

        return QPointF(center_x, center_y)

    def __find_radius(self) -> float:
        diff = self.__center - self.__p1
        return math.hypot(diff.x(), diff.y())
    
    def __str__(self) -> str:
        return f"center = ({self.__center.x():.3f}, {self.__center.y():.3f}), R = {self.__radius:.3f}"
    
    def centers_distance(self, other) -> float:
        if isinstance(other, Circle):
            diff = self.__center - other.__center
            return math.hypot(diff.x(), diff.y())
        return -1

    def is_valid(self) -> bool:
        return self.__is_valid

    def radius(self) -> float:
        return self.__radius
    
    def center(self) -> QPointF:
        return self.__center
