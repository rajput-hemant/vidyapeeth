from werkzeug.security import check_password_hash, generate_password_hash

from lib.extensions import db
from lib.utils import generate_uuid


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(), primary_key=True, default=str(generate_uuid()))
    username = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.Text())

    def __init__(self, username: str, email: str):
        """
        Initialize the User model
        """
        self.username = username
        self.email = email

    def __repr__(self):
        """
        String representation of the User model
        """
        return f"<User {self.username}>"

    def set_password(self, password: str):
        """
        Set the password for the User model
        """
        self.password = generate_password_hash(password)

    def check_password(self, password: str):
        """
        Check the password for the User model
        """
        return check_password_hash(self.password, password)

    @classmethod
    def get_user_by_username(cls, username: str):
        """
        Get a user by username
        """
        return cls.query.filter_by(username=username).first()

    def save(self):
        """
        Save the User model
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Delete the User model
        """
        db.session.delete(self)
        db.session.commit()
