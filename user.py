from database import Database
from session import Session
import json


class User(object):
    def __init__(self, email, password, country="", city="", street="", house_num="", apartment="", entrance="", zip_code="", phone=""):
        self.name = ""
        self.password = password
        self.email = email
        self.country = country
        self.city = city
        self.street = street
        self.house_num = house_num
        self.apartment = apartment
        self.entrance = entrance
        self.zip_code = zip_code
        self.phone = phone
        self.type = ""
        self.db = None

    def connect_to_db(self):
        with open("config.json", "r") as file:
            self.config = json.load(file)
        self.db = Database(self.config["database_name"])
        self.db.connect()


    def login(self):
        user = {"email": self.email, "password": self.password}
        if self.db is None:
            self.connect_to_db()
        record = self.db.get_record("users", user)
        # if record is not None:
        #     session_id = Session()
        #     session_id.create_session(self.email)
        #     if session_id is not None:
        #         return session_id
        return None

