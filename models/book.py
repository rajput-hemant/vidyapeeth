from lib.extensions import db
from lib.utils import generate_uuid


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.String(), primary_key=True, default=str(generate_uuid()))
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.Integer, nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Book %r>" % self.title

    def __init__(self, title: str, author: str, isbn: int, price: float, quantity: int):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.price = price
        self.quantity = quantity

    @classmethod
    def get_all_books(cls):
        return Book.query.all()

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    @classmethod
    def get_book_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_book_by_title(cls, title):
        return cls.query.filter_by(title=title).first()

    @classmethod
    def get_book_by_isbn(cls, isbn):
        return cls.query.filter_by(isbn=isbn).first()
