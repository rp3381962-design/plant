from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "plantshopsecret"

# ---------- FAKE DATABASE USING ARRAYS ----------
plants = [
    {"id": 1, "name": "Aloe Vera", "price": 150, "image": "https://via.placeholder.com/150"},
    {"id": 2, "name": "Snake Plant", "price": 200, "image": "https://via.placeholder.com/150"},
    {"id": 3, "name": "Tulsi", "price": 100, "image": "https://via.placeholder.com/150"}
]

orders = []  # store orders as dictionaries

# ---------- ROUTES ----------
@app.route("/")
def index():
    return render_template("index.html", plants=plants)

@app.route("/add_to_cart/<int:plant_id>")
def add_to_cart(plant_id):
    cart = session.get("cart", [])
    cart.append(plant_id)
    session["cart"] = cart
    return redirect(url_for("index"))

@app.route("/cart")
def cart():
    cart = session.get("cart", [])
    items = []
    total = 0
    for pid in cart:
        for p in plants:
            if p["id"] == pid:
                items.append(p)
                total += p["price"]
    return render_template("cart.html", items=items, total=total)

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        address = request.form["address"]
        cart = session.get("cart", [])

        # Save order in memory
        order = {
            "customer": name,
            "email": email,
            "address": address,
            "items": cart
        }
        orders.append(order)

        session["cart"] = []  # clear cart
        return "✅ Order placed successfully! (Not saved permanently, just in memory)"
    return render_template("checkout.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
