import uuid
from flask import Flask, request
from flask_smorest import abort
from db import stores, items


app = Flask(__name__)


################# STORE #################
@app.get("/store")
def get_stores():
    print(type(stores))
    return {"stores": list(stores.values())}

@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="store not found")

@app.post("/store")
def create_store():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(404, message="store name not found")
    for id in stores:
        if stores[id]["name"] == store_data["name"]:
            abort(404, "Store already exists")
    store_id = uuid.uuid4().hex
    new_store = {**store_data, "id":store_id}
    stores[store_id] = new_store
    return new_store, 201

@app.delete("/store")
def delete_store():
    store_data = request.get_json()
    if store_data["id"] not in stores:
        abort(404, "Store not found")
    store_data = stores[store_data["id"]]
    del stores[store_data["id"]]
    items_id = []
    for item_id in items:
        if items[item_id]["store_id"] == store_data["id"]:
            items_id.append(item_id)
    for item_id in items_id:
        del items[item_id]
    return {"store": store_data}


################# ITEM #################
@app.get("/item")
def get_items():
    return {"items":list(items.values())}

@app.post("/item")
def add_item():
    item_data = request.get_json()
    if "store_id" not in item_data or item_data["store_id"] not in stores:
        abort(404, message="store not found")
    if "price" not in item_data or "name" not in item_data:
        abort(404, message="item details not found")   
    for id in items:
        if items[id]["name"] == item_data["name"] and items[id]["store_id"] == item_data["store_id"]:
            abort(404, message="Item already exixts")
    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
    return item

@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        return abort(404, message="store not found")

@app.delete("/item/<string:id>")
def delete_item(id):
    if id not in items:
        abort(404, "Item not found")
    item_data = items[id]
    del items[id]
    return {"item": item_data}
       

if __name__ == '__main__':
    app.run(debug=True)