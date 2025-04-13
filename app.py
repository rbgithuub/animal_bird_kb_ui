from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb://localhost:27017/")
db = client["animalDB"]
collection = db["animals"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/animals', methods=['GET'])
def get_animals():
    animals = list(collection.find())
    for animal in animals:
        animal['_id'] = str(animal['_id'])
    return jsonify(animals)

@app.route('/animals', methods=['POST'])
def add_animal():
    data = request.json
    result = collection.insert_one(data)
    return jsonify({'inserted_id': str(result.inserted_id)})

@app.route('/animals/<id>', methods=['PUT'])
def update_animal(id):
    data = request.json
    collection.update_one({'_id': ObjectId(id)}, {'$set': data})
    return jsonify({'message': 'Animal updated'})

@app.route('/animals/<id>', methods=['DELETE'])
def delete_animal(id):
    collection.delete_one({'_id': ObjectId(id)})
    return jsonify({'message': 'Animal deleted'})

if __name__ == '__main__':
    app.run(debug=True)
