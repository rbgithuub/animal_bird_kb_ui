from pymongo import MongoClient

mongo_client = None
mongo_db = None


def init_mongo(app):
    global mongo_client, mongo_db

    mongo_client = MongoClient(app.config["MONGO_URI"])
    mongo_db = mongo_client[app.config["MONGO_DB_NAME"]]
    app.config["MONGO_DB"] = mongo_db

    return mongo_db
