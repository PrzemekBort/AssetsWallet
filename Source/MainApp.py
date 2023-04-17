from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtWidgets import QMainWindow, QDialog, QWidget
from GUI.Interfaces import MainWindow_Interface, InputWindow_Interface, ErrorMessageBox_Interface
import GUI.Interfaces.Testowy as test


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

    def setNewWidgetValues(self, values: list):
        """Function takes and setup values entered in 'InputWindow' window. Values are forwarded
            to this function in list."""

        self.newWidgetName = str(values[0])
        self.newWidgetQuantity = str(values[1])
        self.newWidgetPrice = str(values[2])
        self.newWidgetDate = str(values[3])
        self.dataEnteredFlag = True

    # TODO dostosowanie funkcji do każdego typu Assetu
    def addNewWidgetTo(self, layout: QtWidgets.QLayout):
        """Function calls new window to eneter data for new widget. Calls 'createNewWidget' with entered data
            and add it to destiny layout."""

        # Flag to check if data from 'InputWindow' were forwarded correctly or window was just closed
        self.dataEnteredFlag = False

        self.newWindow = InputWindow()
        self.newWindow.enteredData.connect(self.setNewWidgetValues)
        self.newWindow.exec()

        # When data are forwarded correctly, flag is true and new widget can be created
        if self.dataEnteredFlag:
            self.newWidget = GoldWidget(self.newWidgetName, self.newWidgetQuantity,
                                        self.newWidgetPrice, self.newWidgetDate)
            self.newWidget.clickedWidget.connect(self.changeClickedWidget)

            layout.addWidget(self.newWidget)

    def deleteWidgetFrom(self, layout: QtWidgets.QLayout):
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


class InputWindow(QDialog):

    enteredData = QtCore.pyqtSignal(list)

    def __init__(self):
        super(InputWindow, self).__init__()
        self.ui = InputWindow_Interface.Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButton_subbmit.clicked.connect(self.confirm)
        self.ui.pushButton_cancel.clicked.connect(self.close)

    def confirm(self):
        # TODO Dodać komunikat gdy któraś rubryka jest pusta

        try:
            quantity = float(self.ui.lineEdit_quantity.text())
            price = float(self.ui.lineEdit_price.text())

        except ValueError:
            self.ui.lineEdit_quantity.clear()
            self.ui.lineEdit_price.clear()
            ErrorMessageBox('Wprowadzone wartości są błędne. Ilośc i cena muszą być liczbami.').exec()

        else:
            values = [self.ui.lineEdit_name.text(), quantity,
                      price, self.ui.lineEdit_date.text()]
            self.enteredData.emit(values)
            self.close()


class ErrorMessageBox(QDialog):

    def __init__(self, messageText):
        super(ErrorMessageBox, self).__init__()
        self.ui = ErrorMessageBox_Interface.Ui_Form()
        self.ui.setupUi(self)
        self.ui.label.setText(messageText)

        self.ui.pushButton.clicked.connect(self.close)


class AssetWidget(QWidget):

    clickedWidget = QtCore.pyqtSignal(list)

    def __init__(self):
        super(AssetWidget, self).__init__()
        # Opposite of current stylesheet. BASE=0, ALTERNATIVE=1.
        #   example: if current stylesheet is BASE, self.notCurrentStyle=1
        self.notCurrentStyle = 1

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        self.clickEvent(self.notCurrentStyle)

    def clickEvent(self, style: int):
        """Function change current stylesheet when widget is clicked
        and emit signal for MainWindow to change previous clicked widget to BASE stylesheet."""

        if style == 0:
            self.setBasedStylesheet()
            self.clickedWidget.emit([0, self])

        elif style == 1:
            # Change stylesheet to alternative for clicked widget
            self.setAlternativeStylesheet()
            self.clickedWidget.emit([1, self])

    def setBasedStylesheet(self):

        BASE_STYLESHEET = (
            "QFrame {\n"
            "    background-color: rgb(199, 199, 199);\n"
            "    color: rgb(0, 0, 0);\n"
            "    border-radius: 15px;\n"
            "}\n"
            ".QFrame {\n"
            "    border: 2px solid rgb(199, 199, 199);\n"
            "}")

        self.setStyleSheet(BASE_STYLESHEET)
        self.notCurrentStyle = 1

    def setAlternativeStylesheet(self):

        ALTERNATIVE_STYLESHEET = (
            "QFrame {\n"
            "    background-color: rgb(199, 199, 199);\n"
            "    border-radius: 15px;\n"
            "    color: rgb(0, 0, 0);\n"
            "}\n"
            ".QFrame {\n"
            "    border: 2px solid white\n"
            "}")
        self.setStyleSheet(ALTERNATIVE_STYLESHEET)
        self.notCurrentStyle = 0


class GoldWidget(AssetWidget):

    def __init__(self, name, quantity, price, date):
        super(GoldWidget, self).__init__()
        self.ui = test.Ui_Form()
        self.ui.setupUi(self)

        self.ui.NazwaLabel.setText(name)
        self.ui.IloscLabel.setText(quantity)
        self.ui.CenaLabel.setText(price)
        self.ui.DataLabel.setText(date)
