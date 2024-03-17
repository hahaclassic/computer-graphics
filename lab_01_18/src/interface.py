import math
import src.maxarea as maxarea
from src.circle import Circle
from src.widgets import MainWindow
from PyQt6.QtCore import Qt, QPointF

class Interface(MainWindow):
    def __init__(self):
        super().__init__(self)

        ### Points
        self.set1: list[QPointF] = []
        self.set2: list[QPointF] = []
        
        # Connect button click signals to slot functions
        self.button_calc.clicked.connect(self.__calcucate_and_show_result)
        self.button_add_point.clicked.connect(self.__get_point_from_input_fields)
        self.button_clear.clicked.connect(self.clear_all)

    def __calcucate_and_show_result(self) -> None:
    
        max_area, circle1, circle2 = maxarea.find_max_area(self.set1, self.set2)
        if max_area == -math.inf:
            self.output_field.setText("Невозможно получить ответ.")
            return

        tangent_p1, tangent_p2 = maxarea.tangent_coordinates(circle1, circle2)

        self.output_field.setText(
            f"Smax = {max_area:.3f}\ncircle1: {circle1}\ncircle2: {circle2}")

        self.__plot_result_figure(circle1, circle2, tangent_p1, tangent_p2)

    def __plot_result_figure(self, circle1: Circle, circle2: Circle, \
        tangent_p1: QPointF, tangent_p2: QPointF):

        self.canvas.clear()
        self.canvas.plot_points_auto_range(self.set1, 'r')
        self.canvas.plot_points_auto_range(self.set2, 'b')

        self.canvas.plot_line(tangent_p1, tangent_p2, 'g')
        self.canvas.plot_line(circle1.center(), circle2.center(), 'g')

        self.canvas.plot_line(tangent_p1, circle1.center(), 'g')
        self.canvas.plot_line(tangent_p2, circle2.center(), 'g')
        
        self.canvas.plot_circle(circle1, 'g')
        self.canvas.plot_circle(circle2, 'g')
        self.canvas.plot_points_auto_range([circle1.center(), circle2.center(), tangent_p1, tangent_p2], 'w')

    def point_idx_set1(self, point: QPointF) -> int:
        for i, current in enumerate(self.set1):
            if point == current:
                return i
        return -1
    
    def point_idx_set2(self, point: QPointF) -> int:
        for i, current in enumerate(self.set2):
            if point == current:
                return i
        return -1

    def add_point_set1(self, point: QPointF) -> bool:
        # Returns True if the point was successfully added
        idx = self.point_idx_set1(point)
        if idx == -1:
            self.set1.append(point)
            self.table_set1.insert_point(point)
            return True
        return False

    def add_point_set2(self, point: QPointF) -> bool:
        # Returns True if the point was successfully added
        idx = self.point_idx_set2(point)
        if idx == -1:
            self.set2.append(point)
            self.table_set2.insert_point(point)
            return True
        return False

    def __get_point_from_input_fields(self) -> None:
        try:
            x = float(self.input_field_x.toPlainText())
            y = float(self.input_field_y.toPlainText())
        except ValueError:
            self.show_error_message("Некорректные данные", "В полях ввода указаны некорректные данные")
            return

        ok = True
        point = QPointF(x,y)
        if self.check_box_set1.checkState() == Qt.CheckState.Checked:
            ok = self.add_point_set1(point)
            if ok:
                self.canvas.plot_point(point, 'r')
        else:
            ok = self.add_point_set2(point)
            if ok:
                self.canvas.plot_point(point, 'b')

        if not ok:
            self.show_error_message("Ошибка", "Данная точка уже существует")
        
        self.canvas.getViewBox().autoRange()
        self.input_field_x.clear()
        self.input_field_y.clear()

    def delete_point_set1(self, point_idx: int) -> None:
        self.set1.pop(point_idx)
        self.table_set1.removeRow(point_idx)

    def delete_point_set2(self, point_idx: int) -> None:
        self.set2.pop(point_idx)
        self.table_set2.removeRow(point_idx)

    def load_set1(self) -> None:
        points = self.load_data()
        self.clear_set1()

        for i in range(0, len(points) - 1, 2):
            self.add_point_set1(QPointF(points[i], points[i + 1]))

        self.canvas.clear()
        self.canvas.plot_points_auto_range(self.set1, 'r')
        self.canvas.plot_points_auto_range(self.set2, 'b')

    def load_set2(self) -> None:
        points = self.load_data()
        self.clear_set2()

        for i in range(0, len(points) - 1, 2):
            self.add_point_set2(QPointF(points[i], points[i + 1]))

        self.canvas.clear()
        self.canvas.plot_points_auto_range(self.set1, 'r')
        self.canvas.plot_points_auto_range(self.set2, 'b')

    def save_set1(self) -> None:
        self.save_points(self.set1)

    def save_set2(self) -> None:
        self.save_points(self.set2)

    def clear_set1(self) -> None:
        self.set1.clear()
        self.table_set1.setRowCount(0)

    def clear_set2(self) -> None:
        self.set2.clear()
        self.table_set2.setRowCount(0)

    def clear_all(self) -> None:
        self.canvas.clear()
        self.canvas.setXRange(0, 12)
        self.canvas.setYRange(0,12)
        self.clear_set1()
        self.clear_set2()
