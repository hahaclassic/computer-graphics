from PyQt6.QtWidgets import QMainWindow, QMessageBox, \
    QPushButton, QLabel, QGraphicsView, QGraphicsScene, QTextEdit
from PyQt6.QtGui import QColor, QTransform, QMouseEvent, QPolygon
from PyQt6.QtCore import Qt, QPointF, QPoint, QLine, QLineF
from PyQt6 import uic
import src.cut_segment as cut
import time


class Interface(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi('ui/mainwindow.ui', self)

        self.polygon = QPolygon()
        self.is_closed = False
        self.segments: list[QLine] = []
        self.curr_segment: QLine = None
        self.segment_color = QColor(0, 0, 0)
        self.result_color = QColor(255, 0, 0)
        self.polygon_color = QColor(0, 0, 255)
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
        self.close_polygon_button = self.findChild(
            QPushButton, 'closeShapeBtn')
        self.add_point_button = self.findChild(QPushButton, 'addPointBtn')
        self.clear_button = self.findChild(QPushButton, 'clearBtn')
        self.clear_polygon_button = self.findChild(
            QPushButton, 'deleteShapeBtn')

        self.cut_button.clicked.connect(self.cut)
        self.add_segment_button.clicked.connect(self.add_segment)
        self.close_polygon_button.clicked.connect(self.close_polygon)
        self.add_point_button.clicked.connect(self.add_polygon_point)
        self.clear_button.clicked.connect(self.clear)
        self.clear_polygon_button.clicked.connect(self.clear_polygon)

    def __setup_input_fields(self) -> None:
        self.start_x = self.findChild(QTextEdit, 'startX')
        self.start_y = self.findChild(QTextEdit, 'startY')
        self.end_x = self.findChild(QTextEdit, 'endX')
        self.end_y = self.findChild(QTextEdit, 'endY')
        self.point_x = self.findChild(QTextEdit, 'point_x')
        self.point_y = self.findChild(QTextEdit, 'point_y')

    def cut(self) -> None:
        ok = self.check_input_params()
        if not ok:
            return

        start = time.monotonic()
        for seg in self.segments:
            cutted_seg, ok = cut.cyrus_beck(self.polygon, seg)
            if ok:
                self.draw_segment(cutted_seg, self.result_color)
        self.scene.update()
        end = time.monotonic()

        self.update_time_label(end - start)
        self.segments.clear()

    def check_input_params(self) -> bool:
        if len(self.segments) == 0:
            QMessageBox.warning(
                self, 'Ошибка', 'Введите хотя бы один отрезок.')
            return False
        if not self.is_closed:
            QMessageBox.warning(
                self, 'Ошибка', 'Замкните отсекатель (кол-во точек > 2)')
            return False
        if not cut.is_polygon_convex(self.polygon):
            QMessageBox.warning(
                self, 'Ошибка', 'Отсекатель должен быть выпуклым многоугольником!')
            return False

        return True

    def mousePressEvent(self, event: QMouseEvent) -> None:
        point = self.view.mapToScene(event.pos()).toPoint()
        if event.button() == Qt.MouseButton.RightButton:
            self.update_polygon(point)
        elif event.button() == Qt.MouseButton.LeftButton:
            if len(self.polygon) > 2:
                self.is_closed = True
            self.curr_segment = QLine()
            self.curr_segment.setP1(point)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        point = self.view.mapToScene(event.pos()).toPoint()
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.update_curr_segment(point)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        point = self.view.mapToScene(event.pos()).toPoint()
        if event.button() == Qt.MouseButton.LeftButton:
            self.curr_segment.setP2(point)
            self.segments.append(self.curr_segment)
            self.curr_segment = QLine()

    def close_polygon(self) -> None:
        if len(self.polygon) < 3:
            QMessageBox.warning(
                self, 'Ошибка', 'Добавьте еще хотя бы 1 вершину для отсекателя.')
            return
        self.is_closed = True
        self.draw_segment(QLine(
            self.polygon[0], self.polygon[-1]), self.polygon_color)
        self.scene.update()

    def update_polygon(self, new_point: QPoint) -> None:
        if self.is_closed:
            self.polygon.clear()
            self.is_closed = False
            self.update_scene()
        self.polygon.append(new_point)

        self.scene.addEllipse(
            new_point.x() - 2, new_point.y() - 2, 4, 4,
            self.polygon_color, self.polygon_color)

        if len(self.polygon) > 1:
            self.draw_segment(QLine(
                new_point, self.polygon[-2]), self.polygon_color)
            self.scene.update()

    def update_curr_segment(self, point: QPoint) -> None:
        self.update_scene()
        self.curr_segment.setP2(point)
        self.draw_segment(self.curr_segment, self.segment_color)

    def update_scene(self) -> None:
        self.scene.clear()
        self.draw_segments()
        self.draw_polygon()

    def draw_segments(self) -> None:
        for seg in self.segments:
            self.draw_segment(seg, self.segment_color)

    def draw_segment(self, segment: QLine, color: QColor) -> None:
        self.scene.addLine(segment.toLineF(), color)

    def draw_polygon(self) -> None:
        self.scene.addPolygon(self.polygon.toPolygonF(), self.polygon_color)
        self.scene.update()

    def add_polygon_point(self) -> None:
        try:
            point_x = float(self.point_x.toPlainText())
            point_y = float(self.point_y.toPlainText())
        except ValueError:
            QMessageBox.warning(
                self, 'Ошибка', 'Некорректные данные в полях ввода новой точки отсекателя')
            return

        self.update_polygon(QPointF(point_x, point_y).toPoint())

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

    def update_time_label(self, time: float) -> None:
        """Time in seconds."""
        self.time_label.setText(f'{time * 1000: .4f} мс')

    def clear(self) -> None:
        self.segments.clear()
        self.scene.clear()
        self.polygon.clear()

    def clear_polygon(self) -> None:
        self.polygon.clear()
        self.update_scene()
