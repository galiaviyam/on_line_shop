from database import Database
import json
import time
from product import Product

class User(object):
    def __init__(self, email, session_id, type="client", db=None, timeout=3600):
        self.email = email
        self.session_id = session_id
        self.type = type
        self.name = None
        self.db = db
        self.timeout = timeout
        self.error = ""

    def connect_to_db(self):
        if not self.db:
            with open("config.json", "r") as file:
                self.config = json.load(file)
            self.db = Database(self.config["database_name"])
            self.db.connect()

    def create_session(self):
        session_content = {"timestamp": time.time(), "creation_time": time.time(), "active": "yes"}
        record = self.db.add_record("session", session_content)
        self.session_id = record["id"]

    def check_session(self):
        if not self.session_id:
            self.create_session()
        db_filter = {"id": self.session_id}
        record = self.db.get_record("session", db_filter)
        timestamp = record["id"]
        if time.time() - self.timeout > timestamp:
            new_value = {"active": "no"}
            self.db.modify_record("session", db_filter, new_value)
            return False
        else:
            timestamp = {"timestamp": time.time()}
            self.db.modify_record("session", db_filter, timestamp)
            return True

    def login(self, email, password):
        user = {"email": self.email, "password": password}
        if not self.db:
            self.connect_to_db()
        record = self.db.get_record("users", user)
        if not record:
            return False
        self.email = email
        self.name = record["name"]
        self.type = record["type"]
        db_filter = {"id": self.session_id}
        new_value = {"email": self.email, "timestamp": time.time(), "active": "yes"}
        modified = self.db.modify_record("session", db_filter, new_value)
        db_filter = {"email": self.session_id}
        new_value = {"email": email}
        if self.db.get_record("carts", db_filter):
            cart = self.db.modify_record("carts", db_filter)
        if self.db.get_record("wishlist", db_filter):
            cart = self.db.modify_record("wishlist", db_filter)
        return True

    def change_password(self, email, old_password, new_password):
        try:
            if self.login(email, old_password):
                db_filter = {"email": email}
                new_values = {"password": new_password}
                self.db.modify_record("users", db_filter, new_values)
                return True
            else:
                return False
        except Exception:
            self.error = "There was an error with the email or password"


    def add_to_cart(self, email, sku):
        if not self.check_session():
            self.create_session()
        db_filter = {"email": email, "sku": sku}
        cart = self.db.add_record("carts", db_filter)
        if cart is not None:
            return True
        return False

    def remove_from_cart(self, email, sku):
        if not self.check_session():
            self.create_session()
        db_filter = {"email": email, "sku": sku}
        if self.db.get_record("carts", db_filter):
            cart = self.db.delete_record("carts", db_filter)
        else:
            return

    def show_cart(self, email):
        if not self.check_session():
            self.create_session()
        db_filter = {"email": email}
        records = self.db.get_records("carts", db_filter)
        cart = []
        total_price = 0
        for key, record in records.items():
            db_filter = {"sku": record["sku"]}
            product_record = self.db.get_record("products", db_filter)
            product = Product(record["sku"], product_record["name"], product_record["price"])
            cart.append(product)
            total_price += product_record["price"]
        return (cart, total_price)

    def checkout(self, email):
        if not self.check_session():
            self.create_session()
        print("Thank you for shopping")
        # at this point transaction was made and delivery was initiated
        order_num = self.db.get_next_number("orders", "order_number")
        (cart, total_price) = self.show_cart(email)
        date = time.ctime()
        db_filter = {"order_number": order_num, "date": date, "email": email}
        for item in cart:
            db_filter["product"] = item.sku
            db_filter["price"] = item.final_price
            db_filter["status"] = "new order"
            self.db.add_record("orders", db_filter)
        self.empty_cart(email)

    def empty_cart(self, email):
        if not self.check_session():
            self.create_session()
        db_filter = {"email": email}
        self.db.delete_record("carts", db_filter)

    def add_to_wishlist(self, email, sku):
        if not self.check_session():
            self.create_session()
        db_filter = {"email": email, "sku": sku}
        wishlist = {}
        if not self.db.get_record("wishlist", db_filter):
            wishlist = self.db.add_record("wishlist", db_filter)
        if wishlist is not None:
            return True
        return False

    def remove_from_wishlist(self, email, sku):
        if not self.check_session():
            self.create_session()
        db_filter = {"email": email, "sku": sku}
        if self.db.get_record("wishlist", db_filter):
            wishlist = self.db.delete_record("wishlist", db_filter)
        else:
            return

    def show_wishlist(self, email):
        if not self.check_session():
            self.create_session()
        db_filter = {"email": email}
        records = self.db.get_records("wishlist", db_filter)
        wishlist = []
        for key, record in records.items():
            db_filter = {"sku": record["sku"]}
            product_record = self.db.get_record("products", db_filter)
            product = Product(record["sku"], product_record["name"], product_record["price"])
            wishlist.append(product)
        return wishlist
