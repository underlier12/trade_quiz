from elasticsearch import Elasticsearch

import json

es = Elasticsearch()

TRADE_ENGLISH_MAPPING_PATH = 'elastic_se/trade_english_mapping.json'
with open(TRADE_ENGLISH_MAPPING_PATH) as f:
    mapping = json.load(f)

INDEX = 'trade_english'
es.indices.create(
    index=INDEX,
    ignore=400,
    body=mapping
)