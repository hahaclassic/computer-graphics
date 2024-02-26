import sys, os
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QGraphicsView, \
    QGraphicsScene, QGridLayout, QTextEdit, QLabel, QRubberBand, QGraphicsEllipseItem
from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QIcon, QBrush, QPen, QPainter
from PyQt6.QtCore import Qt, QRect, QSize, QPointF, QLineF, QRectF

from ..process import process

class CoordinateGrid(QGraphicsView):
    def __init__(self, scene, parent):
        super().__init__(scene, parent)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.rubberBand = QRubberBand(QRubberBand.Shape.Rectangle, self)
        self.rubberBand.setVisible(False)
        self.rubberBand.setGeometry(QRect(0, 0, 0, 0))
        self.setMouseTracking(True)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setOptimizationFlags(QGraphicsView.OptimizationFlag.DontAdjustForAntialiasing)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.SmartViewportUpdate)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.dragging = False
        self.drag_start = QPointF()
        self.drag_current = QPointF()
        self.selected_point = None
        self.points_set1 = set()
        self.points_set2 = set()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_start = event.pos()
            self.drag_current = event.pos()
        elif event.button() == Qt.MouseButton.MiddleButton:
            items = self.items(event.pos())
            for item in items:
                self.delete_point(item)

        elif event.button() == Qt.MouseButton.RightButton:
            brush = QBrush(Qt.GlobalColor.blue)
            point = self.mapToScene(event.pos())
            self.scene().addEllipse(point.x(), point.y(), 5, 5, QPen(Qt.GlobalColor.black), brush)
            self.points_set2.add((point.x(), point.y()))

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton \
            and abs(self.drag_start.x() - event.pos().x()) <= 1 \
            and abs(self.drag_start.y() - event.pos().y()) <= 1:
            brush = QBrush(Qt.GlobalColor.red)
            point = self.mapToScene(event.pos())
            self.scene().addEllipse(point.x(), point.y(), 5, 5, QPen(Qt.GlobalColor.black), brush)
            self.points_set1.add((point.x(), point.y()))
        self.selected_point = None
        self.rubberBand.setVisible(False)
        self.dragging = False

    def mouseMoveEvent(self, event):
        if self.dragging:
            delta = event.pos() - self.drag_current
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
            self.drag_current = event.pos()

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            factor = 1.25
        else:
            factor = 1 / 1.25
        center = self.mapToScene(self.cursor().pos())
        self.scale(factor, factor)

    def draw_point(self, x: float, y: float):
        pass    
    
    def delete_point(self, point) -> None:
        if not isinstance(point, QGraphicsEllipseItem):
            return
        
        if point.brush().color() == Qt.GlobalColor.red:
            self.points_set1.remove((point.x(), point.y()))
        elif point.brush().color() == Qt.GlobalColor.blue:
            self.points_set2.remove((point.x(), point.y()))

        self.scene().removeItem(point)

    def points(self) -> tuple[set, set]:
        return self.points_set1, self.points_set2
                
    def delete_points(self) -> None:
        items = self.scene().items()
        for item in items:
            self.delete_point(item)

class CoordinateInputField(QTextEdit):
    def __init__(self, parent):
        super().__init__(parent)

    def data(self) -> list[tuple[float, float]]:
        coordinates = self.toPlainText().split()
        points = set()
        for i in range(0, len(coordinates) - 1, 2):
            points.add((coordinates[i], coordinates[i + 1]))
        return points
        

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title and icon
        self.setWindowTitle('PyQt6 Example')
        self.setWindowIcon(QIcon('icon.png'))
        self.setMinimumSize(640,400)

        # Create a graphics scene and view
        self.scene = QGraphicsScene(self)
        self.view = CoordinateGrid(self.scene, self)
        self.view.setMinimumSize(400,400)

        # Add a rectangle to the scene
        self.scene.addRect(10, 10, 100, 100)

        # Create labels
        label1, label2 = QLabel(self), QLabel(self)
        label1.setText("Set A")
        label2.setText("Set B")
        
        # Create output field
        self.output_field = QLabel(self)

        # Create two input fields
        self.input_field1 = CoordinateInputField(self)
        self.input_field1.setFixedWidth(100)
        self.input_field2 = CoordinateInputField(self)
        self.input_field2.setFixedWidth(100)

        # Create two buttons
        button_calc = QPushButton('calc', self)
        button_calc.setFixedSize(QSize(100,20))
        button_clear = QPushButton('clear', self)
        button_clear.setFixedSize(QSize(100,20))

        # Connect button click signals to slot functions
        button_calc.clicked.connect(self.calcucate)
        button_clear.clicked.connect(self.clear)

        # Create a QGridLayout
        layout = QGridLayout()

        # Add QGraphicsView to the layout
        layout.addWidget(self.view, 0, 0, 3, 2)

        # Add labels
        layout.addWidget(label1, 0, 2, 1, 1)
        layout.addWidget(label2, 0, 3, 1, 1)
        layout.addWidget(self.output_field, 3, 0, 2, 1)

        # Add input fields to the layout
        layout.addWidget(self.input_field1, 1, 2, 1, 1)
        layout.addWidget(self.input_field2, 1, 3, 1, 1)

        # Add buttons to the layout
        layout.addWidget(button_calc, 3, 2)
        layout.addWidget(button_clear, 3, 3)

        # Set the layout for the main window
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)    

    def calcucate(self):
        set1, set2 = self.get_points()
        max_area, cicle1, cicle2 = process.find_max_area(set1, set2)
        tangent_p1, tangent_p2 = process.tangent_coordinates(cicle1, cicle2)


        self.output_field.setText(f"S = {max_area:.3f}, cicle1 = {cicle1}, cicle2 = {cicle2}")
        
        self.scene.addEllipse(cicle1.center()[0], cicle1.center()[1], 
                              cicle1.radius(), cicle1.radius(), QPen(Qt.GlobalColor.red))
        self.scene.addEllipse(cicle2.center()[0], cicle2.center()[1], 
                              cicle2.radius(), cicle2.radius(), QPen(Qt.GlobalColor.blue))
        self.scene.addLine(QLineF(tangent_p1[0], tangent_p1[1], tangent_p2[0], tangent_p2[1]), Qt.GlobalColor.white)
        self.scene.addLine(QLineF(cicle1.center()[0], cicle1.center()[1], cicle2.center()[0], cicle2.center()[1]), \
                Qt.GlobalColor.white)

    def clear(self):
        self.view.delete_points()
        self.input_field1.clear()
        self.input_field2.clear()

    def get_points(self):
        points_set1, points_set2 = self.view.points()
        points = self.input_field1.data()
        for p in points:
            points_set1.add(p)
        points = self.input_field2.data()
        for p in points:
            points_set2.add(p)
        print("set A")
        for p in points_set1:
            print(p)
        print("set B")
        for p in points_set2:
            print(p)
        return points_set1, points_set2
        