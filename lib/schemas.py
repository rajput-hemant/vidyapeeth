from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.String()
    username = fields.Str(required=True)
    email = fields.Email(required=True)
