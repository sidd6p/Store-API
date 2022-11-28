import uuid
from flask.views import MethodView
from flask_smorest  import abort, Blueprint

from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Store End-Points")

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return stores.values()

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def post(self, store_data):
        for id in stores:
            if stores[id]["name"] == store_data["name"]:
                abort(404, "Store already exists")
        store_id = uuid.uuid4().hex
        new_store = {**store_data, "id":store_id}
        stores[store_id] = new_store
        return new_store


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message="store not found")
    
    @blp.response(200, StoreSchema)
    def delete(self, store_id):
        store_data = stores[store_id]
        del stores[store_id]
        items_id = []
        for item_id in items:
            if items[item_id]["store_id"] == store_id:
                items_id.append(item_id)
        for item_id in items_id:
            del items[item_id]
        return store_data