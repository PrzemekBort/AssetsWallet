from PyQt6.QtWidgets import QMainWindow, QLayout

from GUI.InputWindow import InputDataWindow
from GUI.Interfaces import MainWindow_Interface

from GUI.AssetsWidgets import GoldWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = MainWindow_Interface.Ui_MainWindow()
        self.ui.setupUi(self)

        # Reference to current clicked widget in scrollArea
        self.currentClickedWidget = None

        # Change page buttons setup
        self.ui.pushButton_menu.clicked.connect(lambda: self.changePage('Menu', 0))
        self.ui.pushButton_gold.clicked.connect(lambda: self.changePage('Gold', 1))
        self.ui.pushButton_crypto.clicked.connect(lambda: self.changePage('Crypto', 2))
        self.ui.pushButton_currency.clicked.connect(lambda: self.changePage('Currency', 3))
        self.ui.pushButton_shares.clicked.connect(lambda: self.changePage('Shares', 4))
        self.ui.pushButton_cash.clicked.connect(lambda: self.changePage('Cash', 5))
        self.ui.pushButton_settings.clicked.connect(lambda: self.changePage('Settings', 6))

        # Add buttons setup
        self.ui.pushButton_gold_add.clicked.connect(
            lambda: self.createNewGoldWidget(self.ui.destinationVerticalLayout_gold))
        self.ui.pushButton_crypto_add.clicked.connect(
            lambda: self.createNewGoldWidget(self.ui.destinationVerticalLayout_crypto))
        self.ui.pushButton_currency_add.clicked.connect(
            lambda: self.createNewGoldWidget(self.ui.destinationVerticalLayout_currency))
        self.ui.pushButton_shares_add.clicked.connect(
            lambda: self.createNewGoldWidget(self.ui.destinationVerticalLayout_shares))

        # Delete buttons setup
        self.ui.pushButton_gold_delete.clicked.connect(
            lambda: self.deleteWidgetFrom(self.ui.destinationVerticalLayout_gold))
        self.ui.pushButton_crypto_delete.clicked.connect(
            lambda: self.deleteWidgetFrom(self.ui.destinationVerticalLayout_crypto))
        self.ui.pushButton_currency_delete.clicked.connect(
            lambda: self.deleteWidgetFrom(self.ui.destinationVerticalLayout_currency))
        self.ui.pushButton_shares_delete.clicked.connect(
            lambda: self.deleteWidgetFrom(self.ui.destinationVerticalLayout_shares))

    def changePage(self, newText: str, newPageIndex: int):
        """The function changes the currently displayed page in a MainStackedWidget
            and text in main label."""

        self.ui.label.setText(newText)
        self.ui.MainStackedWidget.setCurrentIndex(newPageIndex)

    def createNewGoldWidget(self):
        """Function calls new window to eneter data for new widget and create new asset widget"""

        # Dictionary for values emited from InputWidget
        enteredValues = dict()

        self.newWindow = InputDataWindow()
        self.newWindow.enteredData.connect(enteredValues.update)
        self.newWindow.exec()

        # When data are forwarded correctly, enteredValues are not empty dict
        if enteredValues:
            self.newWidget = GoldWidget(enteredValues['Name'], enteredValues['Quantity'], enteredValues['Price'])
            self.addNewGoldWidget(self.newWidget)

    def deleteWidgetFrom(self, layout: QLayout):
        """Function removes widget from layout and delete widget"""
        
        # Checking if any widget is clicked
        if self.currentClickedWidget:
            layout.removeWidget(self.currentClickedWidget)
            self.currentClickedWidget.deleteLater()
            self.currentClickedWidget = None

    def changeClickedWidget(self, lista):

        if lista[0]:
            if self.currentClickedWidget:
                self.currentClickedWidget.setBasedStylesheet()

            self.currentClickedWidget = lista[1]

        else:
            self.currentClickedWidget = None

    def addNewGoldWidget(self, goldWidgetObject: GoldWidget):
        goldWidgetObject.clickedWidget.connect(self.changeClickedWidget)
        self.ui.destinationVerticalLayout_gold.addWidget(goldWidgetObject)



