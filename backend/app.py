from flask import Flask, jsonify
from flask_cors import CORS
import time


app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return {"data": time.time()}