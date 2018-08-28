import pymongo
from pymongo import MongoClient
import datetime
from celery import Celery


app = Celery('tasks', broker='amqp://admin:Krishna1986@159.65.152.34:5672//')

client = MongoClient('mongodb://root:Krishna1986@159.65.152.34:27017/admin')
db = client.TechCrunch

pipeline = [ {"$match": {'state': 'CA'}}, {"$out": "techcrunch_dest"},]
db.techcrunch.aggregate(pipeline)

source = db["techcrunch"].find({'state': 'CA'}).sort("_id", 1)

destination = db["techcrunch_dest"]
destination.delete_many({})

@app.task
def Copy():
    for doc in source:
        result = destination.insert_one(doc)
		# destination.update_one({'_id':result.inserted_id},{'$set':{"date":datetime.datetime.utcnow()}})
    print("Copy done")

from Tasks import *
Copy.delay()