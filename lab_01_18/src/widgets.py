from PyQt6.QtWidgets import QWidget, QMainWindow, QPushButton, \
    QAbstractItemView, QGridLayout, QTextEdit, QLabel, QMenu, QMenuBar, \
    QFileDialog, QTableWidget, QTableWidgetItem, QCheckBox, QMessageBox, \
    QScrollArea, QVBoxLayout
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, QSize, QPointF
import pyqtgraph as pg

from src.circle import Circle

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
    # the parent must implement the functions:
    # load_set1(), load_set2(), save_set1(), save_set2()
    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent)

        self.file_actions = QMenu("Файл", parent)
        self.import_set1 = QAction("Импортировать множество точек А", parent)
        self.export_set1 = QAction("Экспортировать множество точек А", parent)
        self.import_set2 = QAction("Импортировать множество точек B", parent)
        self.export_set2 = QAction("Экспортировать множество точек B", parent)
        self.export_result = QAction("Экспортировать результат поиска", parent)

        self.task_condition = QAction("Условие", parent)
        self.manual = QAction("Инструкция", parent)

        self.import_set1.triggered.connect(parent.load_set1)
        self.export_set1.triggered.connect(parent.save_set1)
        self.import_set2.triggered.connect(parent.load_set2)
        self.export_set2.triggered.connect(parent.save_set2)
        self.export_result.triggered.connect(parent.save_result)
        self.manual.triggered.connect(parent.show_manual)
        self.task_condition.triggered.connect(parent.show_task)

        self.file_actions.addAction(self.import_set1)
        self.file_actions.addAction(self.export_set1)
        self.file_actions.addAction(self.import_set2)
        self.file_actions.addAction(self.export_set2)
        self.file_actions.addAction(self.export_result)
        self.addMenu(self.file_actions)
        self.addAction(self.task_condition)
        self.addAction(self.manual)
        
class PointsTable(QTableWidget):
    # the parent must implement the functions:
    # delete_point_set1(), delete_point_set2()
    def __init__(self, parent: QMainWindow, setIdx: int) -> None:
        super().__init__(parent)
        self.setIdx = setIdx 
        self.main_window = parent
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["X", "Y"])
        self.setFixedWidth(200)
        self.setMinimumHeight(200)
    
    def insert_point(self, point: QPointF) -> None:
        self.insertRow(self.rowCount())
        self.setItem(self.rowCount() - 1, 0, QTableWidgetItem(f"{point.x():.3f}"))
        self.setItem(self.rowCount() - 1, 1, QTableWidgetItem(f"{point.y():.3f}"))

    def contextMenuEvent(self, event) -> None:
        index = self.indexAt(event.pos())
        if not index.isValid():
            return
        
        row = index.row()
        reply = QMessageBox.question(self, 'Удалить точку?',
            f'Удалить точку №{row + 1}?', 
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.setIdx == 1:
                self.main_window.delete_point_set1(row)
            elif self.setIdx == 2: 
                self.main_window.delete_point_set2(row)
            self.main_window.canvas.clear()
            self.main_window.canvas.plot_points(self.main_window.set1, 'r')
            self.main_window.canvas.plot_points(self.main_window.set2, 'b')
        super().contextMenuEvent(event)

class Canvas(pg.PlotWidget):
    # the parent must implement the functions:
    # add_point_set1(), add_point_set2()
    # delete_point_set1(), delete_point_set2()
    # point_idx_set1(), point_idx_set2()
    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent)
        self.showGrid(x=True, y=True)
        self.setXRange(0, 12)
        self.setYRange(0,12)
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
        point = QPointF(grid_pos.x(), grid_pos.y())
    
        if ev.button() == Qt.MouseButton.LeftButton:
            self.plot_point(point, 'r')
            self.parent.add_point_set1(point)
        elif ev.button() == Qt.MouseButton.RightButton:
            self.plot_point(point, 'b')
            self.parent.add_point_set2(point)
        
    def delete_point(self, pos) -> None:
        isExist = False
        for x_start in range(pos.x() - 10, pos.x() + 10):
            for y_start in range(pos.y() - 10, pos.y() + 10):
                grid_pos = self.getViewBox().mapSceneToView(QPointF(x_start, y_start))

                point_idx = self.parent.point_idx_set1(grid_pos)
                if point_idx != -1:
                    self.parent.delete_point_set1(point_idx)
                    isExist = True
                    break

                point_idx = self.parent.point_idx_set2(grid_pos)
                if point_idx != -1:
                    self.parent.delete_point_set2(point_idx)
                    isExist = True
                    break
            if isExist:
                self.clear()
                self.plot_points(self.parent.set1, 'r')
                self.plot_points(self.parent.set2, 'b')
                break

    def plot_point(self, point: QPointF, color: str) -> None:
        scatter = pg.ScatterPlotItem(pen=color, x=[point.x()], y=[point.y()], brush=color, symbol='o')
        self.addItem(scatter)
 
    def plot_points(self, points: list[QPointF], color: str) -> None:
        x = list(map(lambda point: point.x(), points))
        y = list(map(lambda point: point.y(), points))
        scatter = pg.ScatterPlotItem(pen=color, x=x, y=y, brush=color, symbol='o')
        self.addItem(scatter)
        
    def plot_points_auto_range(self, points: list[QPointF], color: str) -> None:
        self.plot_points(points, color)
        self.getViewBox().autoRange()

    def plot_line(self, start: QPointF, end: QPointF, color) -> None:
        x = [start.x(), end.x()]
        y = [start.y(), end.y()]

        line = pg.PlotDataItem(pen=color, x=x, y=y, brush=color)
        self.addItem(line)
        self.getViewBox().autoRange()

    def plot_circle(self, circle: Circle, color: str) -> None:
        center, r = circle.center(), circle.radius()
        x1,y1 = center.x() - r, center.y() - r
        circle1 = pg.CircleROI(pen=color, pos=(x1,y1), radius=r)

        self.addItem(circle1)
        self.getViewBox().autoRange()

class MainWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__()

        self.setWindowTitle('Лабораторная работа №1')
        self.setMinimumSize(920,550)
        
        self.manualWidget = self.__setup_manual()
        self.taskWidget = self.__setup_task()

        self.menu_bar = MenuBar(parent)
        self.setMenuBar(self.menu_bar)
        self.canvas = Canvas(parent)

        self.result_label = QLabel("Результат:")
        self.output_field = QLabel(self)

        self.__setup_input_fields()
        self.__setup_tables()
        self.__setup_buttons()

        # Create a QGridLayout
        self.layoutWidget = self.__setup_layout()
    
        # Set the layout for the main window
        central_widget = QWidget()
        central_widget.setLayout(self.layoutWidget)
        self.setCentralWidget(central_widget)    

    def __setup_input_fields(self) -> None:
        self.label_x, self.label_y = QLabel(self), QLabel(self)
        self.label_x.setText("координата X")
        self.label_y.setText("координата Y") 

        self.input_field_x = QTextEdit(self)
        self.input_field_x.setFixedSize(QSize(200, 50))
        self.input_field_y = QTextEdit(self)
        self.input_field_y.setFixedSize(QSize(200, 50))

        self.check_box_set1 = QCheckBox("В множество А", self)
        self.check_box_set2 = QCheckBox("В множество B", self)

        self.check_box_set1.setChecked(True)
        self.check_box_set1.stateChanged.connect(lambda state: self.check_box_set2.setChecked(not state))
        self.check_box_set2.stateChanged.connect(lambda state: self.check_box_set1.setChecked(not state))

    def __setup_tables(self) -> None:
        self.table_set1_label, self.table_set2_label = QLabel(self), QLabel(self)
        self.table_set1_label.setText("Множество A")
        self.table_set2_label.setText("Множество B")
    
        self.table_set1 = PointsTable(self, 1)
        self.table_set2 = PointsTable(self, 2)

    def __setup_buttons(self) -> None:
        self.button_calc = QPushButton('Найти решение', self)
        self.button_calc.setStyleSheet("""QPushButton { 
            background-color: green; 
            color: black;
        }""")
        self.button_clear = QPushButton('Очистить плоскость', self)
        self.button_add_point = QPushButton('Добавить точку', self)

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
        except PermissionError or FileNotFoundError or IsADirectoryError:
            manual = "Произошла ошибка во время получения инструкции."

        manualWidget = ScrolledLabel(manual)
        manualWidget.hide()

        return manualWidget

    def __setup_task(self) -> QLabel:
        try:
            file = open(TASK_PATH, "r", encoding='utf-8')
            task = file.read()
            file.close()
        except PermissionError or FileNotFoundError or IsADirectoryError:
            task = "Произошла ошибка во время получения условия задачи."

        taskWidget = QLabel(task)
        taskWidget.hide()

        return taskWidget

    def load_data(self) -> list[float]:
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
        except PermissionError or FileNotFoundError or IsADirectoryError:
            self.show_error_message("Ошибка чтения файла", "Произошла ошибка во время открытия или чтения файла")
        
        return float_data

    def save_points(self, points: list[QPointF]) -> None:
        if len(points) == 0:
            self.show_error_message("Ошибка", "Множество пусто.")
            return
        
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "")
        if file_name == "":
            return
        
        with open(file_name, "w") as file:
            for point in points:
                file.write(f"{point.x()} {point.y()}\n")

    def save_result(self) -> None:
        if self.output_field.text() == "":
            self.show_error_message("Ошибка", "Нет результирующих данных.")
            return
    
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "")
        if file_name == "":
            return
        
        try:
            with open(file_name, "w") as file:
                file.write(self.output_field.text())
        except PermissionError or FileNotFoundError or IsADirectoryError: 
            self.show_error_message("Ошибка записи", "Произошла ошибка во время записи данных в файл.")

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

    def show_error_message(self, title: str, message: str) -> None:
        QMessageBox.warning(self, title, message)
