import sys

from PySide6.QtWidgets import QApplication

from ownimage.font_generator.ui import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(300, 260)
    window.show()
    sys.exit(app.exec())
