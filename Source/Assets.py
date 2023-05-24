class Asset:

    def __init__(self, name, quantity, buyPrice, buyDate='01.01.2023'):
        self.name = name
        self.quantity = quantity
        self.buyPrice = buyPrice
        self.buyDate = buyDate

    def changeName(self, newName: str):
        self.name = newName

    def changeQuantity(self, newQuantity: float):
        pass
