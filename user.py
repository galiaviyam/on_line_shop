from database import Database
from session import Session
from address import Address
import json


class User(object):
    def __init__(self, email, password):
        self.name = ""
        self.password = password
        self.email = email
        self.address = Address()
        self.type = ""
        self.db = None

    def connect_to_db(self):
        with open("config.json", "r") as file:
            self.config = json.load(file)
        self.db = Database(self.config["database_name"])
        self.db.connect()

    def add(self):
        pass

    def delete(self):
        pass

    def modify(self):
        pass

    def get_param(self):
        pass

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

