from pymongo import MongoClient
import datetime


client = MongoClient("mongodb://guest:Z8zDntK3aC0l@54.251.133.139:27017/?authSource=logs_db")
db = client["logs_db"]
col = db["logs"]

# manually process the data using python.
def process_query(custom_minutes):
    print(f'custom minutes: {custom_minutes}')

    if isinstance(custom_minutes, str):
        return False

    # set dict 
    final_data = {}

    # query to get all data
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
        { "$sort" : { "_id.interval" : 1 } }
    ])

    # to make list iterable
    columns = list(data)

    resultset = {}
    # set first nest for intervals
    for d in columns:
        timestamp = datetime.datetime.utcfromtimestamp(int(d['_id']['interval'])/1000)
        converted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M')
        resultset[converted_timestamp] = {}
        
    # set second nest for values per intervals
    for d in columns:
        timestamp = datetime.datetime.utcfromtimestamp(int(d['_id']['interval'])/1000)
        converted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M')
        if converted_timestamp in resultset:
            if d['status'] == 'success':
                resultset[converted_timestamp]['success'] = d['count']
            if d['status'] == 'error':
                resultset[converted_timestamp]['error'] = d['count']

    return resultset
