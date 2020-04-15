from product_list import ProductList
from database import Database
from product import Product


class Store(object):
    def __init__(self):
        self.name = ""
        self.terms = ""
        self.product_list = ProductList()
        self.categories = {}

    def get_categories(self):
        filter = {}
        categories = Database.get_records("categories", filter)
        for key, category in categories.items():
            self.categories[key] = ""

    def get_store(self):
        columns = {"id": "1"}
        record = Database.get_record("stores", columns)
        self.name = record["name"]
        self.terms = record["terms"]
        self.get_categories()
        filter = {"homepage": "1"}
        records = Database.get_records("products", filter)
        for sku, record in records.items():
            product = Product(sku, record["name"], record["price"])
            result = self.product_list.add_item(product)

    def search(self, search_string="", category=""):
        pass

    def get_by_category(self, category):
        filter = {"category": category}
        records = Database.get_records("products", filter)
        products_by_category = ProductList()
        for sku, record in records.items():
            product = Product(sku, record["name"], record["price"])
            products_by_category.add_item(product)
        return products_by_category

    def add_to_cart(self, email, sku):
        filter = {"email": email, "sku": sku}
        cart = Database.add_record("carts", filter)
        if cart is not None:
            return True
        return False

    def show_cart(self, email):
        filter = {"email": email}
        records = Database.get_records("carts", filter)
        cart = ProductList()
        for key, record in records.items():
            filter = {"sku": record["sku"]}
            product_record = Database.get_record("products", filter)
            product = Product(record["sku"], product_record["name"], product_record["price"])
            cart.add_item(product)
            cart.total_price += product_record["price"]
        return cart

    def checkout(self, email):
        print("thank you for shopping")
        # at this point transaction was made and delivery was initiated
        self.empty_cart(email)

    def empty_cart(self, email):
        filter = {"email": email}
        Database.delete_record("carts", filter)
