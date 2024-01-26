from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.String()
    username = fields.Str(required=True)
    email = fields.Email(required=True)


class BookSchema(Schema):
    id = fields.String()
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    isbn = fields.Integer(required=True)
    price = fields.Float(required=True)
    quantity = fields.Integer(required=True)
