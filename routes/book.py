from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from lib.schemas import BookSchema
from models.book import Book

book = Blueprint("book", __name__)


@book.get("/all")
def get_all_books():
    """
    Get all books
    """

    books = Book.get_all_books()
    books = BookSchema().dump(books, many=True)

    return (
        jsonify(
            {
                "status": "success",
                "message": "books retrieved successfully",
                "data": books,
            }
        ),
        200,
    )  # OK


@book.post("/create")
@jwt_required()
def create_book():
    """
    Create a new book
    """

    data: dict[str, str] = request.get_json()

    title = data["title"]
    author = data["author"]
    isbn = data["isbn"]
    price = data["price"]
    quantity = data["quantity"]

    print(title, author, isbn, price, quantity)

    # TODO: validate data

    book = Book(title, author, int(isbn), float(price), int(quantity)).create()
    book = BookSchema().dump(book)

    return (
        jsonify(
            {
                "status": "success",
                "message": "book created successfully",
                "data": book,
            }
        ),
        201,
    )  # Created


@book.put("/update/<id>")
@jwt_required()
def update_book(id):
    """
    Update a book
    """

    data: dict[str, str] = request.get_json()

    title = data["title"]
    author = data["author"]
    isbn = data["isbn"]
    price = data["price"]
    quantity = data["quantity"]

    book = Book.get_book_by_id(id)

    if book is None:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "book not found",
                }
            ),
            404,
        )  # Not Found

    book.title = title
    book.author = author
    book.isbn = isbn
    book.price = price
    book.quantity = quantity

    book.update()

    book = BookSchema().dump(book)

    return (
        jsonify(
            {
                "status": "success",
                "message": "book updated successfully",
                "data": book,
            }
        ),
        200,
    )  # OK


@book.delete("/delete/<id>")
def delete_book(id):
    """
    Delete a book
    """

    book = Book.get_book_by_id(id)

    if book is None:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "book not found",
                }
            ),
            404,
        )

    book.delete()

    return (
        jsonify(
            {
                "status": "success",
                "message": "book deleted successfully",
            }
        ),
        200,
    )


# @book.get("/<id>")
# def get_book_by_id(id):
#     """
#     Get a book by id
#     """

#     book = Book.get_book_by_id(id)

#     if book is None:
#         return (
#             jsonify(
#                 {
#                     "status": "error",
#                     "message": "book not found",
#                 }
#             ),
#             404,
#         )

#     book = BookSchema().dump(book)

#     return (
#         jsonify(
#             {
#                 "status": "success",
#                 "message": "book retrieved successfully",
#                 "data": book,
#             }
#         ),
#         200,
#     )


@book.get("/<isbn>")
def get_book_by_isbn(isbn):
    """
    Get a book by isbn
    """

    book = Book.get_book_by_isbn(isbn)

    if book is None:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "book not found",
                }
            ),
            404,
        )

    book = BookSchema().dump(book)

    return (
        jsonify(
            {
                "status": "success",
                "message": "book retrieved successfully",
                "data": book,
            }
        ),
        200,
    )
