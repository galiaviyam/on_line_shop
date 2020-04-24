from product_list import ProductList
from database import Database
from product import Product
import json


class Store(object):
    def __init__(self, name):
        self.name = name
        self.terms = ""
        self.product_list = ProductList()
        self.categories = {}
        self.db = None
        self.config = None

    def get_categories(self):
        filter = {}
        categories = self.db.get_records("categories", filter)
        for uid, category in categories.items():
            self.categories[category["category"]] = uid

    def get_store(self):
        with open("config.json", "r") as file:
            self.config = json.load(file)
        self.db = Database(self.config["database_name"])
        self.db.connect()
        columns = {"id": "1"}
        record = self.db.get_record("stores", columns)
        self.name = record["name"]
        self.terms = record["terms"]
        self.get_categories()
        filter = {"homepage": "1"}
        records = self.db.get_records("products", filter)
        for sku, record in records.items():
            product = Product(sku, record["name"], record["price"])
            result = self.product_list.add_item(product)

    def search(self, search_string="", category=""):
        filter = [("sku", search_string, "="), ("name", search_string, "LIKE"), ("description", search_string, "LIKE")]
        if category != "":
            filter.append(("category", category, "="))
        records = self.db.search("products", filter)
        search_results = ProductList()
        for sku, record in records.items():
            product = Product(sku, record["name"], record["price"])
            search_results.add_item(product)
        return search_results


    def get_by_category(self, category):
        filter = {"category": category}
        records = self.db.get_records("products", filter)
        products_by_category = ProductList()
        for sku, record in records.items():
            product = Product(sku, record["name"], record["price"])
            products_by_category.add_item(product)
        return products_by_category

    def add_to_cart(self, email, sku):
        filter = {"email": email, "sku": sku}
        cart = self.db.add_record("carts", filter)
        if cart is not None:
            return True
        return False

    def show_cart(self, email):
        filter = {"email": email}
        records = self.db.get_records("carts", filter)
        cart = ProductList()
        for key, record in records.items():
            filter = {"sku": record["sku"]}
            product_record = self.db.get_record("products", filter)
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
        self.db.delete_record("carts", filter)
    
    def add_to_wishlist(self, email, sku):
        filter = {"email": email, "sku": sku}
        wishlist = {}
        if not self.db.get_record("wishlist", filter):
            wishlist = self.db.add_record("wishlist", filter)
        if wishlist is not None:
            return True
        return False

    def remove_from_wishlist(self, email, sku):
        filter = {"email": email, "sku": sku}
        if self.db.get_record("wishlist", filter):
            wishlist = self.db.delete_record("wishlist", filter)
        else:
            return

    def show_wishlist(self, email):
        filter = {"email": email}
        records = self.db.get_records("wishlist", filter)
        wishlist = ProductList()
        for key, record in records.items():
            filter = {"sku": record["sku"]}
            product_record = self.db.get_record("products", filter)
            product = Product(record["sku"], product_record["name"], product_record["price"])
            wishlist.add_item(product)
            wishlist.total_price += product_record["price"]
        return wishlist
