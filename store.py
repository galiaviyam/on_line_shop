from database import Database
import json


class Store(object):
    def __init__(self, name):
        self.name = name
        self.terms = ""
        self.categories = {}
        self.db = None
        self.config = None
        self.product_list = []

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
        for UID, record in records.items():
            product = Product(record["sku"], record["name"], record["price"])
            result = self.product_list.append(product)

    def search(self, search_string="", category=""):
        filter = [("sku", search_string, "="), ("name", search_string, "LIKE"), ("description", search_string, "LIKE")]
        if category != "":
            filter.append(("category", category, "="))
        records = self.db.search("products", filter)
        search_results = []
        for sku, record in records.items():
            product = Product(sku, record["name"], record["price"])
            search_results.append(product)
        return search_results


    def get_by_category(self, category):
        filter = {"category": category}
        records = self.db.get_records("products", filter)
        products_by_category = []
        for sku, record in records.items():
            product = Product(sku, record["name"], record["price"])
            products_by_category.append(product)
        return products_by_category

    def add_user(self):
        pass

    def delete_user(self):
        pass

    def add_to_cart(self, email, sku):
        filter = {"email": email, "sku": sku}
        cart = self.db.add_record("carts", filter)
        if cart is not None:
            return True
        return False

    def show_cart(self, email):
        filter = {"email": email}
        records = self.db.get_records("carts", filter)
        cart = []
        total_price = 0
        for key, record in records.items():
            filter = {"sku": record["sku"]}
            product_record = self.db.get_record("products", filter)
            product = Product(record["sku"], product_record["name"], product_record["price"])
            cart.append(product)
            total_price += product_record["price"]
        return (cart, total_price)

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
        wishlist = []
        for key, record in records.items():
            filter = {"sku": record["sku"]}
            product_record = self.db.get_record("products", filter)
            product = Product(record["sku"], product_record["name"], product_record["price"])
            wishlist.append(product)
        return wishlist


class Product(object):
    def __init__(self, sku, display_name, price, discount="", description="", material="", color="", size=""):
        self.sku = sku
        self.name = display_name
        self.price = price
        self.discount = discount
        self.description = description
        self.material = material
        self.color = color
        self.size = size
