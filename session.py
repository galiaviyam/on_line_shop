import time
from database import Database


class Session(object):
    def __init__(self, session_id=None, timeout=None):
        self.id = session_id
        self.time_stamp = time.time()
        self.timeout = timeout
        if self.timeout is None:
            self.timeout = 3600

    def create_session(self, email):
        session_content = {"email": email, "time_stamp": self.time_stamp}
        record = Database.add_record("sessions", session_content)
        self.id = record["id"]