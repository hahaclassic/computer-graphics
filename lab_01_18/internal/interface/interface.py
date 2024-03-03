import sys, os
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, \
    QGridLayout, QTextEdit, QLabel, QMenu, QMenuBar, QFileDialog, QTableWidget, QTableWidgetItem, QCheckBox
from PyQt6.QtGui import QIcon, QAction,QPen, QFont
from PyQt6.QtCore import Qt, QRect, QSize, QPointF, QLineF, QRectF
import pyqtgraph as pg

import math
from ..process import process
import internal.interface.setup as setup

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

        self.import_set1.triggered.connect(parent.load_set1) #lambda: parent.load_points(parent.set1)
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

        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(["X", "Y"])
        self.setFixedWidth(200)
    
    def insertPoint(self, x: float, y: float):
        self.insertRow(self.rowCount())
        self.setItem(self.rowCount() - 1, 0, QTableWidgetItem(str(x)))
        self.setItem(self.rowCount() - 1, 1, QTableWidgetItem(str(y)))

    def deletePoint(self, x: float, y: float):
        n = self.rowCount()
        for i in range(n):
            if math.fabs(float(self.item(i, 0).text()) - x) < 1e07 \
                and math.fabs(float(self.item(i, 1).text()) - y) < 1e07:
                self.removeRow(i)
                break

