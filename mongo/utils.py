from pymongo import MongoClient

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
        { "$sort" : { "_id.interval" : 1 } }
    ])

    # to make list iterable
    columns = list(data)

    resultset = {}
    # set first nest for intervals
    for d in columns:
        resultset[d['_id']['interval']] = {}
        
    # set second nest for values per intervals
    for d in columns:
        if d['_id']['interval'] in resultset:
            if d['status'] == 'success':
                resultset[d['_id']['interval']]['success'] = d['count']
            elif d['status'] == 'error':
                resultset[d['_id']['interval']]['error'] = d['count']

    return resultset
