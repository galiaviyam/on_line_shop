class Product(object):
    def __init__(self, sku, display_name, price, discount="", description=""):
        self.sku = sku
        self.name = display_name
        self.price = price
        self.discount = discount
        self.description = description

    def modify(self):
        pass
