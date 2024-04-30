from PyQt6.QtWidgets import QMainWindow, QMessageBox, QTextEdit, \
    QPushButton, QColorDialog, QLabel, QGraphicsView, QGraphicsScene, QCheckBox
from PyQt6.QtGui import QColor, QMouseEvent, QTransform, QPolygon
from PyQt6.QtCore import Qt, QPointF, QPoint, QLine
from PyQt6 import uic
import src.draw as draw
import time


class Interface(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/mainwindow.ui', self)

        self.curr_figure: QPolygon = QPolygon()
        self.seed_point: QPoint = None

        self.background_color_label = self.findChild(QLabel, 'backgroundColor')
        self.background_color = QColor(255, 255, 255)
        self.pen_color_label = self.findChild(QLabel, 'PenColor')
        self.pen_color = QColor(0, 0, 0)

        self.with_delay: QCheckBox = self.findChild(QCheckBox, 'checkBox')
        self.time_label = self.findChild(QLabel, 'timeLabel')

        self.__setup_input_fields()
        self.__setup_scene()
        self.__setup_buttons()

    def __setup_input_fields(self):
        self.input_point_x = self.findChild(QTextEdit, 'pointX')
        self.input_point_y = self.findChild(QTextEdit, 'pointY')
        self.input_seed_x = self.findChild(QTextEdit, 'seedX')
        self.input_seed_y = self.findChild(QTextEdit, 'seedY')

        self.ellipse_center_x = self.findChild(QTextEdit, 'ellipseCenterX')
        self.ellipse_center_y = self.findChild(QTextEdit, 'ellipseCenterY')
        self.ellipse_semi_major_axis = self.findChild(QTextEdit, 'bigAxis')
        self.ellipse_semi_minor_axis = self.findChild(QTextEdit, 'smallAxis')

    def __setup_scene(self):
        self.scene = QGraphicsScene()
        self.view = self.findChild(QGraphicsView, 'graphicsView')
        self.view.setScene(self.scene)
        transform = QTransform()
        transform.scale(1, -1)
        self.view.setTransform(transform)
        self.view.mouseReleaseEvent = self.mouseReleaseEvent
        self.view.mouseMoveEvent = self.mouseMoveEvent
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

        self.add_point_button = self.findChild(QPushButton, 'addPointBtn')
        self.add_point_button.clicked.connect(self.get_point_data)
        self.add_seed_button = self.findChild(QPushButton, 'addSeedBtn')
        self.add_seed_button.clicked.connect(self.get_seed_data)
        self.draw_ellipse_button = self.findChild(QPushButton, 'addEllipseBtn')
        self.draw_ellipse_button.clicked.connect(self.draw_ellipse)

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
        if self.seed_point is None:
            QMessageBox.warning(self, 'Ошибка',
                                'Выберите затравку.')
            return
        if self.pen_color == self.background_color:
            QMessageBox.warning(self, 'Ошибка',
                                'Цвет фона не должен соответствовать цвету рисования!')
            return
        delay = 0.0
        if self.with_delay.checkState() == Qt.CheckState.Checked:
            delay = 0.0001

        fill = draw.FillParameters(self.scene, self.pen_color)

        start = time.monotonic()
        draw.fill_figure_with_seed_point(fill, self.seed_point, delay)
        end = time.monotonic()

        self.update_time_label(end - start)
        self.seed_point = None

    def close_shape(self):
        if len(self.curr_figure) == 0:
            return
        draw.draw_line(self.scene, QLine(
            self.curr_figure[0], self.curr_figure[-1]), self.pen_color)

        self.curr_figure = QPolygon()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() & Qt.MouseButton.LeftButton:
            point = self.view.mapToScene(event.pos()).toPoint()
            self.add_point(point)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        point = self.view.mapToScene(event.pos()).toPoint()
        if event.button() == Qt.MouseButton.LeftButton:
            self.add_point(point)
        elif event.button() == Qt.MouseButton.RightButton:
            self.update_seed_point(point)

    def get_point_data(self) -> None:
        try:
            x = float(self.input_point_x.toPlainText())
            y = float(self.input_point_y.toPlainText())
        except ValueError:
            QMessageBox.warning(
                self, 'Ошибка', 'Некорректные данные в полях ввода точки.')
            return

        self.add_point(QPointF(x, y).toPoint())

    def get_seed_data(self) -> None:
        try:
            x = float(self.input_seed_x.toPlainText())
            y = float(self.input_seed_y.toPlainText())
        except ValueError:
            QMessageBox.warning(
                self, 'Ошибка', 'Некорректные данные в полях ввода затравки.')
            return

        self.update_seed_point(QPointF(x, y).toPoint())

    def add_point(self, point: QPoint):
        self.curr_figure.append(point)
        self.update_scene(point)

    def update_scene(self, new_point: QPoint):
        self.scene.addEllipse(
            new_point.x() - 1, new_point.y() - 1, 2, 2, self.pen_color, self.pen_color)

        if len(self.curr_figure) > 1:
            draw.draw_line(self.scene, QLine(
                new_point, self.curr_figure[-2]), self.pen_color)

    def update_time_label(self, time: float):
        """Time in seconds."""
        self.time_label.setText(f'{time * 1000: .4f} мс')

    def update_seed_point(self, point: QPoint):
        self.seed_point = point
        self.scene.addEllipse(
            point.x() - 2, point.y() - 2, 5, 5,
            QColor('red'), QColor('red'))

    def get_ellipse_data(self) -> tuple[draw.Ellipse, bool]:
        try:
            center_x = float(self.ellipse_center_x.toPlainText())
            center_y = float(self.ellipse_center_y.toPlainText())
            semi_major_axis = float(self.ellipse_semi_major_axis.toPlainText())
            semi_minor_axis = float(self.ellipse_semi_minor_axis.toPlainText())
        except ValueError:
            QMessageBox.warning(
                self, 'Ошибка', 'Некорректные данные в полях ввода эллипса')
            return draw.Ellipse(), False

        center = QPointF(center_x, center_y)
        return draw.Ellipse(center, semi_major_axis, semi_minor_axis), True

    def draw_ellipse(self):
        ellipse, ok = self.get_ellipse_data()
        if not ok:
            return

        draw.draw_ellipse_build_in(self.scene, ellipse, self.pen_color)

    def clear(self):
        self.scene.clear()
        self.curr_figure.clear()
