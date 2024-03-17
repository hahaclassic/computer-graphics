import math
from PyQt6.QtCore import QPointF
from PyQt6.QtGui import QVector2D

class Circle: 
    def __init__(self, point1: QPointF, point2: QPointF, point3: QPointF) -> None:
        self.__eps = 1e-07
        self.__center, ok = self.__find_center(point1, point2, point3)
        self.__is_valid = ok
        if ok:
            self.__radius = self.__find_radius(point1)
        else:
            self.__radius = 0.0
            
    # Поиск центра окружности через пересечение перпендикуляров, проведенных
    # из центров хорд, соединяющих точки p1, p2 и p1, p3. 
    # Прямые представлены в виде 'точка + направляющий вектор'.
    # Система уравнений решена методом Крамера.
    def __find_center(self, p1: QPointF, p2: QPointF, p3: QPointF) -> tuple[QPointF, bool]:
        
        vec1, vec2 = QVector2D(p2 - p1), QVector2D(p3 - p1)    
        direction_vec1 = self.__perpendicular_vector(vec1)
        direction_vec2 = self.__perpendicular_vector(vec2)
        mid_point1, mid_point2 = (p1 + p2) / 2, (p1 + p3) / 2

        point_diff = mid_point2 - mid_point1
        d = direction_vec2.x() * direction_vec1.y() - direction_vec1.x() * direction_vec2.y()
        d_t = point_diff.y() * direction_vec2.x() - point_diff.x() * direction_vec2.y()

        if math.fabs(d) > self.__eps:
            t = d_t / d
            center = mid_point1 + t * direction_vec1.toPointF()
            ok = True
        else:
            center = QPointF(0, 0)
            ok = False
    
        return center, ok

    def __perpendicular_vector(self, vec: QVector2D) -> QVector2D:
        return QVector2D(-vec.y(), vec.x()).normalized()

    def __find_radius(self, point: QPointF) -> float:
        return QVector2D(self.__center).distanceToPoint(QVector2D(point))
    
    def __str__(self) -> str:
        return f"center = ({self.__center.x():.3f}, {self.__center.y():.3f}), R = {self.__radius:.3f}"
    
    def centers_distance(self, other) -> float:
        if isinstance(other, Circle):
            return QVector2D(self.__center).distanceToPoint(QVector2D(other.__center))
        return -1

    def is_valid(self) -> bool:
        return self.__is_valid

    def radius(self) -> float:
        return self.__radius
    
    def center(self) -> QPointF:
        return self.__center
