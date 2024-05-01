from PyQt6.QtWidgets import QApplication
import src.interface as interface
import sys

app = QApplication([])
window = interface.Interface()
window.show()

sys.exit(app.exec())
