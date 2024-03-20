from PyQt6.QtWidgets import QMainWindow, QMenu, QMenuBar, QFileDialog, QMessageBox
from PyQt6.QtGui import QAction, QColor
from PyQt6.QtCore import QPointF

from src.widgets import MainWindow
from src.satellite import Satellite, NUM_OF_SATELLITE_POINTS
import math
import copy

SRC_PATH = './src/app_data/satellite.txt'
EPS = 1e-07


class MenuBar(QMenuBar):
    def __init__(self, parent: QMainWindow) -> None:
        super().__init__(parent)

        self.file_actions = QMenu('Файл', parent)
        self.export_points = QAction('Сохранить базовые точки', parent)
        self.import_points = QAction('Импортировать базовые точки', parent)

        self.task_condition = QAction('Условие', parent)
        self.manual = QAction('Инструкция', parent)
        self.basic_satellite = QAction('Вернуть базовый спутник')

        self.export_points.triggered.connect(parent.save_satellite)
        self.import_points.triggered.connect(parent.load_satellite)
        self.manual.triggered.connect(parent.show_manual)
        self.task_condition.triggered.connect(parent.show_task)
        self.basic_satellite.triggered.connect(parent.return_basic_satellite)

        self.file_actions.addAction(self.export_points)
        self.file_actions.addAction(self.import_points)
        self.addMenu(self.file_actions)
        self.addAction(self.task_condition)
        self.addAction(self.manual)
        self.addAction(self.basic_satellite)


