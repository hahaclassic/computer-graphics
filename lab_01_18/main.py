import internal.interface.interface as interface
import sys

app = interface.QApplication(sys.argv)
window = interface.MainWindow()
window.show()

app.exec()
