from flask import Flask, request
from flask_cors import CORS
from datetime import datetime
from elasticsearch import Elasticsearch
from PIL import Image

import time
import pytesseract
import cv2
import os

app = Flask(__name__)
CORS(app)

es = Elasticsearch()

TRADE_ENGLISH = 'trade_english'

# Test
@app.route("/")
def hello():
    return {"data": time.time()}

# Full text query
@app.route("/query/trade-english", methods=['POST'])
def search_document():
    TEMP_TITLE = 'temp.jpg'
    file_obj = request.files.get('File')
    file_obj.save(TEMP_TITLE)

    image = cv2.imread(TEMP_TITLE)
    text = pytesseract.image_to_string(image)
    # text = pytesseract.image_to_string(image, lang='kor+eng')
    # print(text)

    query = {
        "query": {
            "match": {
                "content": text
            }
        }
    }

    res = es.search(
        index=TRADE_ENGLISH,
        body=query
    )

    os.remove(TEMP_TITLE)

    hits = res['hits']['hits']
    if hits:
        output = hits[0]
    if not hits:
        output = 'No results'
    print(output)
    response = {
        "output": output,
        "original": text
    }
    return response

# Registration
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