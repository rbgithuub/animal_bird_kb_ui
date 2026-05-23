from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId
from flasgger import Swagger, swag_from


app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb://mongo:27017/")
db = client["animalDB"]
collection = db["animals"]

# Initialize Swagger
swagger = Swagger(app)

@app.route('/')
def index():
    return render_template('index.html')


# ── GET ALL ANIMALS ──────────────────────────────────────────────────────────
@app.route('/animals', methods=['GET'])
@swag_from({
    'tags': ['Animals'],
    'responses': {
        200: {
            'description': 'List of animals',
            'schema': {
                'type': 'array',
                'items': {'type': 'object'}
            }
        }
    }
})
def get_animals():
    animals = list(collection.find())
    for animal in animals:
        animal['_id'] = str(animal['_id'])
    return jsonify(animals)


# ── POST — ADD SINGLE OR MULTIPLE ANIMALS ────────────────────────────────────
@app.route('/animals', methods=['POST'])
@swag_from({
    'tags': ['Animals'],
    'consumes': ['application/json'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name':          {'type': 'string'},
                    'category':      {'type': 'string'},
                    'origin':        {'type': 'string'},
                    'sleep_pattern': {'type': 'string'},
                    'food_habits':   {'type': 'string'},
                    'fun_facts': {
                        'type': 'object',
                        'properties': {
                            '1': {'type': 'string'},
                            '2': {'type': 'string'}
                        }
                    }
                },
                'required': ['name', 'category', 'origin', 'sleep_pattern', 'food_habits', 'fun_facts']
            }
        }
    ],
    'responses': {
        201: {'description': 'Animal(s) added successfully'},
        400: {'description': 'Bad request'}
    }
})
def add_animal():
    # force=True  → works even if Content-Type header is missing
    # silent=True → returns None instead of raising 400 on malformed JSON
    data = request.get_json(force=True, silent=True)

    if not data:
        return jsonify({"error": "Invalid or missing JSON body"}), 400

    # ── Array input → insert_many ────────────────────────────
    if isinstance(data, list):
        if len(data) == 0:
            return jsonify({"error": "Empty array provided"}), 400

        for i, item in enumerate(data):
            if not isinstance(item, dict):
                return jsonify({
                    "error": f"Item at index {i} is not a valid JSON object"
                }), 400

        result = collection.insert_many(data)
        return jsonify({
            "message": f"{len(result.inserted_ids)} animal(s) added successfully",
            "inserted_ids": [str(oid) for oid in result.inserted_ids]
        }), 201

    # ── Single object input → insert_one ────────────────────
    elif isinstance(data, dict):
        result = collection.insert_one(data)
        return jsonify({
            "message": "Animal added successfully",
            "inserted_id": str(result.inserted_id)
        }), 201

    # ── Anything else is rejected ────────────────────────────
    else:
        return jsonify({"error": "Body must be a JSON object or array of objects"}), 400


# ── PUT — UPDATE ANIMAL BY ID ────────────────────────────────────────────────
@app.route('/animals/<string:id>', methods=['PUT'])
@swag_from({
    'tags': ['Animals'],
    'consumes': ['application/json'],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'MongoDB ObjectId of the animal to update'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name':          {'type': 'string'},
                    'category':      {'type': 'string'},
                    'origin':        {'type': 'string'},
                    'sleep_pattern': {'type': 'string'},
                    'food_habits':   {'type': 'string'},
                    'fun_facts': {
                        'type': 'object',
                        'properties': {
                            '1': {'type': 'string'},
                            '2': {'type': 'string'}
                        }
                    }
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Animal updated successfully'},
        400: {'description': 'Bad request — invalid ID or missing body'},
        404: {'description': 'Animal not found'},
        500: {'description': 'Internal server error'}
    }
})
def update_animal(id):
    data = request.get_json(force=True, silent=True)
    print("PUT request received:", data)

    if not data or not isinstance(data, dict):
        return jsonify({'error': 'No valid JSON data provided'}), 400

    try:
        object_id = ObjectId(id)
    except InvalidId:
        return jsonify({'error': f'Invalid ObjectId format: {id}'}), 400

    try:
        result = collection.update_one({'_id': object_id}, {'$set': data})
        if result.matched_count == 0:
            return jsonify({'error': 'No animal found with this ID'}), 404
        return jsonify({'message': 'Animal updated successfully'}), 200
    except Exception as e:
        print("Update error:", str(e))
        return jsonify({'error': 'Internal server error'}), 500


# ── DELETE — REMOVE ANIMAL BY ID ────────────────────────────────────────────
@app.route('/animals/<string:id>', methods=['DELETE'])
@swag_from({
    'tags': ['Animals'],
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'MongoDB ObjectId of the animal to delete'
        }
    ],
    'responses': {
        200: {'description': 'Animal deleted successfully'},
        400: {'description': 'Invalid ObjectId format'},
        404: {'description': 'Animal not found'},
        500: {'description': 'Internal server error'}
    }
})
def delete_animal(id):
    try:
        object_id = ObjectId(id)
    except InvalidId:
        return jsonify({'error': f'Invalid ObjectId format: {id}'}), 400

    try:
        result = collection.delete_one({'_id': object_id})
        if result.deleted_count == 0:
            return jsonify({'error': 'No animal found with this ID'}), 404
        return jsonify({'message': 'Animal deleted successfully'}), 200
    except Exception as e:
        print("Delete error:", str(e))
        return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)