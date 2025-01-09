import hashlib

class User:
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash

    def check_password(self, password):
        """Check if the provided password matches the stored hash."""
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return hashed_password == self.password_hash