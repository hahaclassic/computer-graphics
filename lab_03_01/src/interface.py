from PyQt6.QtWidgets import QMainWindow, QMessageBox, \
      QPushButton, QColorDialog, QLabel, QGraphicsView, QGraphicsScene, QTextEdit, QComboBox
from PyQt6.QtGui import QColor, QTransform
from PyQt6.QtCore import QLineF
from PyQt6 import uic
import src.plot_algoritms as plot
import math

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

        self.plotter = plot.SegmentPlotter(self.scene)

        self.background_color_label = self.findChild(QLabel, "backgroundColor")
        self.background_color = QColor(255, 255, 255)
        self.segment_color_label = self.findChild(QLabel, "segmentColor")
        self.segment_color = QColor(0, 0, 0)

        self.algorithm = self.findChild(QComboBox, "AlgorithmTypeBox")
        self.__setup_buttons()
        self.__setup_input_fields()

    def __setup_input_fields(self):
        self.input_start_x = self.findChild(QTextEdit, "startCoordX")
        self.input_start_y = self.findChild(QTextEdit, "startCoordY")
        self.input_end_x = self.findChild(QTextEdit, "endCoordX")
        self.input_end_y = self.findChild(QTextEdit, "endCoordY")
        self.input_angle = self.findChild(QTextEdit, "angleInput")

    def __setup_buttons(self):
        self.background_color_button = self.findChild(QPushButton, "changeBackgroundColorBtn")
        self.background_color_button.clicked.connect(self.choose_background_color)

        self.segment_color_button = self.findChild(QPushButton, "changeSegColorBtn")
        self.segment_color_button.clicked.connect(self.choose_segment_color)
    
        self.plot_segment_button = self.findChild(QPushButton, "plotSegmentBtn")
        self.plot_segment_button.clicked.connect(self.plot_segment)

        self.plot_spectrum_button = self.findChild(QPushButton, "plotSpectrumBtn")
        self.plot_spectrum_button.clicked.connect(self.plot_spectrum)

        self.clear_button = self.findChild(QPushButton, "clearBtn")
        self.clear_button.clicked.connect(self.scene.clear)

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

    def get_segment(self) -> tuple[QLineF, bool]:
        try:
            start_x = float(self.input_start_x.toPlainText())
            start_y = float(self.input_start_y.toPlainText())
            end_x = float(self.input_end_x.toPlainText())
            end_y = float(self.input_end_y.toPlainText())
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Некорректные данные в полях ввода координат.")
            return QLineF(), False

        return QLineF(start_x, start_y, end_x, end_y), True
    
    def get_angle(self) -> tuple[float, bool]:
        try:
            angle = float(self.input_angle.toPlainText())
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Некорректные данные в поле ввода угла.")
            return 0, False
        
        return math.radians(angle), True

    def plot_segment(self):
        segment, ok = self.get_segment()
        if not ok:
            return
        
        algoritm = plot.Algorithm(self.algorithm.currentIndex())
        self.plotter.plot(algoritm, segment, self.segment_color)
        
    def plot_spectrum(self):
        segment, ok = self.get_segment()
        if not ok:
            return
        angle, ok = self.get_angle()
        if not ok:
            return
        
        algoritm = plot.Algorithm(self.algorithm.currentIndex())
        self.plotter.spectrum(algoritm, segment, self.segment_color, angle)