class Interface(MainWindow):
    def __init__(self):
        super().__init__()

        self.state_stack: list[Satellite] = []
        self.__set_basic_satellite()

        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)

        self.button_reset.clicked.connect(self.reset_transformations)
        self.button_cancel_last_transformation.clicked.connect(
            self.cancel_last_transformation)
        self.offset_button.clicked.connect(self.move_satellite)
        self.rotate_button.clicked.connect(self.rotate_satellite)
        self.scale_button.clicked.connect(self.scale_satellite)

    def move_satellite(self) -> None:
        try:
            dx = float(self.offset_input_x.toPlainText())
            dy = float(self.offset_input_y.toPlainText())
        except ValueError:
            self.show_error_message(
                'Некорректные данные', 'В полях ввода указаны некорректные данные')
            return

        satellite = copy.copy(self.state_stack[-1])
        satellite.move(dx, dy)
        self.paint_satellite(satellite)
        self.state_stack.append(satellite)
        self.__show_center_coordinates(satellite)

    def rotate_satellite(self) -> None:
        try:
            x = float(self.rotate_input_x.toPlainText())
            y = float(self.rotate_input_y.toPlainText())
            rad_angle = float(self.rotate_angle_input.toPlainText())
        except ValueError:
            self.show_error_message(
                'Некорректные данные', 'В полях ввода указаны некорректные данные')
            return

        angle = math.radians(rad_angle)
        satellite = copy.copy(self.state_stack[-1])
        satellite.rotate(QPointF(x, y), angle)
        self.state_stack.append(satellite)

        self.paint_satellite(satellite)
        self.__show_center_coordinates(satellite)

    def scale_satellite(self) -> None:
        try:
            x = float(self.scale_input_x.toPlainText())
            y = float(self.scale_input_y.toPlainText())
            ratio = float(self.scale_ratio_input.toPlainText())
        except ValueError:
            self.show_error_message(
                'Некорректные данные', 'В полях ввода указаны некорректные данные')
            return
        if ratio < EPS:
            self.show_error_message('Некорректные данные',
                                    f'Коэффициент масшабирования должен быть не меньше {EPS}.')
            return

        satellite = copy.copy(self.state_stack[-1])
        satellite.scale(QPointF(x, y), ratio)
        self.state_stack.append(satellite)
        self.paint_satellite(satellite)
        self.__show_center_coordinates(satellite)

    def paint_satellite(self, satellite: Satellite) -> None:
        self.scene.clear()
        graphics_items = satellite.build()
        for item in graphics_items:
            item.setPen(QColor(0, 255, 0))
            self.scene.addItem(item)

    def cancel_last_transformation(self) -> None:
        if len(self.state_stack) > 1:
            self.state_stack.pop()
            self.paint_satellite(self.state_stack[-1])
            self.__show_center_coordinates(self.state_stack[-1])

    def reset_transformations(self) -> None:
        self.state_stack = self.state_stack[:1]
        self.paint_satellite(self.state_stack[-1])
        self.__show_center_coordinates(self.state_stack[-1])
        self.offset_input_x.clear()
        self.offset_input_y.clear()
        self.rotate_input_x.clear()
        self.rotate_input_y.clear()
        self.rotate_angle_input.clear()
        self.scale_input_x.clear()
        self.scale_input_y.clear()
        self.scale_ratio_input.clear()

    def __show_center_coordinates(self, satellite: Satellite) -> None:
        center = satellite.center()
        self.center_coordinates.setText(
            f'Центр фигуры в данный момент: ({center.x():.3f},{center.y():.3f})')

    def __set_basic_satellite(self) -> None:

        src_points = self.__load_points(SRC_PATH)

        if len(src_points) == 0:
            return

        self.state_stack.clear()
        satellite = Satellite(src_points)
        self.state_stack.append(Satellite(src_points))

        self.paint_satellite(satellite)
        self.__set_input_fields(satellite.center())
        self.__show_center_coordinates(satellite)

    def load_satellite(self) -> None:
        file_name, _ = QFileDialog.getOpenFileName(self, 'Загрузить файл', '')
        if file_name == '':
            return
        src_points = self.__load_points(file_name)
        if len(src_points) == 0:
            return

        self.state_stack.clear()
        satellite = Satellite(src_points)
        self.state_stack.append(satellite)
        self.paint_satellite(satellite)
        self.__set_input_fields(satellite.center())

    def __load_points(self, path: str) -> list[QPointF]:
        try:
            with open(path, 'r') as f:
                data = f.read()
            float_data = list(map(float, data.split()))
        except PermissionError or FileNotFoundError or IsADirectoryError:
            self.show_error_message(
                'Ошибка чтения файла', 'Произошла ошибка во время открытия или чтения файла')
            return []

        if len(float_data) / 2 < NUM_OF_SATELLITE_POINTS:
            self.show_error_message(
                'Ошибка', 'В исходном файле недостаточно данных.')
            return []

        src_points = []
        for i in range(0, len(float_data) - 1, 2):
            src_points.append(QPointF(float_data[i], float_data[i + 1]))

        return src_points

    def save_satellite(self) -> None:
        file_name, _ = QFileDialog.getSaveFileName(self, 'Сохранить файл', '')
        if file_name == '':
            return

        points = self.state_stack[-1].to_points()

        try:
            with open(file_name, 'w') as file:
                for point in points:
                    file.write(f'{point.x()} {point.y()}\n')
        except PermissionError or FileNotFoundError or IsADirectoryError:
            self.show_error_message(
                'Ошибка записи', 'Произошла ошибка во время записи данных в файл')

    def __set_input_fields(self, center: QPointF) -> None:
        self.scale_input_x.setText(f'{center.x():.3f}')
        self.scale_input_y.setText(f'{center.y():.3f}')
        self.rotate_input_x.setText(f'{center.x():.3f}')
        self.rotate_input_y.setText(f'{center.y():.3f}')
        self.center_coordinates.setText(
            f'Центр фигуры в данный момент: ({center.x():.3f},{center.y():.3f})')

    def return_basic_satellite(self) -> None:
        answer = QMessageBox.question(self, 'Подтверждение',
                                      'Текущие данные не будут сохранены. Вы уверены, что хотите продолжить?')
        if answer == QMessageBox.StandardButton.Yes:
            self.__set_basic_satellite()
