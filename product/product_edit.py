class ProductEdit:

    def __init__(self, id, code, name, price, catgrId):
        self.id = id
        self.code = code
        self.name = name
        self.price = price
        self.catgrId = catgrId

    def validate(self):
        # ex : check apakah name unique or not ?
        return True