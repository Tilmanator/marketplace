from app import app

from flask import request

import json
import os

@app.before_first_request
def load_sample_data():
    file = os.path.join(app.root_path, 'sample_data')
    with open(file, 'r') as f:
        app.data = json.loads(f.read())


@app.route('/')
@app.route('/products')
def index():
    some = request.args.get('onlysome')
    return json.dumps(app.data)


@app.route('/purchase/<id>')
def products(id):
    pass