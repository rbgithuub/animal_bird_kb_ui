from bson import ObjectId
from bson.errors import InvalidId
from flasgger import swag_from
from flask import Blueprint, current_app, jsonify, render_template, request

from models.animals import animal_serializer

animal_api = Blueprint("animal_api", __name__)


@animal_api.get("/")
def home():
    return render_template("index.html")


@animal_api.get("/animals")
@swag_from(
    {
        "tags": ["Animals"],
        "responses": {
            200: {
                "description": "List all animals",
                "schema": {"type": "array", "items": {"type": "object"}},
            }
        },
    }
)
def get_animals():
    collection = current_app.config["MONGO_DB"]["animals"]
    animals = list(collection.find())

    for animal in animals:
        animal["_id"] = str(animal["_id"])

    return jsonify([animal_serializer(animal) for animal in animals]), 200


@animal_api.post("/animals")
@swag_from(
    {
        "tags": ["Animals"],
        "consumes": ["application/json"],
        "parameters": [
            {
                "name": "body",
                "in": "body",
                "required": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "category": {"type": "string"},
                        "origin": {"type": "string"},
                        "sleep_pattern": {"type": "string"},
                        "food_habits": {"type": "string"},
                        "fun_facts": {"type": "object"},
                    },
                    "required": [
                        "name",
                        "category",
                        "origin",
                        "sleep_pattern",
                        "food_habits",
                        "fun_facts",
                    ],
                },
            }
        ],
        "responses": {
            201: {"description": "Animal inserted"},
            400: {"description": "Invalid payload"},
        },
    }
)
def add_animal():
    collection = current_app.config["MONGO_DB"]["animals"]
    payload = request.get_json(silent=True)

    if not payload:
        return jsonify({"error": "Invalid or missing JSON"}), 400

    result = collection.insert_one(payload)
    return jsonify({"inserted_id": str(result.inserted_id)}), 201


@animal_api.get("/animals/<string:animal_id>")
def get_animal(animal_id):
    collection = current_app.config["MONGO_DB"]["animals"]

    try:
        obj_id = ObjectId(animal_id)
    except InvalidId:
        return jsonify({"error": "Invalid animal ID"}), 400

    animal = collection.find_one({"_id": obj_id})
    if not animal:
        return jsonify({"error": "Animal not found"}), 404

    animal["_id"] = str(animal["_id"])
    return jsonify(animal_serializer(animal)), 200


@animal_api.put("/animals/<string:animal_id>")
def update_animal(animal_id):
    collection = current_app.config["MONGO_DB"]["animals"]

    try:
        obj_id = ObjectId(animal_id)
    except InvalidId:
        return jsonify({"error": "Invalid animal ID"}), 400

    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"error": "No data provided"}), 400

    result = collection.update_one({"_id": obj_id}, {"$set": payload})
    if result.matched_count == 0:
        return jsonify({"error": "Animal not found"}), 404

    return jsonify({"message": "Animal updated successfully"}), 200


@animal_api.delete("/animals/<string:animal_id>")
def delete_animal(animal_id):
    collection = current_app.config["MONGO_DB"]["animals"]

    try:
        obj_id = ObjectId(animal_id)
    except InvalidId:
        return jsonify({"error": "Invalid animal ID"}), 400

    result = collection.delete_one({"_id": obj_id})
    if result.deleted_count == 0:
        return jsonify({"error": "Animal not found"}), 404

    return jsonify({"message": "Animal deleted"}), 200
