from flask import Flask, request
from flask_cors import CORS
from datetime import datetime
from elasticsearch import Elasticsearch

import time

app = Flask(__name__)
CORS(app)

es = Elasticsearch()

TRADE_ENGLISH = 'trade_english'

@app.route("/")
def hello():
    return {"data": time.time()}

@app.route("/trade-english", methods=['POST'])
def insert_document():
    # print(request.json)
    article = request.json['article']
    version = request.json['version']
    content = request.json['content']
    timestamp = datetime.now()
    doc = {
        'article': article,
        'version': version,
        'content': content,
        'timestamp': timestamp
    }
    # print(doc)

    res = es.index(
        index=TRADE_ENGLISH,
        body=doc
    )
    return res