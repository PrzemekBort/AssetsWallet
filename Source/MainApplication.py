from PyQt6.QtWidgets import QApplication

from GUI.MainWindow import MainWindow
import DataBaseFunctions as dbs


class MainProgram(QApplication):

    def __init__(self, arg):
        super(MainProgram, self).__init__(arg)
        self.MainWindow = MainWindow()
        self.dbConnection = dbs.connectDataBase('../Database/AssetsDataBase.db')
        self.MainWindow.show()
