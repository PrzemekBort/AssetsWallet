from PyQt6 import QtCore
from PyQt6.QtWidgets import QDialog

from GUI.Interfaces import InputWindow_Interface, ErrorMessageBox_Interface


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