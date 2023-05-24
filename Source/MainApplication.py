from PyQt6.QtWidgets import QApplication
from GUI.MainWindow import MainWindow


class MainProgram(QApplication):

    def __init__(self, arg):
        super(MainProgram, self).__init__(arg)
        self.appMainWindow = MainWindow()
        self.appMainWindow.show()
