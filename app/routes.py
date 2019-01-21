from app import app

from flask import request

import json
import os


@app.before_first_request
def load_sample_data():
    """ Load sample data """
    file = os.path.join(app.root_path, 'sample_data')
    with open(file, 'r') as f:
        app.products = json.loads(f.read())
    app.next_id = [1]
    app.carts = {}


@app.route('/products', defaults={'product_id': None})
@app.route('/products/<int:product_id>')
def show_products(product_id):
    """
    If given a product id, try to find and show it
    Otherwise, show all products unless availableOnly is 'true' or '1'
    """
    available_only = request.args.get('availableOnly', default='false')

    if product_id:
        if product_id in map(lambda x: x["id"], app.products):
            for product in app.products:
                if product["id"] == int(product_id):
                    return json.dumps(product) + (" (ignoring availableOnly parameter)"
                                                  if available_only and available_only != 'false' else '')
        else:
            return "No product with id '{}' exists".format(product_id)
    else:
        if available_only == 'true':
            return json.dumps(list(filter(lambda x: x["inventory_count"] > 0, app.products)))
        elif available_only != 'false':
            return "Invalid 'availableOnly' parameter. Must be 'true', 'false' or omitted"
        else:
            return json.dumps(app.products)


@app.route('/cart/<int:cart_id>')
def get_cart(cart_id):
    """ Show the requested cart and it's contents if possible """
    if cart_id not in app.carts:
        return "Invalid cart ID"
    response = json.dumps(app.carts[cart_id])

    response += ' Total Value: $%.2f' % calculate_sum(app.carts[cart_id])
    return response


@app.route('/cart/create')
def create_cart():
    """ Create a cart with a unique identifier"""
    unique_id = app.next_id.pop(0)
    if len(app.next_id) == 0:
        app.next_id.append(unique_id + 1)
    app.carts[unique_id] = {}
    return '{}'.format(unique_id)


@app.route('/cart/<int:cart_id>/add/<int:product_id>')
def add_to_cart(cart_id, product_id):
    """ Add the product to the cart if possible"""
    if cart_id not in app.carts:
        return "Invalid cart ID"
    if product_id not in map(lambda x: x["id"], app.products):
        return "Invalid product ID"
    if product_id not in app.carts[cart_id]:
        app.carts[cart_id][product_id] = 1
    else:
        app.carts[cart_id][product_id] += 1
    return "Successfully added one item"


@app.route('/cart/<int:cart_id>/remove/<int:product_id>')
def remove_from_cart(cart_id, product_id):
    """ Remove the product from the cart if possible"""
    if cart_id not in app.carts:
        return "Invalid cart ID"
    if product_id not in map(lambda x: x["id"], app.products):
        return "Invalid product ID"
    if product_id not in app.carts[cart_id]:
        return "Product {} not in selected cart".format(product_id)
    elif app.carts[cart_id][product_id] == 1:
        app.carts[cart_id].pop(product_id, None)
    else:
        app.carts[cart_id][product_id] -= 1
    return "Successfully removed one item"


@app.route('/cart/<int:cart_id>/complete')
def complete_cart(cart_id):
    """ Complete the cart if possible"""
    if cart_id not in app.carts:
        return "Invalid cart ID"

    for product_id in app.carts[cart_id]:
        if get_availability(product_id) < app.carts[cart_id][product_id]:
            return "Error, we have sold out of that item! Please remove it from your cart"

    for product_id in app.carts[cart_id]:
        decrement(product_id, app.carts[cart_id][product_id])

    app.carts.pop(cart_id, None)
    app.next_id.insert(0, cart_id)
    return "Successfully completed checkout"


def get_availability(product_id):
    if product_id not in map(lambda x: x["id"], app.products):
        return 0

    for i in app.products:
        if i["id"] == product_id:
            return i["inventory_count"]


def decrement(product_id, num=1):
    """Decrement product_id, assumes correct behaviour"""
    if product_id not in map(lambda x: x["id"], app.products):
        return

    for i in app.products:
        if i["id"] == product_id:
            i["inventory_count"] -= num


def calculate_sum(cart):
    sum = 0
    for k in cart:
        price = 0
        for i in app.products:
            if i['id'] == k:
                price = i["price"]

        sum += price * cart[k]
    return sum

# This is deprecated because we updated to carts

# @app.route('/purchase/<int:product_id>')
# def products(product_id):
#     """ Check whether a product can be purchased and if so, purchase it"""
#     for product in app.products:
#         if product["id"] == product_id:
#             if product["inventory_count"] > 0:
#                 product["inventory_count"] -= 1
#                 return "Successful purchase"
#             else:
#                 return "Out of stock, try again later."
#
#     return "No product with id '{}' available".format(product_id)
