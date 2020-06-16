class Session(object):
    def __init__(self, session_id=None, timeout=None, email=None, db=None):
        self.id = session_id
        self.timeout = timeout
        self.email = email
        self.db = db
        if self.timeout is None:
            self.timeout = 3600
