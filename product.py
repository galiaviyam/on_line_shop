import json


class Product(object):
    def __init__(self, sku, name, price, discount="", final_price="", description="", material="", color="", size="",
                 category="", homepage=""):
        self.sku = sku
        self.name = name
        self.price = price
        self.discount = discount
        self.final_price = final_price
        self.description = description
        self.material = material
        self.color = color
        self.size = size
        self.category = category
        self.homepage = homepage

    def print(self):
        product_json = json.dumps(self.__dict__)
        return product_json
