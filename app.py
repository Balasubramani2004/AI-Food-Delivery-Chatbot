"""
app.py — Flask Web Server with Session-Based Cart & Order Management
"""
import os, uuid
from flask import Flask, render_template, request, jsonify, session
import chatbot

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"))
app.secret_key = "foodiebot_secret_key_2024_xK9mP"

# Initialize ML-enhanced chatbot on app startup
chatbot.init()

def get_state():
    if "state" not in session:
        session["state"] = {
            "cart": [],
            "order_placed": False,
            "order_id": None,
            "order_status": None,
            "order_items": [],
            "order_total": 0,
            "payment_method": "",
        }
    return session["state"]

def save_state(state):
    session["state"] = state
    session.modified = True

# ─── Pages ─────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

# ─── Chat ──────────────────────────────────────────────────────────────────────
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()
    if not message:
        return jsonify({"error": "Empty message"}), 400
    state = get_state()
    response = chatbot.process_message(message, state)
    save_state(state)
    return jsonify(response)

# ─── Cart ──────────────────────────────────────────────────────────────────────
@app.route("/cart/add", methods=["POST"])
def cart_add():
    data = request.get_json(silent=True) or {}
    item = data.get("item")
    if not item:
        return jsonify({"error": "No item"}), 400
    state = get_state()
    # Check if already in cart — increase qty or add
    for c in state["cart"]:
        if c["name"] == item["name"]:
            c["qty"] = c.get("qty", 1) + 1
            save_state(state)
            total = sum(i["price"] * i.get("qty", 1) for i in state["cart"])
            return jsonify({"success": True, "message": f"Added another {item['emoji']} {item['name']}!",
                            "cart_count": sum(i.get("qty",1) for i in state["cart"]), "cart_total": total})
    item["qty"] = 1
    state["cart"].append(item)
    save_state(state)
    total = sum(i["price"] * i.get("qty", 1) for i in state["cart"])
    return jsonify({"success": True, "message": f"✅ {item['emoji']} {item['name']} added to cart!",
                    "cart_count": sum(i.get("qty",1) for i in state["cart"]), "cart_total": total})

@app.route("/cart/remove", methods=["POST"])
def cart_remove():
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    state = get_state()
    state["cart"] = [i for i in state["cart"] if i["name"] != name]
    save_state(state)
    total = sum(i["price"] * i.get("qty", 1) for i in state["cart"])
    return jsonify({"success": True, "cart_count": sum(i.get("qty",1) for i in state["cart"]), "cart_total": total})

@app.route("/cart/clear", methods=["POST"])
def cart_clear():
    state = get_state()
    state["cart"] = []
    save_state(state)
    return jsonify({"success": True})

@app.route("/cart/view", methods=["GET"])
def cart_view():
    state = get_state()
    cart = state.get("cart", [])
    total = sum(i["price"] * i.get("qty", 1) for i in cart)
    count = sum(i.get("qty", 1) for i in cart)
    return jsonify({"cart": cart, "total": total, "count": count})

# ─── Order ─────────────────────────────────────────────────────────────────────
@app.route("/order/place", methods=["POST"])
def order_place():
    data = request.get_json(silent=True) or {}
    payment = data.get("payment_method", "Cash on Delivery")
    state = get_state()
    cart = state.get("cart", [])
    if not cart:
        return jsonify({"error": "Cart is empty"}), 400
    order_id = "FB" + str(uuid.uuid4())[:6].upper()
    total = sum(i["price"] * i.get("qty", 1) for i in cart)
    state.update({
        "order_placed": True,
        "order_id": order_id,
        "order_status": "confirmed",
        "order_items": cart.copy(),
        "order_total": total,
        "payment_method": payment,
        "cart": [],
    })
    save_state(state)
    return jsonify({"success": True, "order_id": order_id, "total": total,
                    "payment_method": payment, "estimated_time": "30-45 mins"})

@app.route("/order/status", methods=["GET"])
def order_status():
    state = get_state()
    if not state.get("order_placed"):
        return jsonify({"error": "No active order"}), 404
    return jsonify({
        "order_id":      state.get("order_id"),
        "status":        state.get("order_status"),
        "items":         state.get("order_items", []),
        "total":         state.get("order_total", 0),
        "payment_method":state.get("payment_method", ""),
    })

@app.route("/order/cancel", methods=["POST"])
def order_cancel():
    state = get_state()
    if not state.get("order_placed"):
        return jsonify({"error": "No active order"}), 404
    cancelled_items = state.get("order_items", [])
    cancelled_total = state.get("order_total", 0)
    oid = state.get("order_id")
    state.update({
        "order_status": "cancelled",
        "order_placed": False,
        "order_items": [],
        "order_total": 0,
        "order_id": None,
    })
    save_state(state)
    return jsonify({"success": True, "order_id": oid,
                    "cancelled_items": cancelled_items, "refund_amount": cancelled_total})

@app.route("/menu", methods=["GET"])
def get_menu():
    return jsonify(chatbot.MENU)

if __name__ == "__main__":
    print("\n🍕 FoodieBot running → http://localhost:5000\n")
    app.run(debug=True, port=5000, use_reloader=False)