class Canvas(pg.PlotWidget):
    def __init__(self, parent: QMainWindow):
        super().__init__(parent)
        self.showGrid(x=True, y=True)
        self.setXRange(0, 10)
        self.setYRange(0,10)
        self.setAspectLocked()
        self.parent = parent
        self.setMinimumSize(QSize(400,400))

    def mousePressEvent(self, ev):
        if ev.button() == Qt.MouseButton.MiddleButton:
            return super().mousePressEvent(ev)
        elif ev.button() == Qt.MouseButton.LeftButton and \
            ev.modifiers() & Qt.KeyboardModifier.ControlModifier:
            return self.delete_point(ev.pos())

        pos = ev.pos()
        grid_pos = self.getViewBox().mapSceneToView(QPointF(pos))
        x, y = round(grid_pos.x(), 3), round(grid_pos.y(), 3)
    
        if ev.button() == Qt.MouseButton.LeftButton:
            self.plot_point(x, y, 'r')
            self.parent.add_point_set1(x, y)
        elif ev.button() == Qt.MouseButton.RightButton:
            self.plot_point(x, y, 'b')
            self.parent.add_point_set2(x, y)

    def plot_point(self, x: float, y: float, color: str):
        scatter = pg.ScatterPlotItem(pen=color, x=[x], y=[y], brush=color, symbol='o')
        self.addItem(scatter)
 
    def plot_points(self, points: set, color: str):
        x = list(map(lambda point: point[0], points))
        y = list(map(lambda point: point[1], points))
        scatter = pg.ScatterPlotItem(pen=color, x=x, y=y, brush=color, symbol='o')
        self.addItem(scatter)
        self.getViewBox().autoRange()

    def delete_point(self, pos):
        isExist = False

        for x_start in range(pos.x() - 5, pos.x() + 5):
            for y_start in range(pos.y() - 5, pos.y() + 5):
                grid_pos = self.getViewBox().mapSceneToView(QPointF(x_start, y_start))
                x, y = round(grid_pos.x(), 3), round(grid_pos.y(), 3)

                if (x,y) in self.parent.set1:
                    isExist = True
                    self.parent.delete_point_set1(x, y)
                    break
                elif (x,y) in self.parent.set2:
                    isExist = True
                    self.parent.delete_point_set2(x,y)
                    break
            if isExist:
                self.clear()
                self.plot_points(self.parent.set1, 'r')
                self.plot_points(self.parent.set2, 'b')
                break

    def plot_line(self, start: tuple[float, float], end: tuple[float, float], color):
        x = [start[0], end[0]]
        y = [start[1], end[1]]

        line = pg.PlotDataItem(pen=color, x=x, y=y, brush=color)
        self.addItem(line)
        self.getViewBox().autoRange()

    def plot_cicle(self, center1, r1, center2, r2):
        x1,y1 = center1[0] - r1, center1[1] - r1
        x2,y2 = center2[0] - r2, center2[1] - r2
        cicle1 = pg.CircleROI(pen='g', pos=(x1,y1), radius=r1)
        cicle2 = pg.CircleROI(pen='g', pos=(x2,y2), radius=r2)

        self.addItem(cicle1)
        self.addItem(cicle2)
        self.getViewBox().autoRange()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        ### Buisness logic
        self.set1 = set()
        self.set2 = set()

        # Set window title and icon
        self.setWindowTitle('PyQt6 Example')
        self.setWindowIcon(QIcon('icon.png'))
        self.setMinimumSize(850,440)
        
        self.manual = setup.read_manual()
        self.manualWidget = QLabel(self.manual)
        self.manualWidget.hide()

        self.task = setup.read_task()
        self.taskWidget = QLabel(self.task)
        self.taskWidget.hide()

        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)


        self.canvas = Canvas(self)

        # Create table labels
        table_label1, table_label2 = QLabel(self), QLabel(self)
        table_label1.setText("Множество A")
        table_label2.setText("Множество B")

        # Create input fields labels
        label_x, label_y = QLabel(self), QLabel(self)
        label_x.setText("X")
        label_y.setText("Y") 

        # Create input fields
        self.input_field_x = QTextEdit(self)
        self.input_field_x.setFixedSize(QSize(170, 50))
        self.input_field_y = QTextEdit(self)
        self.input_field_y.setFixedSize(QSize(170, 50))

        self.check_box_set1 = QCheckBox("В множество А", self)
        self.check_box_set2 = QCheckBox("В множество B", self)

        self.check_box_set1.setChecked(True)
        self.check_box_set1.stateChanged.connect(lambda state: self.check_box_set2.setChecked(not state))
        self.check_box_set2.stateChanged.connect(lambda state: self.check_box_set1.setChecked(not state))

        # Create output field
        #self.output_field = QLabel(self)

        # Create point tables
        self.table_set1 = PointsTable(self)
        self.table_set2 = PointsTable(self)

        # Create buttons
        button_calc = QPushButton('Найти решение', self)
        #button_calc.setFixedSize(QSize(100,20))
        button_clear = QPushButton('Очистить', self)
        #button_clear.setFixedSize(QSize(100,20))
        button_add_point = QPushButton('Добавить точку', self)

        # Connect button click signals to slot functions
        button_calc.clicked.connect(self.calcucate)
        button_add_point.clicked.connect(self.get_point_from_input_fields)
        button_clear.clicked.connect(self.clear_all)

        # Create a QGridLayout
        self.layoutWidget = QGridLayout()
    
        self.layoutWidget.addWidget(self.canvas, 0, 0, 10, 2)
        self.layoutWidget.addWidget(self.manualWidget, 0, 0, 8, 2)
        self.layoutWidget.addWidget(self.taskWidget, 0, 0, 3, 2)

        # Add tables to the layout
        self.layoutWidget.addWidget(self.table_set1, 1, 2, 4, 1)
        self.layoutWidget.addWidget(self.table_set2, 1, 3, 4, 1)

        # Add labels
        self.layoutWidget.addWidget(table_label1, 0, 2, 1, 1)
        self.layoutWidget.addWidget(table_label2, 0, 3, 1, 1)

        self.layoutWidget.addWidget(label_x, 5, 2, 1, 1)
        self.layoutWidget.addWidget(label_y, 5, 3, 1, 1)

        # Add input fields
        self.layoutWidget.addWidget(self.input_field_x, 6, 2, 1, 1)
        self.layoutWidget.addWidget(self.input_field_y, 6, 3, 1, 1)

        self.layoutWidget.addWidget(self.check_box_set1, 7, 2, 1, 1)
        self.layoutWidget.addWidget(self.check_box_set2, 7, 3, 1, 1)

        # Add buttons to the layout
        self.layoutWidget.addWidget(button_add_point, 8, 2, 1, 2)
        self.layoutWidget.addWidget(button_calc, 9, 3)
        self.layoutWidget.addWidget(button_clear, 9, 2)

        # Set the layout for the main window
        central_widget = QWidget()
        central_widget.setLayout(self.layoutWidget)
        self.setCentralWidget(central_widget)    

    def calcucate(self):
        max_area, cicle1, cicle2 = process.find_max_area(self.set1, self.set2)
        tangent_p1, tangent_p2 = process.tangent_coordinates(cicle1, cicle2)
        self.canvas.plot_line(tangent_p1, tangent_p2, 'g')
        self.canvas.plot_line(cicle1.center(), cicle2.center(), 'g')

        self.canvas.plot_line(tangent_p1, cicle1.center(), 'g')
        self.canvas.plot_line(tangent_p2, cicle2.center(), 'g')
        
        self.canvas.plot_line(cicle1.center(), cicle2.center(), 'g')
        self.canvas.plot_cicle(cicle1.center(), cicle1.radius(), cicle2.center(), cicle2.radius())
        print(tangent_p1, tangent_p2)
        print(cicle1, cicle2)


    def add_point_set1(self, x: float, y: float):
        rounded_x, rounded_y = round(x, 3), round(y, 3) 
        self.set1.add((rounded_x, rounded_y))
        self.table_set1.insertPoint(rounded_x, rounded_y)

    def add_point_set2(self, x: float, y: float):
        rounded_x, rounded_y = round(x, 3), round(y, 3) 
        self.set2.add((rounded_x, rounded_y))
        self.table_set2.insertPoint(rounded_x, rounded_y)

    def get_point_from_input_fields(self):
        x = float(self.input_field_x.toPlainText())
        y = float(self.input_field_y.toPlainText())

        if self.check_box_set1.checkState() == Qt.CheckState.Checked:
            self.add_point_set1(x,y)
            self.canvas.plot_point(round(x, 3), round(y, 3), 'r')
        else:
            self.add_point_set2(x,y)
            self.canvas.plot_point(round(x, 3), round(y, 3), 'b')

        self.input_field_x.clear()
        self.input_field_y.clear()

    def delete_point_set1(self, x: float, y: float):
        rounded_x, rounded_y = round(x, 3), round(y, 3) 
        self.set1.remove((rounded_x, rounded_y))
        self.table_set1.deletePoint(rounded_x, rounded_y)
    
    def delete_point_set2(self, x: float, y: float):
        rounded_x, rounded_y = round(x, 3), round(y, 3) 
        self.set2.remove((rounded_x, rounded_y))
        self.table_set2.deletePoint(rounded_x, rounded_y)

    def load_set1(self):
        points = self.load_data()
        self.clear_set1()

        for i in range(0, len(points) - 1, 2):
            self.add_point_set1(points[i], points[i + 1])

        self.canvas.clear()
        self.canvas.plot_points(self.set1, 'r')
        self.canvas.plot_points(self.set2, 'b')

    def load_set2(self):
        points = self.load_data()
        self.clear_set2()

        for i in range(0, len(points) - 1, 2):
            self.add_point_set2(points[i], points[i + 1])

        self.canvas.clear()
        self.canvas.plot_points(self.set1, 'r')
        self.canvas.plot_points(self.set2, 'b')

    def load_data(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Открыть файл", "", #"Text files (*.txt);;CSV files (*.csv)"
        )
        with open(file_name, "r") as f:
            data = f.read()
        float_data = list(map(float, data.split()))
        
        return float_data

        # TODO: Добавить исключения при чтении из файла и обработку корректности данных

    def save_set1(self):
        self.save_points(self.set1)

    def save_set2(self):
        self.save_points(self.set2)

    def save_points(self, points: set):
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "")

        file = open(file_name, "w")
        for point in points:
            file.write(f"{point[0]} {point[1]}\n")
        file.close()

        # TODO: Добавить исключения при записи в файл

    def show_manual(self):
        if self.manualWidget.isVisible():
            self.manualWidget.hide()
            self.taskWidget.hide()
            self.canvas.show()
        else:
            self.manualWidget.show()
            self.taskWidget.hide()
            self.canvas.hide()

    def show_task(self):
        if self.taskWidget.isVisible():
            self.manualWidget.hide()
            self.taskWidget.hide()
            self.canvas.show()
        else:
            self.taskWidget.show()
            self.manualWidget.hide()
            self.canvas.hide()

    def clear_set1(self):
        self.set1.clear()
        self.table_set1.setRowCount(0)

    def clear_set2(self):
        self.set2.clear()
        self.table_set2.setRowCount(0)

    def clear_all(self):
        self.canvas.clear()
        self.clear_set1()
        self.clear_set2()