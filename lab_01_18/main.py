from PyQt6.QtWidgets import QApplication
import src.interface as interface
import sys

app = QApplication(sys.argv)
window = interface.MainWindow()
window.show()

sys.exit(app.exec())
