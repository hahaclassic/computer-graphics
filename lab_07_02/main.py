from PyQt6.QtWidgets import QApplication
import src.interface as interface
import sys

app = QApplication([])
window = interface.Interface()
window.show()

sys.exit(app.exec())
# from PyQt6.QtCore import QRect, QLine, QPoint

# import src.cutting_segments as cut


# rect = QRect(0, 10, 10, 10)
# x1, y1 = map(int, input("Введите первую точку: ").split())
# x2, y2 = map(int, input("Введите вторую точку: ").split())
# p1 = QPoint(x1, y1)
# p2 = QPoint(x2, y2)

# ok, line = cut.cohen_sutherland(rect, QLine(p1,p2))
# print(ok, line.p1(), line.p2())
