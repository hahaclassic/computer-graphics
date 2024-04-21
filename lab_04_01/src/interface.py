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

        self.circle_plotter = draw.CirclePlotter(self.scene)
        self.ellipse_plotter = draw.EllipsePlotter(self.scene)

        self.background_color_label = self.findChild(QLabel, 'backgroundColor')
        self.background_color = QColor(255, 255, 255)
        self.pen_color_label = self.findChild(QLabel, 'PenColor')
        self.pen_color = QColor(0, 0, 0)

        self.algorithm = self.findChild(QComboBox, 'AlgorithmTypeBox')
        self.__setup_buttons()
        self.__setup_input_fields()

    def __setup_input_fields(self):
        self.circle_center_x = self.findChild(QTextEdit, 'CircleCenterX')
        self.circle_center_y = self.findChild(QTextEdit, 'CircleCenterY')
        self.circle_radius = self.findChild(QTextEdit, 'CircleRadius')
        self.circle_step = self.findChild(QTextEdit, 'CircleStep')
        self.circle_num_figures = self.findChild(QTextEdit, 'CircleNumFigures')

        self.ellipse_center_x = self.findChild(QTextEdit, 'EllipseCenterX')
        self.ellipse_center_y = self.findChild(QTextEdit, 'EllipseCenterY')
        self.ellipse_semi_major_axis = self.findChild(QTextEdit, 'BigHalfAxis')
        self.ellipse_semi_minor_axis = self.findChild(
            QTextEdit, 'SmallHalfAxis')
        self.ellipse_step = self.findChild(QTextEdit, 'EllipseStep')
        self.ellipse_num_figures = self.findChild(
            QTextEdit, 'EllipseNumFigures')

    def __setup_buttons(self):
        self.background_color_button = self.findChild(
            QPushButton, 'changeBackgroundColorBtn')
        self.background_color_button.clicked.connect(
            self.choose_background_color)
        self.pen_color_button = self.findChild(
            QPushButton, 'changePenColorBtn')
        self.pen_color_button.clicked.connect(self.choose_pen_color)

        self.plot_circle_button = self.findChild(QPushButton, 'plotCircle')
        self.plot_circle_button.clicked.connect(self.plot_circle)

        self.plot_circle_spectrum_button = self.findChild(
            QPushButton, 'plotCircleSpectrum')
        self.plot_circle_spectrum_button.clicked.connect(
            self.plot_circle_spectrum)

        self.plot_ellipse_button = self.findChild(QPushButton, 'plotEllipse')
        self.plot_ellipse_button.clicked.connect(self.plot_ellipse)

        self.plot_ellipse_spectrum_button = self.findChild(
            QPushButton, 'plotEllipseSpectrum')
        self.plot_ellipse_spectrum_button.clicked.connect(
            self.plot_ellipse_spectrum)

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

    def get_circle_data(self) -> tuple[draw.Circle, bool]:
        try:
            center_x = float(self.circle_center_x.toPlainText())
            center_y = float(self.circle_center_y.toPlainText())
            radius = float(self.circle_radius.toPlainText())
        except ValueError:
            QMessageBox.warning(
                self, 'Ошибка', 'Некорректные данные в полях ввода окружности.')
            return draw.Circle(), False

        return draw.Circle(QPointF(center_x, center_y), radius), True

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

    def get_circle_spectrum_data(self) -> tuple[draw.Spectrum, bool]:
        try:
            step = float(self.circle_step.toPlainText())
            num_of_figures = int(self.circle_num_figures.toPlainText())
        except ValueError:
            QMessageBox.warning(
                self, 'Ошибка', 'Некорректные данные для спектра.')
            return draw.Spectrum, False

        return draw.Spectrum(step, num_of_figures), True

    def get_ellipse_spectrum_data(self) -> tuple[draw.Spectrum, bool]:
        try:
            step = float(self.ellipse_step.toPlainText())
            num_of_figures = int(self.ellipse_num_figures.toPlainText())
        except ValueError:
            QMessageBox.warning(
                self, 'Ошибка', 'Некорректные данные для спектра.')
            return draw.Spectrum, False

        return draw.Spectrum(step, num_of_figures), True

    def plot_circle(self):
        circle, ok = self.get_circle_data()
        if not ok:
            return

        algoritm = draw.Algorithm(self.algorithm.currentIndex())
        self.circle_plotter.plot(algoritm, circle, self.pen_color)

    def plot_ellipse(self):
        ellipse, ok = self.get_ellipse_data()
        if not ok:
            return

        algoritm = draw.Algorithm(self.algorithm.currentIndex())
        self.ellipse_plotter.plot(algoritm, ellipse, self.pen_color)

    def plot_circle_spectrum(self):
        circle, ok = self.get_circle_data()
        if not ok:
            return

        spectrum, ok = self.get_circle_spectrum_data()
        if not ok:
            return

        algoritm = draw.Algorithm(self.algorithm.currentIndex())
        self.circle_plotter.spectrum(
            algoritm, circle, spectrum, self.pen_color)

    def plot_ellipse_spectrum(self):
        ellipse, ok = self.get_ellipse_data()
        if not ok:
            return

        spectrum, ok = self.get_ellipse_spectrum_data()
        if not ok:
            return

        algoritm = draw.Algorithm(self.algorithm.currentIndex())
        self.ellipse_plotter.spectrum(
            algoritm, ellipse, spectrum, self.pen_color)
