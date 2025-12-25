from flask import Blueprint, request, jsonify
from app.nlp.entity_extractor import extract_entities
from app.nlp.command_router import route_command

nlp_bp = Blueprint("nlp", __name__)

@nlp_bp.route("/nlp", methods=["POST"])
def nlp_command():
    text = request.json.get("command")
    entities = extract_entities(text)
    result = route_command(text, entities)
    return jsonify({"response": result})

@nlp_bp.route("/chat", methods=["POST"])
def chatbot():
    text = request.json.get("message")

    entities = extract_entities(text)
    intent = detect_intent(text)

    return {
        "intent": intent,
        "structured_data": entities
    }
