from abc import ABC, abstractmethod
from PyQt6 import QtCore, QtWidgets


def generateID():
    yield id in range(1, 1000)


class Assets(ABC):

    objectindex = 0

    @abstractmethod
    def __init__(self, name: str, quantity: float, total_cost: float, purchase_date: str, ID_key=generateID()):
        self.name = name
        self.quantity = quantity
        self.total_cost = total_cost
        self.purchase_date = purchase_date
        self._ID_key = ID_key

    def getName(self):
        return self.name

    def getQuantity(self):
        return self.quantity

    def getTotalcost(self):
        return self.total_cost

    def getPurchasedate(self):
        return self.purchase_date


class NominalCurrencySet:

    def __init__(self, currencyname: str, quantity: float):
        self.name = currencyname
        self.quantity = quantity

    def addquantity(self, amount: float):
        if amount > 0:
            self.quantity += amount
        else:
            print("Wrong value. Amount must be greater than 0.")

    def subtractquantity(self, amount: float):
        if self.quantity >= amount:
            self.quantity -= amount
        else:
            print(f"Wrong value. Value is greater than total amount of {self.name}.")

    def name(self):
        return self.name

    def totalquantity(self):
        return self.quantity

    def info(self):
        return tuple((self.name, self.quantity))


class GoldSet(Assets):

    OBJECT_LIST = []

    def __init__(self, name, quantity, total_cost, purchase_date, gold_type):
        super().__init__(name, quantity, total_cost, purchase_date)
        self._gold_type = gold_type
        self.OBJECT_LIST.append(self)

    def createWidget(self):
        self.new_widget = QtWidgets.QWidget()
        self.new_widget.setMaximumSize(QtCore.QSize(16777215, 50))
        self.new_widget.setMinimumHeight(50)
        self.new_widget.setStyleSheet("QWidget {\n"
                                      "    \n"
                                      "    background-color: rgb(199, 199, 199);\n"
                                      "    border-radius: 15px;\n"
                                      "}")

        self.label_nazwa = QtWidgets.QLabel(parent=self.new_widget)
        self.label_ilosc = QtWidgets.QLabel(parent=self.new_widget)
        self.label_cena = QtWidgets.QLabel(parent=self.new_widget)
        self.label_data = QtWidgets.QLabel(parent=self.new_widget)

        self.label_nazwa.setText(self.name)
        self.label_ilosc.setText(str(self.quantity))
        self.label_cena.setText(str(self.total_cost))
        self.label_data.setText(self.purchase_date)

        horizontalLayout = QtWidgets.QHBoxLayout(self.new_widget)
        horizontalLayout.addWidget(self.label_nazwa)
        horizontalLayout.addWidget(self.label_ilosc)
        horizontalLayout.addWidget(self.label_cena)
        horizontalLayout.addWidget(self.label_data)

        return self.new_widget


class CryptoSet(Assets):

    def __init__(self, name, quantity: float, total_cost, purchase_date, storage_place):
        super().__init__(name, quantity, total_cost, purchase_date)
        self.storage_place = storage_place


class ForeignCurrencySet(Assets, NominalCurrencySet):

    def __init__(self, name, quantity, total_cost, purchase_date):
        super(Assets).__init__(name, quantity, total_cost, purchase_date)


class SharesSet(Assets):

    def __init__(self, name, quantity: int, total_cost, purchase_date):
        super().__init__(name, quantity, total_cost, purchase_date)
