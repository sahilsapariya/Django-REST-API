from flask import Flask, request
from flask_cors import CORS
from db import stores, items
from flask_smorest import abort
import uuid

app = Flask(__name__)
CORS(app)

@app.get("/stores")
def get_stores():
    return {"stores": list(stores.values())}


@app.post("/store")
def create_store():
    store_data = request.get_json()
    if (
        "price" not in store_data
    ):
        abort(
            400,
            message="Bad Request. Ensure 'name' is included in JSON playload"
        )
    for store in stores.values():
        if store["name"] == store['name']:
            abort(404, message=f"{store['name']} already exists.")
    store_id = uuid.uuid4().hex
    store = {**store_data, "id": store_id}
    stores[store_id] = store
    return store, 201


@app.post('/item')
def create_item():
    item_data = request.get_json()
    """Here not only we need to validate data exits,
    But also what types of data. Price should be a float,
    for example."""
    if (
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(
            400,
            message="Bad Request. Ensure 'price', 'store_id', and 'name' are included in JSON playload"
        )
    for item in items.values():
        if (
            item_data["name"] == item['name']
            and item_data["store_id"] == item["store_id"]
        ):
            abort(404, message=f"{item} already exists.")
    if item_data['store_id'] not in stores:
        abort(404, message="Store not found")


    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item

    return item, 201


@app.get("/stores/<store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message="Store not found")

@app.get("/item/<item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message="Store not found")
        
@app.get("/items")
def get_items():
    try:
        return items
    
    except KeyError:
        abort(404, message="items not found")


@app.delete("/item/<item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted."}
    except KeyError:
        abort(404, message="Store not found")

@app.put("/item/<item_id>")
def update_item(item_id):
    item_data = request.get_json()
    if "price" not in item_data or "name" not in item_data:
        abort(404, message="Bad request. Ensure 'price', and 'name' are included in JSON playload.")

    try:
        item = items[item_id]
        item |= item_data

        return item 
    except KeyError:
        abort(404, message="Item not found.")

app.run(debug=True)