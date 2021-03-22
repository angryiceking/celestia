from pymongo import MongoClient

client = MongoClient("mongodb://guest:Z8zDntK3aC0l@54.251.133.139:27017/?authSource=logs_db")
db = client["logs_db"]
col = db["logs"]

final_data = {
    "1:05": {
        "success": 0,
        "error": 0
    },
    "1:10": {
        "success": 0,
        "error": 0
    },
    "1:15": {
        "success": 0,
        "error": 0
    }
}

# manually process the data using python.
def manual_process():
    # query to get all data
    data = col.find({})
    # get start_date for initial checking.
    start_date = data[0]['created_at']

    for d in data:
        check_interval = d['created_at'] - start_date
        interval = (check_interval.seconds // 60) % 60
        if interval <= 5:
            if d['status'] == 'success':
                final_data["1:05"]["success"] += 1
            elif d['status'] == 'error':
                final_data["1:05"]["error"] += 1
        elif interval >= 5 and interval <=10:
            if d['status'] == 'success':
                final_data["1:10"]["success"] += 1
            elif d['status'] == 'error':
                final_data["1:10"]["error"] += 1
        elif interval >= 10 and interval <= 15:
            if d['status'] == 'success':
                final_data["1:15"]["success"] += 1
            elif d['status'] == 'error':
                final_data["1:15"]["error"] += 1

    return final_data