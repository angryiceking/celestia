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
                    { "$subtract": [ "$created_at", datetime.datetime(1970, 1, 1) ] },
                    { "$mod": [
                        { "$subtract": [ "$created_at", datetime.datetime(1970, 1, 1) ] },
                        1000 * 60 * custom_minutes
                    ]}
                ],
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
    timestamp = datetime.datetime.utcfromtimestamp(int(d['_id']['interval'])/1000)
    converted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    mylist[converted_timestamp] = {}

print(mylist)
for d in columns:
    timestamp = datetime.datetime.utcfromtimestamp(int(d['_id']['interval'])/1000)
    converted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    if converted_timestamp in mylist:
        if d['status'] == 'success':
            mylist[converted_timestamp]['success'] = d['count']
        if d['status'] == 'error':
            mylist[converted_timestamp]['error'] = d['count']

print(mylist)