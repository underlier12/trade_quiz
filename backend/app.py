from crypt import methods
from flask import Flask, request
from flask_cors import CORS
from datetime import datetime
from elasticsearch import Elasticsearch

import time
import pytesseract
import cv2
import os

app = Flask(__name__)
CORS(app)

es = Elasticsearch(
    hosts=['http://elastic-container:9200']
)

# Test
@app.route("/")
def hello():
    return {"data": time.time()}

# Full text query
def _common_search(text, index):
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
        output = hits[:5]
    if not hits:
        output = 'No results'

    response = {
        "output": output,
        "original": text
    }
    return response

@app.route("/query/<subject>/<lang>", methods=['POST'])
def search_document(subject, lang):
    TEMP_TITLE = 'temp_img.jpg'
    file_obj = request.files.get('File')
    file_obj.save(TEMP_TITLE)

    image = cv2.imread(TEMP_TITLE)
    text = pytesseract.image_to_string(image, lang=lang)
    response = _common_search(text, subject)
    os.remove(TEMP_TITLE)
    return response

@app.route("/registration/<subject>", methods=['POST'])
def insert_document(subject):
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
        index=subject,
        body=doc
    )
    return res
