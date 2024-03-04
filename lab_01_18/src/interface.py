from PyQt6.QtWidgets import QWidget, QMainWindow, QPushButton, \
    QAbstractItemView, QGridLayout, QTextEdit, QLabel, QMenu, QMenuBar, \
    QFileDialog, QTableWidget, QTableWidgetItem, QCheckBox,QMessageBox, \
    QScrollArea, QVBoxLayout
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, QSize, QPointF
import pyqtgraph as pg

import math
import src.maxarea as maxarea
import src.objects as obj

MANUAL_PATH = "./src/app_messages/manual.txt"
TASK_PATH = "./src/app_messages/task.txt"

class ScrolledLabel(QWidget):
    def __init__(self, text) -> None:
        super().__init__()

        self.label = QLabel(text)
        self.label.setWordWrap(True)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.label)

        layout = QVBoxLayout()
        layout.addWidget(scroll_area)
        self.setLayout(layout)

class MenuBar(QMenuBar):
    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent)

        self.file_actions = QMenu("Файл", parent)
        self.import_set1 = QAction("Импортировать множество точек А", parent)
        self.export_set1 = QAction("Экспортировать множество точек А", parent)
        self.import_set2 = QAction("Импортировать множество точек B", parent)
        self.export_set2 = QAction("Экспортировать множество точек B", parent)

        self.task_condition = QAction("Условие", parent)
        self.manual = QAction("Инструкция", parent)

        self.import_set1.triggered.connect(parent.load_set1)
        self.export_set1.triggered.connect(parent.save_set1)
        self.import_set2.triggered.connect(parent.load_set2)
        self.export_set2.triggered.connect(parent.save_set2)
        self.manual.triggered.connect(parent.show_manual)
        self.task_condition.triggered.connect(parent.show_task)

        self.file_actions.addAction(self.import_set1)
        self.file_actions.addAction(self.export_set1)
        self.file_actions.addAction(self.import_set2)
        self.file_actions.addAction(self.export_set2)
        self.addMenu(self.file_actions)
        self.addAction(self.task_condition)
        self.addAction(self.manual)
        
