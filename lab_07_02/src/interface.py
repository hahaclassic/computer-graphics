from PyQt6.QtWidgets import QMainWindow, QMessageBox, \
    QPushButton, QLabel, QGraphicsView, QGraphicsScene, QTextEdit
from PyQt6.QtGui import QColor, QTransform, QMouseEvent
from PyQt6.QtCore import Qt, QPointF, QPoint, QLine, QRect, QLineF
from PyQt6 import uic
import src.cut_segment as cut
import time


class Interface(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi('ui/mainwindow.ui', self)

        self.rectangle: QRect = None
        self.segments: list[QLine] = []
        self.curr_segment: QLine = None
        self.segment_color = QColor(0, 0, 0)
        self.result_color = QColor(255, 0, 0)
        self.rect_color = QColor(0, 0, 255)
        self.time_label = self.findChild(QLabel, 'timeLabel')

        self.__setup_input_fields()
        self.__setup_scene()
        self.__setup_buttons()

    def __setup_scene(self) -> None:
        self.scene = QGraphicsScene()
        self.view = self.findChild(QGraphicsView, 'graphicsView')
        self.view.setScene(self.scene)
        transform = QTransform()
        transform.scale(1, -1)
        self.view.setTransform(transform)
        self.view.mousePressEvent = self.mousePressEvent
        self.view.mouseMoveEvent = self.mouseMoveEvent
        self.view.mouseReleaseEvent = self.mouseReleaseEvent
        self.scene.setSceneRect(0, 0, 831, 873)

    def __setup_buttons(self) -> None:
        self.cut_button = self.findChild(QPushButton, 'cutBtn')
        self.add_segment_button = self.findChild(QPushButton, 'addSegmentBtn')
        self.add_rectangle_button = self.findChild(QPushButton, 'addRectBtn')
        self.clear_button = self.findChild(QPushButton, 'clearBtn')

        self.cut_button.clicked.connect(self.cut)
        self.add_segment_button.clicked.connect(self.add_segment)
        self.add_rectangle_button.clicked.connect(self.add_rectangle)
        self.clear_button.clicked.connect(self.clear)

    def __setup_input_fields(self) -> None:
        self.start_x = self.findChild(QTextEdit, 'startX')
        self.start_y = self.findChild(QTextEdit, 'startY')
        self.end_x = self.findChild(QTextEdit, 'endX')
        self.end_y = self.findChild(QTextEdit, 'endY')
        self.rect_top_left_x = self.findChild(QTextEdit, 'rectTopX')
        self.rect_top_left_y = self.findChild(QTextEdit, 'rectTopY')
        self.rect_bottom_right_x = self.findChild(QTextEdit, 'rectBottomX')
        self.rect_bottom_right_y = self.findChild(QTextEdit, 'rectBottomY')

    def cut(self) -> None:
        if len(self.segments) == 0:
            QMessageBox.warning(
                self, 'Ошибка', 'Введите хотя бы один отрезок.')

        start = time.monotonic()
        for seg in self.segments:
            cutted_seg, ok = cut.cohen_sutherland(self.rectangle, seg)
            if ok:
                self.draw_segment(cutted_seg, self.result_color)
        self.scene.update()
        end = time.monotonic()

        self.update_time_label(end - start)
        self.segments.clear()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        point = self.view.mapToScene(event.pos()).toPoint()
        if event.button() == Qt.MouseButton.RightButton:
            self.rectangle = QRect(point, point)
        elif event.button() == Qt.MouseButton.LeftButton:
            self.curr_segment = QLine()
            self.curr_segment.setP1(point)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        point = self.view.mapToScene(event.pos()).toPoint()
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.update_curr_segment(point)
        elif event.buttons() & Qt.MouseButton.RightButton:
            self.update_rectangle(point)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        point = self.view.mapToScene(event.pos()).toPoint()
        if event.button() == Qt.MouseButton.LeftButton:
            self.curr_segment.setP2(point)
            self.segments.append(self.curr_segment)
            self.curr_segment = QLine()

    def update_curr_segment(self, point: QPoint) -> None:
        self.update_scene()
        self.curr_segment.setP2(point)
        self.draw_segment(self.curr_segment, self.segment_color)

    def update_rectangle(self, point: QPoint) -> None:
        self.rectangle.setBottomRight(point)
        self.update_scene()

    def update_scene(self):
        self.scene.clear()
        self.draw_segments()
        self.draw_rectangle()

    def draw_segments(self) -> None:
        for seg in self.segments:
            self.draw_segment(seg, self.segment_color)

    def draw_segment(self, segment: QLine, color: QColor) -> None:
        self.scene.addLine(segment.toLineF(), color)

    def draw_rectangle(self) -> None:
        if self.rectangle is None:
            return
        self.scene.addRect(self.rectangle.toRectF(), self.rect_color)
        self.scene.update()

    def add_segment(self) -> None:
        try:
            start_x = float(self.start_x.toPlainText())
            start_y = float(self.start_y.toPlainText())
            end_x = float(self.end_x.toPlainText())
            end_y = float(self.end_y.toPlainText())
        except ValueError:
            QMessageBox.warning(
                self, 'Ошибка', 'Некорректные данные в полях ввода отрезка')
            return

        self.segments.append(QLineF(start_x, start_y, end_x, end_y).toLine())
        self.update_scene()

    def add_rectangle(self) -> None:
        try:
            top_left_x = float(self.rect_top_left_x.toPlainText())
            top_left_y = float(self.rect_top_left_y.toPlainText())
            bottom_right_x = float(self.rect_bottom_right_x.toPlainText())
            bottom_right_y = float(self.rect_bottom_right_y.toPlainText())
        except ValueError:
            QMessageBox.warning(
                self, 'Ошибка', 'Некорректные данные в полях ввода отрезка')
            return

        top_left = QPointF(top_left_x, top_left_y).toPoint()
        bottom_right = QPointF(bottom_right_x, bottom_right_y).toPoint()
        self.rectangle = QRect(top_left, bottom_right)
        self.update_scene()

    def update_time_label(self, time: float) -> None:
        """Time in seconds."""
        self.time_label.setText(f'{time * 1000: .4f} мс')

    def clear(self) -> None:
        self.segments.clear()
        self.scene.clear()
        self.rectangle = None
