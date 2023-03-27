from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtWidgets import QMainWindow, QDialog
from GUI.Interfaces.Interface import Ui_MainWindow
from GUI.Interfaces.InputFormInterface import Ui_Form
from GUI.Interfaces import WrongDataInfoWidget

# TODO ogarnąć Githuba


class MainWindow(QMainWindow):

    # Reference to current clicked widget in scrollArea
    currentClickedWidget = None

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

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
            lambda: self.deleteWidget(self.ui.destinationVerticalLayout_gold))
        self.ui.pushButton_crypto_delete.clicked.connect(
            lambda: self.deleteWidget(self.ui.destinationVerticalLayout_crypto))
        self.ui.pushButton_currency_delete.clicked.connect(
            lambda: self.deleteWidget(self.ui.destinationVerticalLayout_currency))
        self.ui.pushButton_shares_delete.clicked.connect(
            lambda: self.deleteWidget(self.ui.destinationVerticalLayout_shares))

    def changePage(self, newText: str, newPageIndex: int):
        """The function changes the currently displayed page in a MainStackedWidget
            and text in main label."""
        
        _translate = QtCore.QCoreApplication.translate
        self.ui.label.setText(_translate("MainWindow", newText))
        self.ui.MainStackedWidget.setCurrentIndex(newPageIndex)

    def createNewWidget(self, name, quantity, total_cost, purchase_date, ID_key=0):
        """Function creates, setup and returns new widget."""
        # TODO ogarnięcie ID_key, nie może być 0

        BASE_STYLESHEET = (
            "QWidget {\n"
            "    background-color: rgb(199, 199, 199);\n"
            "    border-radius: 15px;\n"
            "}")
        ALTERNATIVE_STYLESHEET = (
            "QWidget {\n"
            "    background-color: rgb(199, 199, 199);\n"
            "    border-radius: 15px;\n"
            "}\n"
            ".QWidget {\n"
            "     border: 2px solid white\n"
            "}")

        newWidget = QtWidgets.QWidget()
        newWidget.setObjectName('newWidget')
        newWidget.ID_key = ID_key

        newWidget.setMaximumSize(QtCore.QSize(16777215, 50))
        newWidget.setMinimumHeight(50)
        newWidget.setStyleSheet(BASE_STYLESHEET)
        newWidget.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))

        labelName = QtWidgets.QLabel(parent=newWidget)
        labelQuantity = QtWidgets.QLabel(parent=newWidget)
        labelPrice = QtWidgets.QLabel(parent=newWidget)
        labelDate = QtWidgets.QLabel(parent=newWidget)

        labelName.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        labelQuantity.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        labelPrice.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        labelDate.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        labelName.setText(name)
        labelQuantity.setText(quantity)
        labelPrice.setText(total_cost)
        labelDate.setText(purchase_date)

        horizontalLayout = QtWidgets.QHBoxLayout(newWidget)
        horizontalLayout.addWidget(labelName)
        horizontalLayout.addWidget(labelQuantity)
        horizontalLayout.addWidget(labelPrice)
        horizontalLayout.addWidget(labelDate)

        # Variable opposite to the currently set stylesheet version. Variable can be only 0 or 1
        newWidget.not_current_style = 1
        
        def clickEvent(version: int):
            """Function change current stylesheet when widget is clicked. 
                Changes stylesheet to based of last clicked widget also"""
            
            # Change stylesheet to based
            if version == 0:
                newWidget.setStyleSheet(BASE_STYLESHEET)
                newWidget.not_current_style = 1
                self.currentClickedWidget = None

            elif version == 1:
                # Change stylesheet to alternative for clicked widget
                newWidget.setStyleSheet(ALTERNATIVE_STYLESHEET)
                newWidget.not_current_style = 0

                # and to based for last clicked widget
                if self.currentClickedWidget:
                    self.currentClickedWidget.setStyleSheet(BASE_STYLESHEET)
                    self.currentClickedWidget.not_current_style = 1

                self.currentClickedWidget = newWidget

        newWidget.mouseReleaseEvent = lambda event: clickEvent(newWidget.not_current_style)

        return newWidget

    def setNewWidgetValues(self, values: list):
        """Function takes and setup values entered in 'InputWidget' window. Values are forwarded
            to this function in list."""

        self.newWidgetName = str(values[0])
        self.newWidgetQuantity = str(values[1])
        self.newWidgetPrice = str(values[2])
        self.newWidgetDate = str(values[3])
        self.dataEnteredFlag = True

    # TODO dostosowanie funkcji do każdego typu Assetu
    def addNewWidgetTo(self, destiny):
        """Function calls new window to eneter data for new widget. Calls 'createNewWidget' with entered data
            and add it to destiny layout."""

        # Flag to check if data from 'InputWidget' were forwarded correctly or window was just closed
        self.dataEnteredFlag = False

        self.newWindow = InputWidget()
        self.newWindow.enteredData.connect(self.setNewWidgetValues)
        self.newWindow.exec()

        # When data are forwarded correctly, flag is true and new widget can be created
        if self.dataEnteredFlag:
            self.newWidget = self.createNewWidget(self.newWidgetName, str(self.newWidgetQuantity),
                                                  str(self.newWidgetPrice), self.newWidgetDate)
            destiny.addWidget(self.newWidget)

    def deleteWidget(self, destiny):
        """Function removes widget from layout and delete widget"""
        
        # Checking if any widget is clicked
        if self.currentClickedWidget:
            destiny.removeWidget(self.currentClickedWidget)
            self.currentClickedWidget.deleteLater()
            self.currentClickedWidget = None


class InputWidget(QDialog):

    enteredData = QtCore.pyqtSignal(list)

    def __init__(self):
        super(InputWidget, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButton_subbmit.clicked.connect(self.confirm)

    def confirm(self):
        # TODO Dodać komunikat gdy któraś rubryka jest pusta

        try:
            quantity = float(self.ui.lineEdit_quantity.text())
            price = float(self.ui.lineEdit_price.text())

        except ValueError:
            self.ui.lineEdit_quantity.clear()
            self.ui.lineEdit_price.clear()
            errorInfoWidget = WrongDataInfo()
            errorInfoWidget.exec()

        else:
            values = [self.ui.lineEdit_name.text(), quantity,
                      price, self.ui.lineEdit_date.text()]
            self.enteredData.emit(values)
            self.close()


class WrongDataInfo(QDialog):

    def __init__(self):
        super(WrongDataInfo, self).__init__()
        self.ui = WrongDataInfoWidget.Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.close)
