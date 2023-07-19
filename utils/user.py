""" User class """

class User:
    """User class"""

    def __init__(self, user_id = None, username = None, password_hash = None, email = None, steam_id = None, created_at = None, last_login = None):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.steam_id = steam_id
        self.created_at = created_at
        self.last_login = last_login

    def __str__(self):
        return f"User ID: {self.user_id}, Username: {self.username}, Email: {self.email}, Steam ID: {self.steam_id}, Created at: {self.created_at}, Last Login: {self.last_login}"

    def get_user_id(self):
        """returns the user ID"""
        return self.user_id

    def get_username(self):
        """returns the username"""
        return self.username

    def get_password_hash(self):
        """returns the password hash"""
        return self.password_hash

    def get_email(self):
        """returns the email"""
        return self.email

    def get_steam_id(self):
        """returns the Steam ID"""
        return self.steam_id

    def get_created_at(self):
        """returns the created_at timestamp"""
        return self.created_at

    def get_last_login(self):
        """returns the last login timestamp"""
        return self.last_login

    def to_json(self):
        """returns the User object as JSON"""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "password_hash": self.password_hash,
            "email": self.email,
            "steam_id": self.steam_id,
            "created_at": self.created_at,
            "last_login": self.last_login
        }
