from marshmallow import fields, Schema

class ItemSchema(Schema):
    id = fields.Str(dump_only=True) #because we will return the id, it will not come from the request itself
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Str(required=True)

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()

class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
