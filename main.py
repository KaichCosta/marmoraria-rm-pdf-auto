import sys
from PyQt6.QtWidgets import QApplication
from gui import PreencherPDFApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PreencherPDFApp()
    window.show()
    sys.exit(app.exec())
