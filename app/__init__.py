from flask import Flask

app = Flask(__name__)
data = {}

from app import routes