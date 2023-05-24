import sys
from PyQt6.QtWidgets import QApplication
from GUI.MainWindow import MainWindow
from Source.MainApplication import MainProgram


if __name__ == "__main__":
    app = MainProgram(sys.argv)
    sys.exit(app.exec())
