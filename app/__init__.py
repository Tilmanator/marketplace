from flask import Flask

app = Flask(__name__)
products = {}
carts = {}
next_id = []

from app import routes
