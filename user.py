from database import Database
from session import Session


class User(object):
    def __init__(self, email, password):
        self.name = ""
        self.password = password
        self.email = email
        self.address = ""
        self.type = ""

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
        record = Database.get_record("users", user)
        if record is not None:
            session_id = Session()
            session_id.create_session(self.email)
            if session_id is not None:
                return session_id
        return None

