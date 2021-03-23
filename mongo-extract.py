from pymongo import MongoClient
import datetime

client = MongoClient("mongodb://guest:Z8zDntK3aC0l@54.251.133.139:27017/?authSource=logs_db")
db = client["logs_db"]
col = db["logs"]
custom_minutes = 5

def transform_date(date):
    try:
        ndate = datetime.datetime.strftime(date, '%Y-%m-%d %X')
    except ValueError:
        ndate = datetime.datetime.strftime(date, '%Y-%m-%d %X')

    return ndate

data = col.aggregate([
    { "$group": {
        "_id": {
            "interval": {
                "$subtract": [ 
                  { "$minute": "$created_at" },
                  { "$mod": [{ "$minute": "$created_at"}, custom_minutes] }
                ]
              },
            "status": "$status",
        },
        "status": { "$addToSet": "$status"},
        "count": { "$sum": 1}
    }},
    {
        "$unwind": "$status"
    },
    { "$sort" : { "_id.interval" : -1 } }
])

columns = list(data)

# print(columns)
mylist = {}
for d in columns:
    mylist[d['_id']['interval']] = {}

print(mylist)
for d in columns:
    if d['_id']['interval'] in mylist:
        if d['status'] == 'success':
            mylist[d['_id']['interval']]['success'] = d['count']
        if d['status'] == 'error':
            mylist[d['_id']['interval']]['error'] = d['count']

print(mylist)