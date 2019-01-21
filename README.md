# Marketplace

A simple marketplace implementation including shopping carts and products.

## Installation

Ensure you have Python installed on your machine.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install project requirements by executing the following command in the root directory of this repo.

```bash
pip install -r requirements.txt
```
If you have any issues, try updating both Python and pip to a more recent version.

## Usage
To start the local server, navigate to the root directory of this repo and execute:
```bash
flask run
```
You can now navigate [here](localhost:5000/products) to view all available sample products.

## URL guide
*Prepend localhost:5000 to the following links if you made no changes*

#### /products?availableOnly=false
- Returns all products unless the availableOnly flag is set to 'true'

#### /products/<product_id>
- Returns the specified product

#### /cart/create
- Creates a shopping cart, returning your unique cart ID

#### /cart/<cart_id>
- Returns specified cart

#### /cart/<cart_id>/add/<product_id>
- Adds 1 product to cart

#### /cart/<cart_id>/remove/<product_id>
- Removes product from cart

#### /cart/<cart_id>/complete
- Checkout! All the items in the cart are purchased (if possible)
