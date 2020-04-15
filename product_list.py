from product import Product


class ProductList(object):
    def __init__(self):
        self.product_list = []
        self.list_id = 0
        self.total_price = 0

    def add_item(self, product):
        if not isinstance(product, Product):
            return False
        self.product_list.append(product)
        return True

    def remove_item(self):
        pass

    def change_quantity(self):
        pass
