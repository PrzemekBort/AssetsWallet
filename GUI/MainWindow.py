from PyQt6 import QtCore
from PyQt6.QtWidgets import QMainWindow, QDialog, QLayout
from GUI.Interfaces import MainWindow_Interface, InputWindow_Interface, ErrorMessageBox_Interface

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
            lambda: self.addNewWidgetTo(self.ui.destinationVerticalLayout_gold))
        self.ui.pushButton_crypto_add.clicked.connect(
            lambda: self.addNewWidgetTo(self.ui.destinationVerticalLayout_crypto))
        self.ui.pushButton_currency_add.clicked.connect(
            lambda: self.addNewWidgetTo(self.ui.destinationVerticalLayout_currency))
        self.ui.pushButton_shares_add.clicked.connect(
            lambda: self.addNewWidgetTo(self.ui.destinationVerticalLayout_shares))

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

    def addNewWidgetTo(self, layout: QLayout):
        """Function calls new window to eneter data for new widget and create new asset widget"""

        # Dictionary for values emited from InputWidget
        enteredValues = dict()

        self.newWindow = InputDataWindow()
        self.newWindow.enteredData.connect(enteredValues.update)
        self.newWindow.exec()

        # When data are forwarded correctly, enteredValues are not empty dict
        if enteredValues:
            self.newWidget = GoldWidget(enteredValues['Name'], enteredValues['Quantity'], enteredValues['Price'])
            self.newWidget.clickedWidget.connect(self.changeClickedWidget)

            layout.addWidget(self.newWidget)

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


class InputDataWindow(QDialog):

    enteredData = QtCore.pyqtSignal(dict)

    def __init__(self):
        super(InputDataWindow, self).__init__()
        self.ui = InputWindow_Interface.Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButton_subbmit.clicked.connect(self.confirm)
        self.ui.pushButton_cancel.clicked.connect(self.close)

    def confirm(self):
        nameIsEntered, quantityIsEntered, priceIsEntered = True, True, True

        # Checking if neccesarry fields are entered
        if self.ui.lineEdit_name.text() == '':
            nameIsEntered = False
            self.ui.label_name.setStyleSheet('color: red;')
        else:
            nameIsEntered = True
            self.ui.label_name.setStyleSheet('color: white')

        if self.ui.lineEdit_quantity.text() == '':
            quantityIsEntered = False
            self.ui.label_quantity.setStyleSheet('color: red;')
        else:
            quantityIsEntered = True
            self.ui.label_quantity.setStyleSheet('color: white')

        if self.ui.lineEdit_totalprice.text() == '':
            priceIsEntered = False
            self.ui.label_totlacprice.setStyleSheet('color: red;')
        else:
            priceIsEntered = True
            self.ui.label_totlacprice.setStyleSheet('color: white')

        if (nameIsEntered and quantityIsEntered and priceIsEntered) is True:
            # Checking if quantity and price values are numbers
            try:
                quantity = float(self.ui.lineEdit_quantity.text())
                totalPrice = float(self.ui.lineEdit_totalprice.text())

            except ValueError:
                MessageBox('Wrong values. Qunatity and price must be numbers.').exec()

            else:
                values = {'Name': str(self.ui.lineEdit_name.text()), 'Quantity': str(quantity),
                          'Price': str(totalPrice), 'Date': str(self.ui.lineEdit_date),
                          'StoragePlace': str(self.ui.lineEdit_storage)}

                self.enteredData.emit(values)
                self.close()

        else:
            MessageBox('Not all mandatory values are provided!').exec()


class MessageBox(QDialog):

    def __init__(self, messageText):
        super(MessageBox, self).__init__()
        self.ui = ErrorMessageBox_Interface.Ui_Form()
        self.ui.setupUi(self)
        self.ui.label.setText(messageText)

        self.ui.pushButton.clicked.connect(self.close)
