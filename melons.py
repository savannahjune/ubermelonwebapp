from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import model
import jinja2
import os

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def index():
    """This is the 'cover' page of the ubermelon site"""
    return render_template("index.html")

@app.route("/melons")
def list_melons():
    """This is the big page showing all the melons ubermelon has to offer"""
    melons = model.get_melons()
    return render_template("all_melons.html",
                           melon_list = melons)

@app.route("/melon/<int:id>")
def show_melon(id):
    """This page shows the details of a given melon, as well as giving an
    option to buy the melon."""
    melon = model.get_melon_by_id(id)
    print melon
    return render_template("melon_details.html",
                  display_melon = melon)

@app.route("/cart")
def shopping_cart():
    """TODO: Display the contents of the shopping cart. The shopping cart is a
    list held in the session that contains all the melons to be added. Check
    accompanying screenshots for details."""


    melon_dict = {}
    total = 0
    
    for key in session['cart']:

        melon = model.get_melon_by_id(key)
        melon_dict[key] = {"name": melon.common_name, "quantity": session['cart'][key], "price": melon.price }
        total += melon_dict[key]["price"] * melon_dict[key]["quantity"]

    return render_template("cart.html", melon_dict=melon_dict, cart_total="%0.2f" % total) 

@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """TODO: Finish shopping cart functionality using session variables to hold
    cart list.

    Intended behavior: when a melon is added to a cart, redirect them to the
    shopping cart page, while displaying the message
    "Successfully added to cart" """

    temp_id=str(id)

    if 'cart' in session:

        # if temp_id in session['cart']:
        #     session['cart'][temp_id] += 1

        # else:
        #     session['cart'][temp_id] = 1
        session['cart'][temp_id] = session['cart'].get(temp_id, 0) + 1

    else:
        print "initializing cart in session"
        session['cart'] = {temp_id: 1}
    
    display_melon = model.get_melon_by_id(id)

    flash("You successfully added one " + display_melon.common_name +" to your cart!")
    return redirect('/cart')
"""We did not do anything to deal with case in which user checks cart before adding item"""    

@app.route("/login", methods=["GET"])
def show_login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """TODO: Receive the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session."""
    email = request.form.get("email")
    password = request.form.get("password")

    # verify_user = model.get_customer_by_email(email)

    # make session user dictionary

    if 'email' in session:
        flash("You are successfully logged in!")
    else:
        flash("Please sign up for an ubermelon account ya scrub")


@app.route("/checkout")
def checkout():
    """TODO: Implement a payment system. For now, just return them to the main
    melon listing page."""
    flash("Sorry! Checkout will be implemented in a future version of ubermelon.")
    return redirect("/melons")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
