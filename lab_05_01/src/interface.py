from PyQt6.QtWidgets import QMainWindow, QMessageBox, \
    QPushButton, QColorDialog, QLabel, QGraphicsView, QGraphicsScene, QTextEdit, QComboBox
from PyQt6.QtGui import QColor, QTransform
from PyQt6.QtCore import QPointF
from PyQt6 import uic
import src.draw as draw


class Interface(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/mainwindow.ui', self)
        self.scene = QGraphicsScene()
        self.view = self.findChild(QGraphicsView, 'graphicsView')
        self.view.setScene(self.scene)
        transform = QTransform()
        transform.scale(1, -1)
        self.view.setTransform(transform)
        self.view.mousePressEvent = self.add_point

        self.circle_plotter = draw.CirclePlotter(self.scene)
        self.ellipse_plotter = draw.EllipsePlotter(self.scene)

        self.background_color_label = self.findChild(QLabel, 'backgroundColor')
        self.background_color = QColor(255, 255, 255)
        self.pen_color_label = self.findChild(QLabel, 'PenColor')
        self.pen_color = QColor(0, 0, 0)

        self.__setup_buttons()

    def __setup_buttons(self):
        self.background_color_button = self.findChild(
            QPushButton, 'changeBackgroundColorBtn')
        self.background_color_button.clicked.connect(
            self.choose_background_color)
        self.pen_color_button = self.findChild(
            QPushButton, 'changePenColorBtn')
        self.pen_color_button.clicked.connect(self.choose_pen_color)

        self.paint_shape_button = self.findChild(QPushButton, 'paintShapeBtn')
        self.paint_shape_button.clicked.connect(self.paint_shape)

        self.close_shape_button = self.findChild(QPushButton, 'closeShapeBtn')
        self.close_shape_button.clicked.connect(self.close_shape)

        self.clear_button = self.findChild(QPushButton, 'clearBtn')
        self.clear_button.clicked.connect(self.scene.clear)

    def choose_background_color(self):
        color_dialog = QColorDialog(self)
        if color_dialog.exec():
            self.background_color = color_dialog.currentColor()
            self.background_color_label.setStyleSheet(
                f'background-color: {self.background_color.name()}'
            )
            self.view.setBackgroundBrush(self.background_color)

    def choose_pen_color(self):
        color_dialog = QColorDialog(self)
        if color_dialog.exec():
            self.pen_color = color_dialog.currentColor()
            self.pen_color_label.setStyleSheet(
                f'background-color: {self.segment_color.name()}'
            )

    def paint_shape(self):
        pass

    def close_shape(self):
        pass

    def add_point(self):
        pass
    