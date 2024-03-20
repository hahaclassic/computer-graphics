from PyQt6.QtWidgets import QWidget, QMainWindow, QPushButton, \
    QGridLayout, QTextEdit, QLabel, QMessageBox, QScrollArea, \
    QVBoxLayout, QFrame, QGraphicsView, QGraphicsScene
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QTransform

MANUAL_PATH = './src/app_data/manual.txt'
TASK_PATH = './src/app_data/task.txt'


class ScrolledLabel(QWidget):
    def __init__(self, text) -> None:
        super().__init__()

        self.label = QLabel(text)
        self.label.setWordWrap(True)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.label)

        layout = QVBoxLayout()
        layout.addWidget(scroll_area)
        self.setLayout(layout)


def create_line():
    hr_line = QFrame()
    hr_line.setFrameShape(QFrame.Shape.HLine)
    return hr_line


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Лабораторная работа №2')
        self.setMinimumSize(1000, 700)

        self.manualWidget = self.__setup_manual()
        self.taskWidget = self.__setup_task()

        # Input fields
        self.input_section_width = 150
        self.config_label = QLabel('Конфигурация')
        self.config_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.config_label.setFixedWidth(self.input_section_width * 2)
        self.__setup_offset_interface()
        self.__setup_rotation_interface()
        self.__setup_scaling_interface()

        # Canvas
        transform = QTransform()
        transform.scale(1, -1)
        self.scene = QGraphicsScene()
        self.canvas = QGraphicsView(self.scene, self)
        self.canvas.setTransform(transform)

        self.line = create_line()

        # Create buttons
        self.button_reset = QPushButton('Вернуть исходное состояние', self)
        self.button_cancel_last_transformation = QPushButton(
            'Отменить последнее преобразование', self)

        # Center log
        self.center_coordinates = QLabel(
            'Центр фигуры в данный момент: (0, 0)', self)

        # Create a QGridLayout
        self.layoutWidget = self.__setup_layout()

        # Set the layout for the main window
        central_widget = QWidget()
        central_widget.setLayout(self.layoutWidget)
        self.setCentralWidget(central_widget)

    def __setup_offset_interface(self):
        self.offset_line1 = create_line()
        self.offset_label = QLabel('Смещение')
        self.offset_line2 = create_line()
        self.offset_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.offset_label.setFixedWidth(self.input_section_width * 2)

        self.offset_label_x = QLabel('dx')
        self.offset_label_x.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.offset_label_x.setFixedWidth(self.input_section_width)
        self.offset_label_y = QLabel('dy')
        self.offset_label_y.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.offset_label_y.setFixedWidth(self.input_section_width)

        self.offset_input_x = QTextEdit(self)
        self.offset_input_x.setText('0')
        self.offset_input_x.setFixedSize(QSize(self.input_section_width, 30))
        self.offset_input_y = QTextEdit(self)
        self.offset_input_y.setText('0')
        self.offset_input_y.setFixedSize(QSize(self.input_section_width, 30))

        self.offset_button = QPushButton('Выполнить смещение', self)

    def __setup_rotation_interface(self):
        self.rotation_line1 = create_line()
        self.rotate_label = QLabel('Поворот')
        self.rotation_line2 = create_line()
        self.rotate_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rotate_label.setFixedWidth(self.input_section_width * 2)

        self.rotate_center_label = QLabel('Центр поворота')
        self.rotate_center_label.setFixedWidth(self.input_section_width * 2)
        self.rotate_center_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rotate_center_x = QLabel('x')
        self.rotate_center_x.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rotate_center_x.setFixedWidth(self.input_section_width)
        self.rotate_center_y = QLabel('y')
        self.rotate_center_y.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rotate_center_y.setFixedWidth(self.input_section_width)

        self.rotate_input_x = QTextEdit(self)
        self.rotate_input_x.setText('0')
        self.rotate_input_x.setFixedSize(QSize(self.input_section_width, 30))
        self.rotate_input_y = QTextEdit(self)
        self.rotate_input_y.setText('0')
        self.rotate_input_y.setFixedSize(QSize(self.input_section_width, 30))

        self.rotate_angle_label = QLabel('Угол поворота (в градусах)')
        self.rotate_angle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rotate_angle_label.setFixedWidth(self.input_section_width * 2)
        self.rotate_angle_input = QTextEdit(self)
        self.rotate_angle_input.setText('0')
        self.rotate_angle_input.setFixedSize(
            QSize(self.input_section_width * 2, 30))

        self.rotate_button = QPushButton('Выполнить поворот', self)

    def __setup_scaling_interface(self):
        self.scaling_line1 = create_line()
        self.scale_label = QLabel('Масштаб')
        self.scaling_line2 = create_line()
        self.scale_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scale_label.setFixedWidth(self.input_section_width * 2)

        self.scale_center_label = QLabel('Центр масштабирования')
        self.scale_center_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scale_center_label.setFixedWidth(self.input_section_width * 2)
        self.scale_label_x = QLabel('x')
        self.scale_label_x.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scale_label_x.setFixedWidth(self.input_section_width)
        self.scale_label_y = QLabel('y')
        self.scale_label_y.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scale_label_y.setFixedWidth(self.input_section_width)

        self.scale_input_x = QTextEdit(self)
        self.scale_input_x.setText('0')
        self.scale_input_x.setFixedSize(QSize(self.input_section_width, 30))
        self.scale_input_y = QTextEdit(self)
        self.scale_input_y.setText('0')
        self.scale_input_y.setFixedSize(QSize(self.input_section_width, 30))

        self.scale_ratio_label = QLabel('Коэффициент масштабирования')
        self.scale_ratio_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.scale_ratio_label.setFixedWidth(self.input_section_width * 2)

        self.scale_ratio_input = QTextEdit(self)
        self.scale_ratio_input.setText('1')
        self.scale_ratio_input.setFixedSize(
            QSize(self.input_section_width * 2, 30))

        self.scale_button = QPushButton('Выполнить масштабирование', self)

    def __setup_layout(self) -> QGridLayout:
        layoutWidget = QGridLayout()
        layoutWidget.addWidget(self.canvas, 0, 0, 27, 2)
        layoutWidget.addWidget(self.manualWidget, 0, 0, 27, 2)
        layoutWidget.addWidget(self.taskWidget, 0, 0, 28, 2)
        layoutWidget.addWidget(self.center_coordinates, 27, 0, 1, 2)
        layoutWidget.addWidget(self.config_label, 0, 2, 1, 2)

        # add offset interface
        layoutWidget.addWidget(self.offset_line1, 1, 2, 1, 2)
        layoutWidget.addWidget(self.offset_label, 2, 2, 1, 2)
        layoutWidget.addWidget(self.offset_line2, 3, 2, 1, 2)
        layoutWidget.addWidget(self.offset_label_x, 4, 2, 1, 1)
        layoutWidget.addWidget(self.offset_label_y, 4, 3, 1, 1)
        layoutWidget.addWidget(self.offset_input_x, 5, 2, 1, 1)
        layoutWidget.addWidget(self.offset_input_y, 5, 3, 1, 1)
        layoutWidget.addWidget(self.offset_button, 6, 2, 1, 2)

        # add scale interface
        layoutWidget.addWidget(self.scaling_line1, 7, 2, 1, 2)
        layoutWidget.addWidget(self.scale_label, 8, 2, 1, 2)
        layoutWidget.addWidget(self.scaling_line2, 9, 2, 1, 2)
        layoutWidget.addWidget(self.scale_center_label, 10, 2, 1, 2)
        layoutWidget.addWidget(self.scale_label_x, 11, 2, 1, 1)
        layoutWidget.addWidget(self.scale_label_y, 11, 3, 1, 1)
        layoutWidget.addWidget(self.scale_input_x, 12, 2, 1, 1)
        layoutWidget.addWidget(self.scale_input_y, 12, 3, 1, 1)
        layoutWidget.addWidget(self.scale_ratio_label, 13, 2, 1, 2)
        layoutWidget.addWidget(self.scale_ratio_input, 14, 2, 1, 2)
        layoutWidget.addWidget(self.scale_button, 15, 2, 1, 2)

        # add rotate interface
        layoutWidget.addWidget(self.rotation_line1, 16, 2, 1, 2)
        layoutWidget.addWidget(self.rotate_label, 17, 2, 1, 2)
        layoutWidget.addWidget(self.rotation_line2, 18, 2, 1, 2)
        layoutWidget.addWidget(self.rotate_center_label, 19, 2, 1, 2)
        layoutWidget.addWidget(self.rotate_center_x, 20, 2, 1, 1)
        layoutWidget.addWidget(self.rotate_center_y, 20, 3, 1, 1)
        layoutWidget.addWidget(self.rotate_input_x, 21, 2, 1, 1)
        layoutWidget.addWidget(self.rotate_input_y, 21, 3, 1, 1)
        layoutWidget.addWidget(self.rotate_angle_label, 22, 2, 1, 2)
        layoutWidget.addWidget(self.rotate_angle_input, 23, 2, 1, 2)
        layoutWidget.addWidget(self.rotate_button, 24, 2, 1, 2)

        layoutWidget.addWidget(self.line, 25, 2, 1, 2)
        layoutWidget.addWidget(
            self.button_cancel_last_transformation, 26, 2, 1, 2)
        layoutWidget.addWidget(self.button_reset, 27, 2, 1, 2)

        return layoutWidget

    def __setup_manual(self) -> ScrolledLabel:

        try:
            file = open(MANUAL_PATH, 'r', encoding='utf-8')
            manual = file.read()
            file.close()
        except PermissionError or FileNotFoundError or IsADirectoryError:
            manual = 'Произошла ошибка во время получения инструкции.'

        manualWidget = ScrolledLabel(manual)
        manualWidget.hide()

        return manualWidget

    def __setup_task(self) -> QLabel:
        try:
            file = open(TASK_PATH, 'r', encoding='utf-8')
            task = file.read()
            file.close()
        except PermissionError or FileNotFoundError or IsADirectoryError:
            task = 'Произошла ошибка во время получения условия задачи.'

        taskWidget = QLabel(task)
        taskWidget.hide()

        return taskWidget

    def show_manual(self) -> None:
        if self.manualWidget.isVisible():
            self.manualWidget.hide()
            self.taskWidget.hide()
            self.canvas.show()
        else:
            self.manualWidget.show()
            self.taskWidget.hide()
            self.canvas.hide()

    def show_task(self) -> None:
        if self.taskWidget.isVisible():
            self.manualWidget.hide()
            self.taskWidget.hide()
            self.canvas.show()
        else:
            self.taskWidget.show()
            self.manualWidget.hide()
            self.canvas.hide()

    def show_error_message(self, title: str, message: str) -> None:
        QMessageBox.warning(self, title, message)
