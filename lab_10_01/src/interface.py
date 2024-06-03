from PyQt6.QtWidgets import QMainWindow, QMessageBox, \
    QPushButton, QLabel, QGraphicsView, QGraphicsScene, QTextEdit, QComboBox
from PyQt6.QtGui import QColor
from PyQt6.QtCore import QLineF
from PyQt6 import uic
import time

import src.horizon as horizon
import src.functions as functions

EPS = 1e-07


class Interface(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        uic.loadUi('ui/mainwindow.ui', self)

        self.background_color = QColor(0, 0, 0)
        self.color = QColor(255, 255, 255)

        self.time_label = self.findChild(QLabel, 'timeLabel')
        self.function_box = self.findChild(QComboBox, 'comboBox')

        self.functions = [
            functions.func1,
            functions.func2,
            functions.func3,
            functions.func4,
        ]

        self.__setup_input_fields()
        self.__setup_scene()
        self.__setup_buttons()

    def __setup_scene(self) -> None:
        self.scene = QGraphicsScene()
        self.view = self.findChild(QGraphicsView, 'graphicsView')
        self.view.setScene(self.scene)
        self.view.setBackgroundBrush(self.background_color)

    def __setup_buttons(self) -> None:
        self.plot_button = self.findChild(QPushButton, 'plotBtn')
        self.clear_button = self.findChild(QPushButton, 'clearBtn')
        self.plot_button.clicked.connect(self.plot)
        self.clear_button.clicked.connect(self.clear)

    def __setup_input_fields(self) -> None:
        self.input_start_x = self.findChild(QTextEdit, 'x_start')
        self.input_end_x = self.findChild(QTextEdit, 'x_end')
        self.input_step_x = self.findChild(QTextEdit, 'x_step')

        self.input_start_z = self.findChild(QTextEdit, 'z_start')
        self.input_end_z = self.findChild(QTextEdit, 'z_end')
        self.input_step_z = self.findChild(QTextEdit, 'z_step')

        self.input_angle_x = self.findChild(QTextEdit, 'angle_x')
        self.input_angle_y = self.findChild(QTextEdit, 'angle_y')
        self.input_angle_z = self.findChild(QTextEdit, 'angle_z')
        self.input_scale = self.findChild(QTextEdit, 'scale')

    def plot(self) -> None:
        x_interval, z_interval, transform = self.get_data()
        if x_interval is None or z_interval is None or transform is None:
            return

        self.scene.clear()
        func = self.functions[self.function_box.currentIndex()]

        start = time.monotonic()
        lines = horizon.horizon_method(
            self.view, x_interval, z_interval, func, transform)
        self.draw_lines(lines)
        # self.scene.update()
        end = time.monotonic()

        self.update_time_label(end - start)

    def draw_line(self, line: QLineF, color: QColor) -> None:
        self.scene.addLine(line, color)

    def draw_lines(self, lines: list[QLineF]) -> None:
        for line in lines:
            self.draw_line(line, self.color)

    def update_time_label(self, time: float) -> None:
        """Time in seconds."""
        self.time_label.setText(f'{time * 1000: .4f} мс')

    def get_data(self) -> tuple[horizon.Interval, horizon.Interval,
                                horizon.Transformation]:
        x_interval = self.get_x_interval()
        z_interval = self.get_z_interval()
        transform = self.get_transformation()
        return x_interval, z_interval, transform

    def get_x_interval(self) -> horizon.Interval:
        try:
            start_x = float(self.input_start_x.toPlainText())
            end_x = float(self.input_end_x.toPlainText())
            step_x = float(self.input_step_x.toPlainText())
        except ValueError:
            QMessageBox.warning(
                self, 'Ошибка', 'Некорректные данные в полях ввода интервала по оси X')
            return None

        return horizon.Interval(start_x, end_x, step_x)

    def get_z_interval(self) -> horizon.Interval:
        try:
            start_z = float(self.input_start_z.toPlainText())
            end_z = float(self.input_end_z.toPlainText())
            step_z = float(self.input_step_z.toPlainText())
        except ValueError:
            QMessageBox.warning(
                self, 'Ошибка', 'Некорректные данные в полях ввода интервала по оси Z')
            return None

        return horizon.Interval(start_z, end_z, step_z)

    def get_transformation(self) -> horizon.Transformation:
        rotation = self.get_angles()
        scale_ratio = self.get_scale_ratio()
        if rotation is None or scale_ratio is None:
            return None
        return horizon.Transformation(rotation, scale_ratio)

    def get_angles(self) -> horizon.Rotation:
        try:
            angle_x = float(self.input_angle_x.toPlainText())
            angle_y = float(self.input_angle_y.toPlainText())
            angle_z = float(self.input_angle_z.toPlainText())
        except ValueError:
            QMessageBox.warning(
                self, 'Ошибка', 'Некорректные данные в полях ввода углов поворота')
            return None

        return horizon.Rotation(angle_x, angle_y, angle_z)

    def get_scale_ratio(self) -> float:
        try:
            scale = float(self.input_scale.toPlainText())
        except ValueError:
            QMessageBox.warning(
                self, 'Ошибка', 'Некорректные данные в поле ввода коэффициента масшатибрования')
            return None
        if scale < EPS:
            QMessageBox.warning(self, 'Некорректные данные',
                                f'Коэффициент масшабирования должен быть не меньше {EPS}.')
            return None

        return scale

    def clear(self) -> None:
        self.scene.clear()
