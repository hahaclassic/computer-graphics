import math

# point = tuple[float, float]
# tuple[0] - x
# tuple[1] - y

class Cicle: 
    def __init__(self, point1: tuple[float, float], point2: tuple[float, float], \
        point3: tuple[float, float]) -> None:

        self.__is_valid = True
        self.__p1 = point1
        # self.__p2 = point2
        # self.__p3 = point3
        try:
            self.__center = self.__find_center(point1, point2, point3)
            self.__radius = self.__find_radius()
        except:
            self.__center, self.__radius = (0,0), 0
            self.__is_valid = False

    def __find_center(self, p1, p2, p3) -> tuple[float, float]:

        squares_sum1 = (p1[0] ** 2) + (p1[1] ** 2)
        squares_sum2 = (p2[0] ** 2) + (p2[1] ** 2)
        squares_sum3 = (p3[0] ** 2) + (p3[1] ** 2) 
        a = squares_sum2 - squares_sum3
        b = squares_sum3 - squares_sum1
        c = squares_sum1 - squares_sum2 
        d = p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1])
        
        center_x = -0.5 * (p1[1] * a + p2[1] * b + p3[1] * c) * (1 / d) 
        center_y = 0.5 * (p1[0] * a + p2[0] * b + p3[0] * c) * (1 / d)

        return (center_x, center_y)

    def __find_radius(self) -> float:
        return math.dist(self.__center, self.__p1)
    
    def __str__(self) -> str:
        return f"center = ({self.__center[0]:.3f}, {self.__center[1]:.3f}), R = {self.__radius:.3f}"
    
    def centers_distance(self, other) -> float:
        return math.dist(self.__center, other.__center)

    def is_valid(self) -> bool:
        return self.__is_valid

    def radius(self) -> float:
        return self.__radius
    
    def center(self) -> tuple[float, float]:
        return self.__center

class Vector2D():
    def __init__(self, start: tuple[float, float], end: tuple[float, float]) -> None:
        super().__init__()
        self.start_point = start
        self.end_point = end
        self.length = math.dist(start, end)

    def len(self) -> float:
        return self.length
    
    def rotate(self, alpha: float) -> None:

        x = self.end_point[0] - self.start_point[0]
        y = self.end_point[1] - self.start_point[1]

        x, y = math.cos(alpha) * x - math.sin(alpha) * y, \
            math.sin(alpha) * x + math.cos(alpha) * y

        self.end_point = (x + self.start_point[0], y + self.start_point[1])

    def end(self) -> tuple[float, float]:
        return self.end_point

    def start(self) -> tuple[float, float]:
        return self.start_point
    