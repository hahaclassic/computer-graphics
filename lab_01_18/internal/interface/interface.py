import sys, os
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, \
    QGridLayout, QTextEdit, QLabel, QMenu, QMenuBar, QFileDialog
from PyQt6.QtGui import QIcon, QAction,QPen
from PyQt6.QtCore import Qt, QRect, QSize, QPointF, QLineF, QRectF
import pyqtgraph as pg

from ..process import process

class CoordinateInputField(QTextEdit):
    def __init__(self, parent):
        super().__init__(parent)

    def data(self) -> list[tuple[float, float]]:
        coordinates = self.toPlainText().split()
        points = set()
        for i in range(0, len(coordinates) - 1, 2):
            points.add((coordinates[i], coordinates[i + 1]))
        return points
    
class MenuBar(QMenuBar):
    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent)

        self.file_actions = QMenu("Файл", parent)
        self.import_data = QAction("Импортировать данные", parent)
        self.export_data = QAction("Экспортировать данные", parent)
        self.file_actions.addAction(self.import_data)
        self.file_actions.addAction(self.export_data)

        self.task_condition = QAction("Условие", parent)
        self.manual = QAction("Инструкция", parent)

        self.import_data.triggered.connect(self.import_data_clicked)
        self.export_data.triggered.connect(self.export_data_clicked)
        self.manual.triggered.connect(self.show_manual)
        self.task_condition.triggered.connect(self.show_task_cond)

        self.addMenu(self.file_actions)
        self.addAction(self.task_condition)
        self.addAction(self.manual)

    # Возможно, стоит перенести в функции главного окна
    def import_data_clicked(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Открыть файл", "", #"Text files (*.txt);;CSV files (*.csv)"
        )
        if file_name:
            print(f"Selected file: {file_name}")

    def export_data_clicked(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Сохранить файл", "", #"Text files (*.txt);;CSV files (*.csv)"
        )
        if file_name:
            print(f"Selected file: {file_name}")

    def show_manual(self):
        print("manual")

    def show_task_cond(self):
        print("task condition")
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title and icon
        self.setWindowTitle('PyQt6 Example')
        self.setWindowIcon(QIcon('icon.png'))
        self.setMinimumSize(640,400)

        self.coordinateGrid = pg.PlotWidget()
        
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)

        # Create labels
        label1, label2 = QLabel(self), QLabel(self)
        label1.setText("Set A")
        label2.setText("Set B")
        
        # Create output field
        self.output_field = QLabel(self)

        # Create two input fields
        self.input_field1 = CoordinateInputField(self)
        self.input_field1.setFixedWidth(100)
        self.input_field2 = CoordinateInputField(self)
        self.input_field2.setFixedWidth(100)

        # Create two buttons
        button_calc = QPushButton('calc', self)
        button_calc.setFixedSize(QSize(100,20))
        button_clear = QPushButton('clear', self)
        button_clear.setFixedSize(QSize(100,20))

        # Connect button click signals to slot functions
        button_calc.clicked.connect(self.calcucate)
        button_clear.clicked.connect(self.clear)

        # Create a QGridLayout
        layout = QGridLayout()
    
        # Add QGraphicsView to the layout
        layout.addWidget(self.coordinateGrid, 0, 0, 3, 2)

        # Add labels
        layout.addWidget(label1, 0, 2, 1, 1)
        layout.addWidget(label2, 0, 3, 1, 1)
        layout.addWidget(self.output_field, 3, 0, 2, 1)

        # Add input fields to the layout
        layout.addWidget(self.input_field1, 1, 2, 1, 1)
        layout.addWidget(self.input_field2, 1, 3, 1, 1)

        # Add buttons to the layout
        layout.addWidget(button_calc, 3, 2)
        layout.addWidget(button_clear, 3, 3)

        # Set the layout for the main window
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)    

    def calcucate(self):
        set1, set2 = self.get_points()
        max_area, cicle1, cicle2 = process.find_max_area(set1, set2)
        tangent_p1, tangent_p2 = process.tangent_coordinates(cicle1, cicle2)


        self.output_field.setText(f"S = {max_area:.3f}, cicle1 = {cicle1}, cicle2 = {cicle2}")
        
        self.scene.addEllipse(cicle1.center()[0], cicle1.center()[1], 
                              cicle1.radius(), cicle1.radius(), QPen(Qt.GlobalColor.red))
        self.scene.addEllipse(cicle2.center()[0], cicle2.center()[1], 
                              cicle2.radius(), cicle2.radius(), QPen(Qt.GlobalColor.blue))
        self.scene.addLine(QLineF(tangent_p1[0], tangent_p1[1], tangent_p2[0], tangent_p2[1]), Qt.GlobalColor.white)
        self.scene.addLine(QLineF(cicle1.center()[0], cicle1.center()[1], cicle2.center()[0], cicle2.center()[1]), \
                Qt.GlobalColor.white)

    def clear(self):
        self.view.delete_points()
        self.input_field1.clear()
        self.input_field2.clear()

    def get_points(self):
        points_set1, points_set2 = self.view.points()
        points = self.input_field1.data()
        for p in points:
            points_set1.add(p)
        points = self.input_field2.data()
        for p in points:
            points_set2.add(p)
        print("set A")
        for p in points_set1:
            print(p)
        print("set B")
        for p in points_set2:
            print(p)
        return points_set1, points_set2
        