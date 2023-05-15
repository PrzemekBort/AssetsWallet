from PyQt6.QtWidgets import QWidget
from PyQt6 import QtCore, QtGui
from GUI.Interfaces import GoldWidget_Interface


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

    def __init__(self, name, quantity, value):
        super(GoldWidget, self).__init__()
        self.ui = GoldWidget_Interface.Ui_Form()
        self.ui.setupUi(self)

        self.ui.nameLabel.setText(name)
        self.ui.quantityLabel.setText(quantity)
        self.ui.valueLabel.setText(value)
        self.ui.priceLabel.setText('No data')
        self.ui.profitLossLabel.setText('No data')