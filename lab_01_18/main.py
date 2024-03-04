from PyQt6.QtWidgets import QApplication
import src.interface as interface
import sys

app = QApplication([])
window = interface.MainWindow()
window.show()

sys.exit(app.exec())
