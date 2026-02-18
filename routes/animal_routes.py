from flask import Blueprint, request, jsonify, render_template, current_app
from flask import render_template
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId
from models.animals import animal_serializer

animal_api = Blueprint('animal_api', __name__)


@animal_api.route('/')
def home():
    return render_template('index.html')

@animal_api.route("/animals", methods=["POST"])
def add_animals_bulk():
    try:
        db = current_app.config["MONGO_DB"]
        collection = db["animals"]

        data = request.get_json()

        if isinstance(data, dict):
            data = [data]

        if not isinstance(data, list):
            return jsonify({"error": "Invalid input format"}), 400

        result = collection.insert_many(data)
        inserted_ids = [str(_id) for _id in result.inserted_ids]

        return jsonify({
            "message": "Animals inserted successfully",
            "inserted_ids": inserted_ids
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@animal_api.route("/animals", methods=["GET"])
def get_animals():
    db = current_app.config["MONGO_DB"]
    collection = db["animals"]

    animals = list(collection.find())
    for animal in animals:
        animal['_id'] = str(animal['_id'])

    return jsonify([animal_serializer(animal) for animal in animals])


@animal_api.route("/animals/<id>", methods=["GET"])
def get_animal(id):
    try:
        db = current_app.config["MONGO_DB"]
        collection = db["animals"]

        # Validate ObjectId
        try:
            obj_id = ObjectId(id)
        except InvalidId:
            return jsonify({"error": "Invalid animal ID"}), 400

        animal = collection.find_one({"_id": obj_id})

        if not animal:
            return jsonify({"error": "Animal not found"}), 404

        animal["_id"] = str(animal["_id"])

        return jsonify(animal_serializer(animal)), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@animal_api.route('/animals/<id>', methods=['PUT'])
def update_animal(id):
    try:
        db = current_app.config["MONGO_DB"]
        collection = db["animals"]

        # Validate ObjectId
        try:
            obj_id = ObjectId(id)
        except InvalidId:
            return jsonify({"error": "Invalid animal ID"}), 400

        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Only update allowed fields
        allowed_fields = [
            "name",
            "category",
            "origin",
            "sleep_pattern",
            "food_habits",
            "fun_facts"
        ]

        update_data = {
            field: data[field]
            for field in allowed_fields
            if field in data
        }

        if not update_data:
            return jsonify({"error": "No valid fields to update"}), 400

        result = collection.update_one(
            {"_id": obj_id},
            {"$set": update_data}
        )

        if result.matched_count == 0:
            return jsonify({"error": "Animal not found"}), 404

        return jsonify({"message": "Animal updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@animal_api.route("/animals/<id>", methods=["DELETE"])
def delete_animal(id):
    db = current_app.config["MONGO_DB"]
    collection = db["animals"]

    collection.delete_one({"_id": ObjectId(id)})
    return jsonify({"msg": "Deleted"})
