from PyQt6.QtWidgets import QMainWindow, QMessageBox, \
    QPushButton, QLabel, QGraphicsView, QGraphicsScene, QTextEdit
from PyQt6.QtGui import QColor, QTransform, QMouseEvent, QPolygon
from PyQt6.QtCore import Qt, QPointF, QPoint, QLine
from PyQt6 import uic
import src.cut_shapes as cut
import time


class Interface(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi('ui/mainwindow.ui', self)

        self.clipper = QPolygon()
        self.is_clipper_closed = False
        self.shapes: list[QPolygon] = []
        self.curr_shape: QPolygon = QPolygon()
        self.shape_color = QColor(0, 0, 0)
        self.result_color = QColor(255, 0, 0)
        self.clipper_color = QColor(0, 0, 255)
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
        self.clear_button = self.findChild(QPushButton, 'clearBtn')

        self.add_clipper_point_btn = self.findChild(
            QPushButton, 'addClipperPointBtn')
        self.add_shape_point_btn = self.findChild(
            QPushButton, 'addShapePointBtn')
        self.close_clipper_btn = self.findChild(QPushButton, 'closeClipperBtn')
        self.close_shape_btn = self.findChild(QPushButton, 'closeShapeBtn')
        self.delete_shapes_btn = self.findChild(QPushButton, 'deleteShapeBtn')
        self.delete_clipper_btn = self.findChild(
            QPushButton, 'deleteClipperBtn')

        self.add_clipper_point_btn.clicked.connect(self.add_clipper_point)
        self.add_shape_point_btn.clicked.connect(self.add_curr_shape_point)
        self.close_clipper_btn.clicked.connect(self.close_clipper)
        self.close_shape_btn.clicked.connect(self.close_curr_shape)
        self.delete_shapes_btn.clicked.connect(self.clear_shapes)
        self.delete_clipper_btn.clicked.connect(self.clear_clipper)

        self.cut_button.clicked.connect(self.cut)
        self.clear_button.clicked.connect(self.clear)

    def __setup_input_fields(self) -> None:
        self.clipper_point_x = self.findChild(QTextEdit, 'clipper_point_x')
        self.clipper_point_y = self.findChild(QTextEdit, 'clipper_point_y')
        self.shape_point_x = self.findChild(QTextEdit, 'shape_point_x')
        self.shape_point_y = self.findChild(QTextEdit, 'shape_point_y')

    def cut(self) -> None:
        if not self.check_input_params():
            return

        start = time.monotonic()
        for shape in self.shapes:
            cutted_shape, ok = cut.sutherland_hodgman(self.clipper, shape)
            if ok:
                self.draw_shape(cutted_shape, self.result_color)
                self.scene.update()

        self.scene.update()
        end = time.monotonic()

        self.update_time_label(end - start)
        self.shapes.clear()

    def check_input_params(self) -> bool:
        if len(self.shapes) == 0:
            QMessageBox.warning(
                self, 'Ошибка', 'Добавьте хотя бы одну фигуру для отсечения')
            return False
        if not self.is_clipper_closed:
            QMessageBox.warning(
                self, 'Ошибка', 'Замкните отсекатель (кол-во точек > 2)')
            return False
        if not cut.is_polygon_convex(self.clipper):
            QMessageBox.warning(
                self, 'Ошибка', 'Отсекатель должен быть выпуклым многоугольником!')
            return False

        return True

    def mousePressEvent(self, event: QMouseEvent) -> None:
        point = self.view.mapToScene(event.pos()).toPoint()
        if event.button() == Qt.MouseButton.RightButton:
            self.update_clipper(point)
        elif event.button() == Qt.MouseButton.LeftButton:
            self.update_curr_shape(point)

    def close_clipper(self) -> None:
        if len(self.clipper) < 3:
            QMessageBox.warning(
                self, 'Ошибка', 'Отсекатель должен содержать минимум 3 вершины.')
            return
        self.is_clipper_closed = True
        self.draw_segment(self.clipper[0], self.clipper[-1],
                          self.clipper_color)
        self.scene.update()

    def close_curr_shape(self) -> None:
        if len(self.curr_shape) < 3:
            QMessageBox.warning(
                self, 'Ошибка', 'Фигура должна содержать минимум 3 вершины.')
            return
        self.draw_segment(self.curr_shape[0], self.curr_shape[-1],
                          self.shape_color)
        self.shapes.append(self.curr_shape)
        self.curr_shape = QPolygon()
        self.scene.update()

    def update_clipper(self, new_point: QPoint) -> None:
        if self.is_clipper_closed:
            self.clipper.clear()
            self.is_clipper_closed = False
            self.update_scene()
        self.clipper.append(new_point)

        self.scene.addEllipse(
            new_point.x() - 2, new_point.y() - 2, 4, 4,
            self.clipper_color, self.clipper_color)

        if len(self.clipper) > 1:
            self.draw_segment(new_point, self.clipper[-2],
                              self.clipper_color)
            self.scene.update()

    def update_curr_shape(self, new_point: QPoint) -> None:
        self.curr_shape.append(new_point)

        self.scene.addEllipse(
            new_point.x() - 2, new_point.y() - 2, 4, 4,
            self.shape_color, self.shape_color)

        if len(self.curr_shape) > 1:
            self.draw_segment(new_point, self.curr_shape[-2],
                              self.shape_color)
            self.scene.update()

    def update_scene(self) -> None:
        self.scene.clear()
        self.draw_shapes()
        self.draw_clipper()

    def draw_segment(self, p1: QPoint, p2: QPoint, color: QColor) -> None:
        self.scene.addLine(QLine(p1, p2).toLineF(), color)

    def draw_shapes(self) -> None:
        for shape in self.shapes:
            self.draw_shape(shape, self.shape_color)

    def draw_shape(self, shape: QPolygon, color: QColor) -> None:
        self.scene.addPolygon(shape.toPolygonF(), color)
        self.scene.update()

    def draw_clipper(self) -> None:
        self.scene.addPolygon(self.clipper.toPolygonF(), self.clipper_color)
        self.scene.update()

    def add_clipper_point(self) -> None:
        try:
            point_x = float(self.clipper_point_x.toPlainText())
            point_y = float(self.clipper_point_y.toPlainText())
        except ValueError:
            QMessageBox.warning(
                self, 'Ошибка', 'Некорректные данные в полях ввода новой точки отсекателя.')
            return

        self.update_clipper(QPointF(point_x, point_y).toPoint())

    def add_curr_shape_point(self) -> None:
        try:
            point_x = float(self.shape_point_x.toPlainText())
            point_y = float(self.shape_point_y.toPlainText())
        except ValueError:
            QMessageBox.warning(
                self, 'Ошибка', 'Некорректные данные в полях ввода новой точки фигуры.')
            return
        self.update_curr_shape(QPointF(point_x, point_y).toPoint())

    def update_time_label(self, time: float) -> None:
        """Time in seconds."""
        self.time_label.setText(f'{time * 1000: .4f} мс')

    def clear(self) -> None:
        self.is_closed = False
        self.shapes.clear()
        self.curr_shape.clear()
        self.scene.clear()
        self.clipper.clear()

    def clear_clipper(self) -> None:
        self.clipper.clear()
        self.is_closed = False
        self.update_scene()

    def clear_shapes(self) -> None:
        self.shapes.clear()
        self.curr_shape.clear()
        self.update_scene()
