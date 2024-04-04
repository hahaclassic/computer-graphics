from PyQt6.QtWidgets import QMainWindow, QMenu, QMenuBar, QFileDialog, QMessageBox, \
      QPushButton, QColorDialog, QLabel, QGraphicsView, QGraphicsScene, QTextEdit, QComboBox
from PyQt6.QtGui import QAction, QColor, QTransform
from PyQt6.QtCore import QPointF, QLineF
from PyQt6 import uic
import src.geometry as geo

class Interface(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui/mainwindow.ui", self)
        self.scene = QGraphicsScene()
        self.view = self.findChild(QGraphicsView, "graphicsView")
        self.view.setScene(self.scene)
        transform = QTransform()
        transform.scale(1, -1)
        self.view.setTransform(transform)

        self.background_color_button = self.findChild(QPushButton, "changeBackgroundColorBtn")
        self.background_color_button.clicked.connect(self.choose_background_color)
        self.background_color_label = self.findChild(QLabel, "backgroundColor")
        self.background_color = QColor(255, 255, 255)

        self.segment_color_button = self.findChild(QPushButton, "changeSegColorBtn")
        self.segment_color_button.clicked.connect(self.choose_segment_color)
        self.segment_color_label = self.findChild(QLabel, "segmentColor")
        self.segment_color = QColor(0, 0, 0)

        self.input_start_x = self.findChild(QTextEdit, "startCoordX")
        self.input_start_y = self.findChild(QTextEdit, "startCoordY")
        self.input_end_x = self.findChild(QTextEdit, "endCoordX")
        self.input_end_y = self.findChild(QTextEdit, "endCoordY")

        self.algorithm = self.findChild(QComboBox, "AlgorithmTypeBox")
        
        self.plot_segment_button = self.findChild(QPushButton, "plotSegmentBtn")
        self.plot_segment_button.clicked.connect(self.plot_segment)

    def choose_background_color(self):
        color_dialog = QColorDialog(self)
        if color_dialog.exec():
            self.background_color = color_dialog.currentColor()
            self.background_color_label.setStyleSheet(
                f"background-color: {self.background_color.name()}"
            )
            self.view.setBackgroundBrush(self.background_color)
        
    def choose_segment_color(self):
        color_dialog = QColorDialog(self)
        if color_dialog.exec():
            self.segment_color = color_dialog.currentColor()
            self.segment_color_label.setStyleSheet(
                f"background-color: {self.segment_color.name()}"
            )

    def get_points(self) -> tuple[QPointF, QPointF]:
        try:
            start_x = float(self.input_start_x.toPlainText())
            start_y = float(self.input_start_y.toPlainText())
            end_x = float(self.input_end_x.toPlainText())
            end_y = float(self.input_end_y.toPlainText())
        except ValueError:
            return

        return QPointF(start_x, start_y), QPointF(end_x, end_y)

    def plot_segment(self):
        start, end = self.get_points()

        match self.algorithm.currentIndex():
            case 0:
                geo.float_bresenham(self.scene, self.segment_color, start, end)

            case 1:
                geo.int_bresenham(self.scene, self.segment_color, start, end)

            case 3:
                geo.digital_differential_analyzer(self.scene, self.segment_color, start, end)

            case 5: # "Алгоритм, использующий библиотечную функцию":
                line = QLineF(start, end)
                self.scene.addLine(line, self.segment_color)
                