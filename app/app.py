from flask import Flask, jsonify, request

app = Flask(__name__)

# Fake in-memory "menu" for the FoodExpress platform
MENU = [
    {"id": 1, "name": "Margherita Pizza", "price": 6.50},
    {"id": 2, "name": "Chicken Burger", "price": 4.75},
    {"id": 3, "name": "Pad Thai", "price": 5.25},
    {"id": 4, "name": "Iced Coffee", "price": 2.00},
]

ORDERS = []


@app.route("/", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "FoodExpress API",
        "message": "Deployed via Jenkins + Terraform + Docker pipeline"
    })


@app.route("/menu", methods=["GET"])
def get_menu():
    return jsonify(MENU)


@app.route("/order", methods=["POST"])
def place_order():
    data = request.get_json(force=True, silent=True) or {}
    item_id = data.get("item_id")

    item = next((m for m in MENU if m["id"] == item_id), None)
    if not item:
        return jsonify({"error": "item_id not found in menu"}), 400

    order = {"order_id": len(ORDERS) + 1, "item": item}
    ORDERS.append(order)
    return jsonify(order), 201


@app.route("/orders", methods=["GET"])
def list_orders():
    return jsonify(ORDERS)


if __name__ == "__main__":
    # Listens on all interfaces so it's reachable from outside the container
    app.run(host="0.0.0.0", port=5000)
