import pymongo
import json


DB_URI = '127.0.0.1'
DB_PORT = 10086
database_client = pymongo.MongoClient(DB_URI, DB_PORT)

# 连接到database和collection，如果给定的不存在，则创建新的
MONGO_DB_NAME = 'shopify_shop_collections'
TABLE_NAME = 'collection_title'
database = database_client[MONGO_DB_NAME]
collection = database[TABLE_NAME]

resultdocs = collection.find({}, {'_id': 0, 'domain': 1, 'ct': 1})
data = [{'%s' % (item['domain']): item['ct']} for item in resultdocs]

with open('shop-data.json', 'w', encoding='utf-8') as fp:
    fp.write(json.dumps(data, ensure_ascii=False))
