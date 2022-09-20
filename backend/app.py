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
INTERNATIONAL_PAYMENT = 'international_payment'

# Test
@app.route("/")
def hello():
    return {"data": time.time()}

# Full text query
def common_search(text, index):
    query = {
        "query": {
            "match": {
                "content": text
            }
        }
    }
    res = es.search(
        index=index,
        body=query
    )
    hits = res['hits']['hits']
    if hits:
        output = hits[0]
    if not hits:
        output = 'No results'

    response = {
        "output": output,
        "original": text
    }
    return response

@app.route("/query/trade-english/eng", methods=['POST'])
def search_document_trade_english_eng():
    TEMP_TITLE = 'trade_english_eng.jpg'
    file_obj = request.files.get('File')
    file_obj.save(TEMP_TITLE)

    image = cv2.imread(TEMP_TITLE)
    text = pytesseract.image_to_string(image)

    response = common_search(text, TRADE_ENGLISH)
    os.remove(TEMP_TITLE)
    return response

@app.route("/query/trade-english/kor", methods=['POST'])
def search_document_trade_english_kor():
    TEMP_TITLE = 'trade_english_kor.jpg'
    file_obj = request.files.get('File')
    file_obj.save(TEMP_TITLE)

    image = cv2.imread(TEMP_TITLE)
    text = pytesseract.image_to_string(image, lang='kor')

    response = common_search(text, TRADE_ENGLISH)
    os.remove(TEMP_TITLE)
    return response

@app.route("/query/international-payment/eng", methods=['POST'])
def search_document_international_payment_eng_eng():
    TEMP_TITLE = 'international_payment_eng.jpg'
    file_obj = request.files.get('File')
    file_obj.save(TEMP_TITLE)

    image = cv2.imread(TEMP_TITLE)
    text = pytesseract.image_to_string(image)

    response = common_search(text, INTERNATIONAL_PAYMENT)
    os.remove(TEMP_TITLE)
    return response

@app.route("/query/international-payment/kor", methods=['POST'])
def search_document_international_payment_eng_kor():
    TEMP_TITLE = 'international_payment_kor.jpg'
    file_obj = request.files.get('File')
    file_obj.save(TEMP_TITLE)

    image = cv2.imread(TEMP_TITLE)
    text = pytesseract.image_to_string(image, lang='kor')

    response = common_search(text, INTERNATIONAL_PAYMENT)
    os.remove(TEMP_TITLE)
    return response

# Registration
@app.route("/registration/trade-english", methods=['POST'])
def insert_document_trade_english():
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

@app.route("/registration/international-payment", methods=['POST'])
def insert_document_international_payment():
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
        index=INTERNATIONAL_PAYMENT,
        body=doc
    )
    return res