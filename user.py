from database import Database
import json
import time
from product import Product


class User(object):
    def __init__(self, email, session_id, user_type="client", db=None, timeout=3600):
        self.email = email
        self.session_id = session_id
        self.type = user_type
        self.name = None
        self.db = db
        self.timeout = timeout
        self.error = ""
        self.config = ""

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
        if not self.email:
            self.email = record["id"]

    def check_session(self):
        if not self.session_id:
            self.create_session()
        db_filter = {"id": self.session_id}
        record = self.db.get_record("session", db_filter)
        timestamp = record["timestamp"]
        if time.time() - self.timeout > timestamp:
            new_value = {"active": "no"}
            self.db.modify_record("session", db_filter, new_value)
            return False
        else:
            timestamp = {"timestamp": time.time()}
            self.db.modify_record("session", db_filter, timestamp)
            return True

    def login(self, email, password):
        user = {"email": email, "password": password}
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
            cart = self.db.modify_record("carts", db_filter, new_value)
        if self.db.get_record("wishlist", db_filter):
            wishlist = self.db.modify_record("wishlist", db_filter, new_value)
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
        except Exception as e:
            self.error = "There was an error with the email or password"

    def add_to_cart(self, sku):
        if not self.check_session():
            self.create_session()
        db_filter = {"email": self.email, "sku": sku}
        cart = self.db.add_record("carts", db_filter)
        if cart is not None:
            return True
        return False

    def remove_from_cart(self, sku):
        if not self.check_session():
            self.create_session()
        db_filter = {"email": self.email, "sku": sku}
        if self.db.get_record("carts", db_filter):
            cart = self.db.delete_record("carts", db_filter)

    def show_cart(self):
        if not self.check_session():
            self.create_session()
        db_filter = {"email": self.email}
        records = self.db.get_records("carts", db_filter)
        cart_list = []
        cart_price = 0
        for key, record in records.items():
            db_filter = {"sku": record["sku"]}
            product_record = self.db.get_record("products", db_filter)
            product = Product(record["sku"], product_record["name"], product_record["price"], final_price=product_record["final_price"])
            cart_list.append(product)
            cart_price += product_record["final_price"]
        return (cart_list, cart_price)

    def checkout(self):
        try:
            if self.email == self.session_id or not self.check_session:
                return 2
            # at this point transaction was made and delivery was initiated
            order_num = self.db.get_next_number("orders", "order_number")
            (cart, total_price) = self.show_cart()
            date = time.ctime()
            db_filter = {"order_number": order_num, "date": date, "email": self.email}
            for item in cart:
                db_filter["product"] = item.sku
                db_filter["price"] = item.final_price
                db_filter["status"] = "new order"
                self.db.add_record("orders", db_filter)
            self.empty_cart()
            return 0
        except Exception as e:
            return 1

    def empty_cart(self):
        if not self.check_session():
            self.create_session()
        db_filter = {"email": self.email}
        self.db.delete_record("carts", db_filter)

    def add_to_wishlist(self, sku):
        if not self.check_session():
            self.create_session()
        db_filter = {"email": self.email, "sku": sku}
        wishlist = {}
        if not self.db.get_record("wishlist", db_filter):
            wishlist = self.db.add_record("wishlist", db_filter)
        if wishlist is not None:
            return True
        return False

    def remove_from_wishlist(self, sku):
        if not self.check_session():
            self.create_session()
        db_filter = {"email": self.email, "sku": sku}
        if self.db.get_record("wishlist", db_filter):
            wishlist = self.db.delete_record("wishlist", db_filter)

    def show_wishlist(self):
        if not self.check_session():
            self.create_session()
        db_filter = {"email": self.email}
        records = self.db.get_records("wishlist", db_filter)
        wishlist = []
        for key, record in records.items():
            db_filter = {"sku": record["sku"]}
            product_record = self.db.get_record("products", db_filter)
            product = Product(record["sku"], product_record["name"], product_record["price"])
            wishlist.append(product)
        return wishlist

    def get_user_type(self):
        db_filter = {"email": self.email}
        record = self.db.get_record("users", db_filter)
        return record["type"]
