from flask import Flask, request

app = Flask(__name__)

stores = [{"name": "mystore", "items": [{"name": "carom", "price": 15.99}]}]


@app.get("/stores")
def get_stores():
    return {"stores": stores}


@app.post("/store")
def create_store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": request_data['items']}
    stores.append(new_store)
    return new_store, 201


@app.post('/stores/<name>/item')
def create_item(name):
    request_data = request.get_json()

    for store in stores:
        if store['name'] == name:
            new_item = {"name" : request_data["name"], "price" : request_data["price"]}
            store["items"].append(new_item)
            return new_item, 201
    return {"message" : "store doesnot found"}, 404


@app.get("/stores/<name>")
def get_store_detail(name):
    for store in stores:
        if store['name'] == name:
            return store
    return None

@app.get("/stores/<name>/item")
def get_item_in_store(name):
    for store in stores:
        if store['name'] == name:
            return {"items" : store['items']}
    return {"message" : "store doesnot found"}, 404

app.run(debug=True)