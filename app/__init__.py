from flask import Flask
from pymongo import MongoClient
import os

def create_app():
    app = Flask(__name__)

    # Load environment variables
    mongo_uri = os.getenv("MONGO_URI")
    mongo_db_name = os.getenv("MONGO_DB")

    # Initialize Mongo
    client = MongoClient(mongo_uri)
    db = client[mongo_db_name]

    # Store DB in app config
    app.config["MONGO_DB"] = db

    # Register blueprint
    from routes.animal_routes import animal_api
    app.register_blueprint(animal_api)

    return app
