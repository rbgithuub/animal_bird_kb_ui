from flask import Blueprint, request, jsonify
from flask import render_template
from config import MONGO_URI
from pymongo import MongoClient
from bson import ObjectId
from models.animals import animal_serializer

animal_api = Blueprint('animal_api', __name__)
client = MongoClient(MONGO_URI)
db = client["animalDB"]
collection = db["animals"]


@animal_api.route('/')
def home():
    return render_template('index.html')

@animal_api.route("/animals", methods=["POST"])
def add_animals_bulk():
    try:
        data = request.get_json()
        
        # Ensure data is a list of dictionaries
        if not isinstance(data, list):
            return jsonify({"error": "Expected a list of animal objects"}), 400

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
    animals = list(collection.find())
    for animal in animals:
        animal['_id'] = str(animal['_id'])  # Convert ObjectId to string for JSON
    return jsonify(animals)


@animal_api.route("/animals/<id>", methods=["GET"])
def get_animal(id):
    animal = animals.find_one({"_id": ObjectId(id)})
    return jsonify(animal_serializer(animal))

"""@animal_api.route("/animals/<id>", methods=["PUT"])
def update_animal(id):
    data = request.json
    animals.update_one({"_id": ObjectId(id)}, {"$set": data})
    return jsonify({"msg": "Updated"})"""

@animal_api.route('/animals/<id>', methods=['PUT'])
def update_animal(id):
    print("Received PUT request for ID:", id)
    print("Request JSON:", request.json)
    data = request.json
    updated_data = {
        "name": data['name'],
        "category": data['category'],
        "origin": data['origin'],
        "sleep_pattern": data['sleep_pattern'],
        "food_habits": data['food_habits'],
        "fun_facts": data['fun_facts']
    }
    if data:
        result = collection.update_one({"_id": ObjectId(id)}, {"$set": updated_data})
        return jsonify({'message': 'Animal updated'}), 200
    else:
        return jsonify({"error":"No data provided"}), 400


@animal_api.route("/animals/<id>", methods=["DELETE"])
def delete_animal(id):
    animals.delete_one({"_id": ObjectId(id)})
    return jsonify({"msg": "Deleted"})
