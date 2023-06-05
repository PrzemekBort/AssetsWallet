from PyQt6.QtWidgets import QWidget
from PyQt6 import QtCore, QtGui
from abc import abstractmethod

from GUI.Interfaces import Widget_Interface
import Source.WebScraper as WS


class AssetWidget(QWidget):

    clickedWidget = QtCore.pyqtSignal(list)

    def __init__(self, ID: int, name: str, quantity: float, buyPrice: float, buyDate=None):
        super(AssetWidget, self).__init__()
        self.ui = Widget_Interface.Ui_Form()
        self.ui.setupUi(self)

        # Parameters bellow are common for all asset types
        self.ID = ID  # PRIMARY KEY in database
        self.name = name
        self.quantity = quantity  # Quantity in ounces
        self.buyPrice = buyPrice
        self.buyDate = buyDate

        # Opposite of current stylesheet. BASE=0, ALTERNATIVE=1.
        self.notCurrentStyle = 1

    # SETTING LABELS
    def setNameLabel(self, name: str):
        self.ui.nameLabel.setText(name)

    def setQuantityLabel(self, quantity: float):
        self.ui.quantityLabel.setText(str(quantity))

    def setCurrentValueLabel(self, value: float):
        self.ui.currentValueLabel.setText(str(value))

    def setProfitLossRatioLabel(self, ratio: float):
        self.ui.profitLossLabel.setText(str(ratio))

    # SETTING EVENTS
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

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        self.clickEvent(self.notCurrentStyle)

    # SETTING STYLESHEETS
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

    # FUNCTIONALITY
    @abstractmethod
    def countCurrentValue(self):
        pass

    def countProfitRate(self):
        value = self.countCurrentValue()
        return value - self.buyPrice


class GoldWidget(AssetWidget):

    def __init__(self, Gold_ID: int, name: str, quantity: float, buyPrice: float, buyDate=None, goldFormType=None,
                 goldOrigin=None, goldFiness=None):

        super(GoldWidget, self).__init__(Gold_ID, name, quantity, buyPrice, buyDate)
        self.goldFormType = goldFormType   # Type of gold form e.g. coin, billet, contract
        self.goldOrigin = goldOrigin
        self.goldFiness = goldFiness

        self.setNameLabel(self.name)
        self.setQuantityLabel(self.quantity)
        self.countCurrentValue()
        self.setCurrentValueLabel(self.countCurrentValue())
        self.setProfitLossRatioLabel(self.countProfitRate())

    def countCurrentValue(self):
        goldPrice = WS.getGoldPricePLN()
        return goldPrice * self.quantity  # Price for 1 ounce * ounces quantity


