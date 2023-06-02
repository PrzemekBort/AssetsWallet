from PyQt6.QtWidgets import QApplication

from GUI.MainWindow import MainWindow
import GUI.AssetsWidgets as appWidgets
import Source.DataBaseFunctions as dbf
from Settings import dataBasePath


class MainProgram(QApplication):

    def __init__(self, arg):
        super(MainProgram, self).__init__(arg)
        self.MainWindow = MainWindow()
        self.dbConnection = dbf.connectDataBase(dataBasePath)
        self.MainWindow.show()

    def loadGoldAssets(self):
        """Load data trom GOLDSET table and add GoldWidgets to layout"""
        cursor = dbf.loadData(self.dbConnection, 'GOLDSET')
        if cursor is None:
            print('Data loading error.')

        else:
            for row in cursor:
                gold_ID = row[0]
                name = row[1]
                quantity = row[2]
                buyPrice = row[3]
                buyDate = row[4]
                goldForm = row[5]
                origin = row[6]
                finess = row[7]

                newGoldWidget = appWidgets.GoldWidget(gold_ID, name, quantity, buyPrice,
                                                      buyDate, goldForm, origin, finess)

                # TODO implement
