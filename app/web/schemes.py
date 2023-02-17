from marshmallow import fields, Schema


class OkResponseSchema(Schema):
    status = fields.Str()
    data = fields.Dict()
