from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId
from flasgger import Swagger, swag_from

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb://localhost:27017/")
db = client["animalDB"]
collection = db["animals"]

# Initialize Swagger
swagger = Swagger(app)

@app.route('/')
def index():
    return render_template('index.html')

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
                'name': {'type': 'string'},
                'category': {'type': 'string'},
                'origin': {'type': 'string'},
                'sleep_pattern': {'type': 'string'},
                'food_habits': {'type': 'string'},
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
        200: {'description': 'Animal added successfully'},
        400: {'description': 'Bad request'}
    }
})
def add_animal():
    data = request.json
    if data:
        result = collection.insert_one(data)
        return jsonify({"message": "Animal added successfully"}), 200
        """return jsonify({'inserted_id': str(result.inserted_id)})"""
    else:
        return jsonify({"error": "Invalid or missing JSON"}), 400

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
            'description': 'ID of the animal to update'
         },
        {
            'name': 'body',
            'in': 'body',
            'required': True, 
            'schema': {
               'type': 'object',
               'properties': {
                   'name': {'type': 'string'},
                   'category': {'type': 'string'},
                   'origin': {'type': 'string'},
                   'sleep_pattern': {'type': 'string'},
                   'food_habits': {'type': 'string'},
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
        400: {'description': 'Bad request'},
        404: {'description': 'Animal not found'}
        }
}
)

def update_animal(id):
    data = request.json
    print("PUT request received:", data)
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    try:
        result = collection.update_one({'_id': ObjectId(id)}, {'$set': data})
        if result.matched_count == 0:
              return jsonify({'error': 'No animal found with this ID'}), 404
        return jsonify({'message': 'Animal updated successfully'}), 200
    except Exception as e:
        print("Update error:", str(e))
        return jsonify({'error': 'Server error'}), 500

@app.route('/animals/<id>', methods=['DELETE'])
@swag_from({
    'tags': ['Animals'],
    'parameters': [{'name': 'id', 'in': 'path', 'type': 'string', 'required': True}],
    'responses': {200: {'description': 'Animal deleted successfully'}}
})

def delete_animal(id):
    collection.delete_one({'_id': ObjectId(id)})
    return jsonify({'message': 'Animal deleted'})

if __name__ == '__main__':
    app.run(debug=True)
