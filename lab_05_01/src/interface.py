from PyQt6.QtWidgets import QMainWindow, QMessageBox, \
    QPushButton, QColorDialog, QLabel, QGraphicsView, QGraphicsScene, QTextEdit, QComboBox, QCheckBox
from PyQt6.QtGui import QColor, QTransform, QPolygon
from PyQt6.QtCore import Qt, QChildEvent, QPointF, QPoint, QLine
from PyQt6 import uic
import src.draw as draw


class Interface(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/mainwindow.ui', self)

        self.figures: list[QPolygon] = []
        self.curr_figure: list[QPoint] = []

        # self.circle_plotter = draw.CirclePlotter(self.scene)
        # self.ellipse_plotter = draw.EllipsePlotter(self.scene)

        self.background_color_label = self.findChild(QLabel, 'backgroundColor')
        self.background_color = QColor(255, 255, 255)
        self.pen_color_label = self.findChild(QLabel, 'PenColor')
        self.pen_color = QColor(0, 0, 0)

        self.with_delay: QCheckBox = self.findChild(QCheckBox, "checkBox")
        self.time_label = self.findChild(QLabel, "timeLabel")

        self.__setup_scene()
        self.__setup_buttons()

    def __setup_scene(self):
        self.scene = QGraphicsScene()
        self.view = self.findChild(QGraphicsView, 'graphicsView')
        self.view.setScene(self.scene)
        transform = QTransform()
        transform.scale(1, -1)
        self.view.setTransform(transform)
        self.view.mousePressEvent = self.add_point
        self.scene.setSceneRect(0, 0, 831, 873)

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
        self.clear_button.clicked.connect(self.clear)

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
                f'background-color: {self.pen_color.name()}'
            )

    def paint_shape(self):
        if len(self.figures) == 0:
            QMessageBox.warning(self, 'Ошибка', 'Нет ни одной замкнутой фигуры!')
            return
        delay = 0.0
        if self.with_delay.checkState() == Qt.CheckState.Checked:
            delay = 0.001

        draw.CAP_algorithm_with_ordered_list_of_edges(self.scene, self.figures, self.pen_color, delay)
        self.figures.clear()

    def close_shape(self):
        self.scene.addLine(QLine(self.curr_figure[0], self.curr_figure[-1]).toLineF(), self.pen_color)
        self.figures.append(self.curr_figure.copy())
        self.curr_figure.clear()

    # def mousePressEvent(self, event):
    #     if event.button() == Qt.MouseButton.LeftButton:
    #         pos = self.view.mapToScene(event.pos())
    #         point = QPointF(pos.x(), pos.y()).toPoint()
    #         self.points.append(point)
    #         self.scene.addEllipse(point.x(), point.y(), 5, 5, self.pen_color, self.pen_color)

    def add_point(self, event):
        if event.button() != Qt.MouseButton.LeftButton:
            return
        
        pos = self.view.mapToScene(event.pos())
        point = QPointF(pos.x(), pos.y()).toPoint()
        self.curr_figure.append(point)
        self.scene.addEllipse(point.x() - 2, point.y() - 2, 5, 5, self.pen_color, self.pen_color)

        if len(self.curr_figure) > 1:
            self.scene.addLine(QLine(point, self.curr_figure[-2]).toLineF(), self.pen_color)

    def clear(self):
        self.scene.clear()
        self.figures.clear()
        self.curr_figure.clear()