class PointsTable(QTableWidget):
    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent)
        self.main_window = parent
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["X", "Y"])
        self.setFixedWidth(200)
        self.setMinimumHeight(200)
    
    def insert_point(self, x: float, y: float) -> None:
        self.insertRow(self.rowCount())
        self.setItem(self.rowCount() - 1, 0, QTableWidgetItem(str(x)))
        self.setItem(self.rowCount() - 1, 1, QTableWidgetItem(str(y)))

    # TODO: Вынести 1e-07 в глобальные константы как eps
    def delete_point(self, x: float, y: float) -> None:
        n = self.rowCount()
        for i in range(n):
            if math.fabs(float(self.item(i, 0).text()) - x) < 1e-07 \
                and math.fabs(float(self.item(i, 1).text()) - y) < 1e-07:
                self.removeRow(i)
                break

    # TODO: Переделать, убрать обращение к полям родительского виджета.
    # TODO: (optional) отмечать выбранную точку, чтобы пользователь понимал,
    # какая точка в данный момент выбрана.
    def contextMenuEvent(self, event) -> None:
        index = self.indexAt(event.pos())
        if not index.isValid():
            return
    
        row = index.row()
        reply = QMessageBox.question(self, 'Удалить точку?',
            f'Удалить точку №{row + 1}?', 
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            x, y = float(self.item(row, 0).text()), float(self.item(row, 1).text())
            if (x,y) in self.main_window.set1:
                self.main_window.delete_point_set1(x,y)
                self.main_window.canvas.clear()
                self.main_window.canvas.plot_points(self.main_window.set1, 'r')
                self.main_window.canvas.plot_points(self.main_window.set2, 'b')
            else:
                self.main_window.delete_point_set2(x,y)
                self.main_window.canvas.clear()
                self.main_window.canvas.plot_points(self.main_window.set1, 'r')
                self.main_window.canvas.plot_points(self.main_window.set2, 'b')
            self.removeRow(row)

        super().contextMenuEvent(event)

class Canvas(pg.PlotWidget):
    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent)
        self.showGrid(x=True, y=True)
        self.setXRange(0, 10)
        self.setYRange(0,10)
        self.setAspectLocked()
        self.parent = parent
        self.setMinimumSize(QSize(400,400))

    def mousePressEvent(self, ev) -> None:
        if ev.button() == Qt.MouseButton.MiddleButton:
            return super().mousePressEvent(ev)
        elif ev.button() == Qt.MouseButton.LeftButton and \
            ev.modifiers() & Qt.KeyboardModifier.ControlModifier:
            return self.delete_point(ev.pos())

        grid_pos = self.getViewBox().mapSceneToView(QPointF(ev.pos()))
        x, y = round(grid_pos.x(), 3), round(grid_pos.y(), 3)
    
        if ev.button() == Qt.MouseButton.LeftButton:
            self.plot_point(x, y, 'r')
            self.parent.add_point_set1(x, y)
        elif ev.button() == Qt.MouseButton.RightButton:
            self.plot_point(x, y, 'b')
            self.parent.add_point_set2(x, y)

    def plot_point(self, x: float, y: float, color: str) -> None:
        scatter = pg.ScatterPlotItem(pen=color, x=[x], y=[y], brush=color, symbol='o')
        self.addItem(scatter)
 
    def plot_points(self, points: set, color: str) -> None:
        x = list(map(lambda point: point[0], points))
        y = list(map(lambda point: point[1], points))
        scatter = pg.ScatterPlotItem(pen=color, x=x, y=y, brush=color, symbol='o')
        self.addItem(scatter)
        
    def plot_points_auto_range(self, points: set, color: str) -> None:
        self.plot_points(points, color)
        self.getViewBox().autoRange()

    # Переделать, убрать обращение к полям родительского виджета.
    def delete_point(self, pos) -> None:
        isExist = False

        for x_start in range(pos.x() - 10, pos.x() + 10):
            for y_start in range(pos.y() - 10, pos.y() + 10):
                grid_pos = self.getViewBox().mapSceneToView(QPointF(x_start, y_start))
                x, y = round(grid_pos.x(), 3), round(grid_pos.y(), 3)

                if (x,y) in self.parent.set1:
                    isExist = True
                    self.parent.delete_point_set1(x, y)
                    self.parent.delete_point_set1_from_table(x,y)
                    break
                elif (x,y) in self.parent.set2:
                    isExist = True
                    self.parent.delete_point_set2(x,y)
                    self.parent.delete_point_set2_from_table(x,y)
                    break
            if isExist:
                self.clear()
                self.plot_points(self.parent.set1, 'r')
                self.plot_points(self.parent.set2, 'b')
                break

    def plot_line(self, start: tuple[float, float], end: tuple[float, float], color) -> None:
        x = [start[0], end[0]]
        y = [start[1], end[1]]

        line = pg.PlotDataItem(pen=color, x=x, y=y, brush=color)
        self.addItem(line)
        self.getViewBox().autoRange()

    def plot_cicle(self, cicle: obj.Cicle, color: str) -> None:
        center, r = cicle.center(), cicle.radius()
        x1,y1 = center[0] - r, center[1] - r
        cicle1 = pg.CircleROI(pen=color, pos=(x1,y1), radius=r)

        self.addItem(cicle1)
        self.getViewBox().autoRange()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        ### Points
        self.set1 = set()
        self.set2 = set()

        self.setWindowTitle('Лабораторная работа №1')
        self.setMinimumSize(920,550)
        
        self.manualWidget = self.__setup_manual()
        self.taskWidget = self.__setup_task()

        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)

        self.canvas = Canvas(self)

        # Create table labels
        self.table_set1_label, self.table_set2_label = QLabel(self), QLabel(self)
        self.table_set1_label.setText("Множество A")
        self.table_set2_label.setText("Множество B")

        # Create input fields labels
        self.label_x, self.label_y = QLabel(self), QLabel(self)
        self.label_x.setText("координата X")
        self.label_y.setText("координата Y") 

        # Create input fields
        self.input_field_x = QTextEdit(self)
        self.input_field_x.setFixedSize(QSize(200, 50))
        self.input_field_y = QTextEdit(self)
        self.input_field_y.setFixedSize(QSize(200, 50))

        self.check_box_set1 = QCheckBox("В множество А", self)
        self.check_box_set2 = QCheckBox("В множество B", self)

        self.check_box_set1.setChecked(True)
        self.check_box_set1.stateChanged.connect(lambda state: self.check_box_set2.setChecked(not state))
        self.check_box_set2.stateChanged.connect(lambda state: self.check_box_set1.setChecked(not state))

        # Create output fields
        self.result_label = QLabel("Результат:")
        self.output_field = QLabel(self)
    
        # Create point tables
        self.table_set1 = PointsTable(self)
        self.table_set2 = PointsTable(self)

        # Create buttons
        self.button_calc = QPushButton('Найти решение', self)
        self.button_calc.setStyleSheet("""QPushButton { 
            background-color: green; 
            color: black;
        }""")
        self.button_clear = QPushButton('Очистить плоскость', self)
        self.button_add_point = QPushButton('Добавить точку', self)

        # Connect button click signals to slot functions
        self.button_calc.clicked.connect(self.__calcucate_and_show_result)
        self.button_add_point.clicked.connect(self.__get_point_from_input_fields)
        self.button_clear.clicked.connect(self.clear_all)

        # Create a QGridLayout
        self.layoutWidget = self.__setup_layout()
    
        # Set the layout for the main window
        central_widget = QWidget()
        central_widget.setLayout(self.layoutWidget)
        self.setCentralWidget(central_widget)    

    def __setup_layout(self) -> QGridLayout:
        layoutWidget = QGridLayout()
        layoutWidget.addWidget(self.canvas, 0, 0, 7, 2)
        layoutWidget.addWidget(self.manualWidget, 0, 0, 7, 2)
        layoutWidget.addWidget(self.taskWidget, 0, 0, 7, 2)

        # Add tables to the layout
        layoutWidget.addWidget(self.table_set1, 1, 2, 4, 1)
        layoutWidget.addWidget(self.table_set2, 1, 3, 4, 1)

        # Add labels
        layoutWidget.addWidget(self.table_set1_label, 0, 2, 1, 1)
        layoutWidget.addWidget(self.table_set2_label, 0, 3, 1, 1)

        layoutWidget.addWidget(self.label_x, 5, 2, 1, 1)
        layoutWidget.addWidget(self.label_y, 5, 3, 1, 1)

        # Add input fields
        layoutWidget.addWidget(self.input_field_x, 6, 2, 1, 1)
        layoutWidget.addWidget(self.input_field_y, 6, 3, 1, 1)

        layoutWidget.addWidget(self.check_box_set1, 7, 2, 1, 1)
        layoutWidget.addWidget(self.check_box_set2, 7, 3, 1, 1)

        # Add output fields
        layoutWidget.addWidget(self.result_label, 7, 0, 1, 1)
        layoutWidget.addWidget(self.output_field, 8, 0, 2, 1)

        # Add buttons to the layout
        layoutWidget.addWidget(self.button_add_point, 8, 2, 1, 2)
        layoutWidget.addWidget(self.button_calc, 9, 3)
        layoutWidget.addWidget(self.button_clear, 9, 2)

        return layoutWidget

    def __setup_manual(self) -> ScrolledLabel:

        try:
            file = open(MANUAL_PATH, "r", encoding='utf-8')
            manual = file.read()
            file.close()
        except:
            manual = "Произошла ошибка во время получения инструкции."

        manualWidget = ScrolledLabel(manual)
        manualWidget.hide()

        return manualWidget

    def __setup_task(self) -> QLabel:
        try:
            file = open(TASK_PATH, "r", encoding='utf-8')
            task = file.read()
            file.close()
        except:
            task = "Произошла ошибка во время получения условия задачи."

        taskWidget = QLabel(task)
        taskWidget.hide()

        return taskWidget

    def __calcucate_and_show_result(self) -> None:
    
        max_area, cicle1, cicle2 = maxarea.find_max_area(self.set1, self.set2)
        if max_area == -math.inf:
            self.output_field.setText("Невозможно получить ответ.")
            return

        tangent_p1, tangent_p2 = maxarea.tangent_coordinates(cicle1, cicle2)

        self.output_field.setText(
            f"Smax = {max_area:.3f}\ncicle1: {cicle1}\ncicle2: {cicle2}")

        self.__plot_result_figure(cicle1, cicle2, tangent_p1, tangent_p2)

    def __plot_result_figure(self, cicle1: obj.Cicle, cicle2: obj.Cicle, tangent_p1, tangent_p2):
        self.canvas.clear()
        self.canvas.plot_points_auto_range(self.set1, 'r')
        self.canvas.plot_points_auto_range(self.set2, 'b')

        self.canvas.plot_line(tangent_p1, tangent_p2, 'g')
        self.canvas.plot_line(cicle1.center(), cicle2.center(), 'g')

        self.canvas.plot_line(tangent_p1, cicle1.center(), 'g')
        self.canvas.plot_line(tangent_p2, cicle2.center(), 'g')
        
        self.canvas.plot_cicle(cicle1, 'g')
        self.canvas.plot_cicle(cicle2, 'g')
        self.canvas.plot_points_auto_range(set([cicle1.center(), cicle2.center(), tangent_p1, tangent_p2]), 'w')

    def add_point_set1(self, x: float, y: float) -> bool:
        point = (round(x, 3), round(y, 3))
        if point not in self.set1:
            self.set1.add(point)
            self.table_set1.insert_point(point[0], point[1])

    def add_point_set2(self, x: float, y: float) -> bool:
        point = (round(x, 3), round(y, 3))
        if point not in self.set1:
            self.set2.add(point)
            self.table_set2.insert_point(point[0], point[1])

    def __get_point_from_input_fields(self) -> None:
        try:
            x = float(self.input_field_x.toPlainText())
            y = float(self.input_field_y.toPlainText())
        except:
            self.show_error_message("Некорректные данные", 
                "В полях ввода указаны некорректные данные")
            return

        if self.check_box_set1.checkState() == Qt.CheckState.Checked:
            self.add_point_set1(x,y)
            self.canvas.plot_point(round(x, 3), round(y, 3), 'r')
        else:
            self.add_point_set2(x,y)
            self.canvas.plot_point(round(x, 3), round(y, 3), 'b')
        self.canvas.getViewBox().autoRange()

        self.input_field_x.clear()
        self.input_field_y.clear()

    def delete_point_set1(self, x: float, y: float) -> None:
        rounded_x, rounded_y = round(x, 3), round(y, 3) 
        self.set1.remove((rounded_x, rounded_y))

    def delete_point_set1_from_table(self, x: float, y: float) -> None:
        rounded_x, rounded_y = round(x, 3), round(y, 3) 
        self.table_set1.delete_point(rounded_x, rounded_y)

    def delete_point_set2(self, x: float, y: float) -> None:
        rounded_x, rounded_y = round(x, 3), round(y, 3) 
        self.set2.remove((rounded_x, rounded_y))

    def delete_point_set2_from_table(self, x: float, y: float) -> None:
        rounded_x, rounded_y = round(x, 3), round(y, 3) 
        self.table_set2.delete_point(rounded_x, rounded_y)

    def load_set1(self) -> None:
        points = self.__load_data()
        self.clear_set1()

        for i in range(0, len(points) - 1, 2):
            self.add_point_set1(points[i], points[i + 1])

        self.canvas.clear()
        self.canvas.plot_points_auto_range(self.set1, 'r')
        self.canvas.plot_points_auto_range(self.set2, 'b')

    def load_set2(self) -> None:
        points = self.__load_data()
        self.clear_set2()

        for i in range(0, len(points) - 1, 2):
            self.add_point_set2(points[i], points[i + 1])

        self.canvas.clear()
        self.canvas.plot_points_auto_range(self.set1, 'r')
        self.canvas.plot_points_auto_range(self.set2, 'b')

    def __load_data(self) -> list[float]:
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Открыть файл", "", #"Text files (*.txt);;CSV files (*.csv)"
        )
        if file_name == "":
            return []
        
        float_data = []
        try:
            with open(file_name, "r") as f:
                data = f.read()
            float_data = list(map(float, data.split()))
        except:
            self.show_error_message("Ошибка чтения файла", "Произошла ошибка во время открытия или чтения файла")
        
        return float_data

    def save_set1(self) -> None:
        self.__save_points(self.set1)

    def save_set2(self) -> None:
        self.__save_points(self.set2)

    def __save_points(self, points: set) -> None:
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "")
        if file_name == "":
            return

        try:
            file = open(file_name, "w")
            for point in points:
                file.write(f"{point[0]} {point[1]}\n")
            file.close()
        except:
            self.show_error_message("Ошибка записи", "Произошла ошибка во время записи данных в файл")

    def show_manual(self) -> None:
        if self.manualWidget.isVisible():
            self.manualWidget.hide()
            self.taskWidget.hide()
            self.canvas.show()
        else:
            self.manualWidget.show()
            self.taskWidget.hide()
            self.canvas.hide()

    def show_task(self) -> None:
        if self.taskWidget.isVisible():
            self.manualWidget.hide()
            self.taskWidget.hide()
            self.canvas.show()
        else:
            self.taskWidget.show()
            self.manualWidget.hide()
            self.canvas.hide()

    def clear_set1(self) -> None:
        self.set1.clear()
        self.table_set1.setRowCount(0)

    def clear_set2(self) -> None:
        self.set2.clear()
        self.table_set2.setRowCount(0)

    def clear_all(self) -> None:
        self.canvas.clear()
        self.clear_set1()
        self.clear_set2()

    def show_error_message(self, title: str, message: str) -> None:
        QMessageBox.warning(self, title, message)
        