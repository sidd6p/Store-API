import uuid
from flask.views import MethodView
from flask_smorest import abort, Blueprint

from db import stores, items
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("items", __name__, description="Item End-Point")

@blp.route("/item")
class ItemList(MethodView):

    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()
    
    @blp.arguments(ItemSchema)
    @blp.response(200, ItemSchema)
    def post(self, item_data):
        for id in items:
            if items[id]["name"] == item_data["name"] and items[id]["store_id"] == item_data["store_id"]:
                abort(404, message="Item already exixts")
            if item_data["store_id"] not in stores:
                abort(404, "Store does not exixts")
        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
        return item        
    
@blp.route("/item/<string:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            return abort(404, message="store not found") 

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        if item_id not in items:
            abort(404, message="Item not found")
        items[item_id].update(item_data)
        return items[item_id]  
    
    @blp.response(200, ItemSchema)
    def delete(self, item_id):
        if item_id not in items:
            abort(404, "Item not found")
        item_data = items[item_id]
        del items[item_id]
        return item_data
          
