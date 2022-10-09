from elasticsearch import Elasticsearch

import json

es = Elasticsearch()

COMMON_MAPPING_PATH = 'elastic_se/trade_english_mapping.json'
with open(COMMON_MAPPING_PATH) as f:
    mapping = json.load(f)

INDEX_LIST = [
    'trade-english', 
    'international-payment', 
    'fta', 
    'digital-trading'
]

for index in INDEX_LIST:
    es.indices.create(
    index=index,
    ignore=400,
    body=mapping
)
