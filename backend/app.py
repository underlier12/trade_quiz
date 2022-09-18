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
def common_search(text):
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
    hits = res['hits']['hits']
    if hits:
        output = hits[0]
    if not hits:
        output = 'No results'
    # print(output)
    response = {
        "output": output,
        "original": text
    }
    return response

@app.route("/query/trade-english/eng", methods=['POST'])
def search_document_eng():
    TEMP_TITLE = 'temp_eng.jpg'
    file_obj = request.files.get('File')
    file_obj.save(TEMP_TITLE)

    image = cv2.imread(TEMP_TITLE)
    text = pytesseract.image_to_string(image)

    response = common_search(text)
    os.remove(TEMP_TITLE)
    return response

@app.route("/query/trade-english/kor", methods=['POST'])
def search_document_kor():
    TEMP_TITLE = 'temp_kor.jpg'
    file_obj = request.files.get('File')
    file_obj.save(TEMP_TITLE)

    image = cv2.imread(TEMP_TITLE)
    text = pytesseract.image_to_string(image, lang='kor+eng')
    print(text)

    response = common_search(text)
    os.remove(TEMP_TITLE)
    return response

# Registration
@app.route("/registration/trade-english", methods=['POST'])
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

    res = es.index(
        index=TRADE_ENGLISH,
        body=doc
    )
    return res