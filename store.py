from database import Database
import json
from sqlite3 import IntegrityError
from user import User
from product import Product
from tabulate import tabulate


class Store(object):
    def __init__(self, config_file):
        self.config_file = config_file
        self.name = ""
        self.terms = ""
        self.categories = {}
        self.db = None
        self.config = None
        self.product_list = []
        self.error = ""
        self.timeout = 3600
        self.session_id = None
        self.user = None

    def get_store(self):
        with open(self.config_file, "r") as file:
            self.config = json.load(file)
        if "timeout" in self.config:
            self.timeout = self.config["timeout"]
        self.db = Database(self.config["database_name"])
        self.user = User(self.session_id, self.session_id, db=self.db)
        if not self.user.check_session():
            self.user.create_session()
        columns = {"id": "1"}
        record = self.db.get_record("stores", columns)
        self.name = record["name"]
        self.terms = record["terms"]
        self.get_categories()
        self.update_homepage()

    def update_homepage(self):
        self.product_list = []
        db_filter = {"homepage": "1"}
        records = self.db.get_records("products", db_filter)
        for UID, record in records.items():
            product = Product(record["sku"], record["name"], record["price"], record["discount"], record["final_price"],
                              record["description"], record["material"], record["color"], record["size"])
            result = self.product_list.append(product)

    def get_categories(self):
        db_filter = {}
        categories = self.db.get_records("categories", db_filter)
        category_list = []
        for uid, category in categories.items():
            category_list.append(categories[uid])
            self.categories[category["category"]] = uid
        return category_list

    def get_users(self, user_type):
        db_filter = {"type": user_type}
        users = self.db.get_records("users", db_filter)
        return users

    def search(self, search_string="", category=""):
        db_filter = [("sku", search_string, "="), ("name", search_string, "LIKE"), ("description", search_string, "LIKE")]
        if category != "":
            db_filter.append(("category", category, "="))
        records = self.db.search("products", db_filter)
        search_results = []
        for uid, record in records.items():
            product = Product(record["sku"], record["name"], record["price"], record["discount"], record["final_price"],
                              record["description"], record["material"], record["color"], record["size"])
            search_results.append(product)
        return search_results

    def get_by_category(self, category):
        db_filter = {"category": category}
        records = self.db.get_records("products", db_filter)
        products_by_category = []
        for sku, record in records.items():
            product = Product(record["sku"], record["name"], record["price"], record["discount"], record["final_price"],
                              record["description"], record["material"], record["color"], record["size"])
            products_by_category.append(product)
        return products_by_category

    def add_user(self, email, password, name="", user_type="client", country="", city="", street="", house_num="",
                 apartment="", entrance="", zip_code="", phone=""):
        try:
            db_filter = {"email": email, "password": password, "name": name, "type": user_type, "country": country,
                         "city": city, "street": street, "house_num": house_num, "apartment": apartment,
                         "entrance": entrance, "zip_code": zip_code, "phone": phone}
            self.db.add_record("users", db_filter)
        except IntegrityError:
            self.error = "A user with email %s already exists" % email
            return False
        return True

    def delete_user(self, email):
        try:
            db_filter = {"email": email}
            result = self.db.get_record("users", db_filter)
            deleted = self.db.delete_record("users", db_filter)
            success = "User %s deleted successfully" % email
            return success
        except IntegrityError:
            self.error = "A product with email %s does not exist" % email

    @staticmethod
    def get_product_price(price, discount):
        try:
            if discount != "":
                if int(discount) > 100 or int(discount) < 0:
                    raise Exception
                result = int(price) * (100 - int(discount)) / 100
                result = int(result)
                return result
            else:
                return price
        except Exception as e:
            return price

    def add_product(self, sku, name, price, discount="", description="", material="", color="", size="", category="",
                    homepage=""):
        product = None
        try:
            final_price = Store.get_product_price(price, discount)
            db_filter = {"sku": sku, "name": name, "price": price, "discount": discount, "final_price": final_price,
                         "description": description, "material": material, "color": color, "size": size,
                         "category": category, "homepage": homepage}
            result = self.db.add_record("products", db_filter)
            product = Product(sku=result["sku"], name=result["name"], price=result["price"],
                              discount=result["discount"], final_price=result["final_price"],
                              description=result["description"], material=result["material"], color=result["color"],
                              size=result["size"], category=result["category"], homepage=result["homepage"])
        except IntegrityError:
            self.error = "A product with SKU %s already exists" % sku
        return product

    def modify_product(self, sku, **new_values):
        product = None
        try:
            db_filter = {"sku": sku}
            result = self.db.get_record("products", db_filter)
            for key in list(new_values):
                if not new_values[key]:
                    del new_values[key]
            price = new_values["price"] if "price" in new_values else result["price"]
            discount = new_values["discount"] if "discount" in new_values else result["discount"]
            new_values["final_price"] = self.get_product_price(price, discount)
            result = self.db.modify_record("products", result, new_values)
            product = Product(sku=result["sku"], name=result["name"], price=result["price"],
                              discount=result["discount"], final_price=result["final_price"],
                              description=result["description"], material=result["material"],
                              color=result["color"], size=result["size"], category=result["category"],
                              homepage=result["homepage"])
            print("Product modified successfully")
        except Exception as e:
            self.error = "There was an error with sku %s" % sku
        return product

    def delete_product(self, sku):
        try:
            db_filter = {"sku": sku}
            result = self.db.get_record("products", db_filter)
            product = Product(sku=result["sku"], name=result["name"], price=result["price"],
                              discount=result["discount"], final_price=result["final_price"],
                              description=result["description"], material=result["material"], color=result["color"],
                              size=result["size"], category=result["category"], homepage=result["homepage"])
            deleted = self.db.delete_record("products", db_filter)
            print("Product deleted successfully")
            return product
        except IntegrityError as e:
            self.error = "A product with SKU %s does not exist" % sku

    def show_orders(self):
        orders = {}
        db_filter = {"status": "new order"}
        records = self.db.get_records("orders", db_filter)
        for UID, record in records.items():
            if record["order_number"] in orders:
                orders[record["order_number"]]["items"].append(
                    {"product": record["product"], "price": record["price"]})
            else:
                orders[record["order_number"]] = {
                    "email": record["email"],
                    "date": record["date"],
                    "status": record["status"],
                    "items": [{"product": record["product"], "price": record["price"]}]
                }
        for order, details in orders.items():
            print("order number: " + str(order))
            print("email: " + orders[order]["email"])
            print("status: " + orders[order]["status"])
            headers = ["item", "price"]
            table = [x.values() for x in orders[order]["items"]]
            print(tabulate(table, headers, tablefmt="grid"))
            print("")

    def add_category(self, category):
        try:
            db_filter = {"category": category}
            self.db.add_record("categories", db_filter)
        except IntegrityError:
            self.error = "A category %s already exists" % category
            return False
        return True
